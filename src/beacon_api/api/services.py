"""Sercive Endpoint.

The service endpoint reveals information about this beacon useful for the Beacon Network.

.. note:: See ``beacon_api`` root folder ``__init__.py`` for changing values used here.

GET /services
    Lists services known by this service.
    Returns an array of ServiceInfo.
GET /services?serviceType={serviceType}
    Returns an array of ServiceInfo filtered by type
GET /services?model={model}
    Returns an array of ServiceInfo in an specific model, i.e.: "Beacon-v1" or "GA4GH-ServiceInfo-v0.1"
GET /services?listFormat='full|short' 
    full: (default) Returns an array of ServiceInfo
    short: returns just the id, name, serviceURL, ServiceType and open.
GET /services?apiVersion={version}
    Returns an array of ServiceInfo filtered by Service API version supported
GET /services/{id}
    List a service details.
    Returns the ServiceInfo of the node
POST /services
    Requires HTTPS.
    Including Beacon info (/datasets too ??)
PUT /services/{id}
    Requires HTTPS.
DELETE /services/{id}
    Requires HTTPS.
"""

import logging
from json import dumps
from datetime import date, datetime

from .exceptions import BeaconServicesBadRequest, BeaconServerError

from ..utils.models import Beacon_v1, GA4GH_ServiceInfo_v01, organization


LOG = logging.getLogger(__name__)

# ----------------------------------------------------------------------------------------------------------------------
#                                                 FORMATTING
# ----------------------------------------------------------------------------------------------------------------------

def json_serial(obj):
    """
    JSON serializer for objects not serializable by default json code.
    Here used to handle datetime type objects.
    """

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))


def transform_services(record, short=False):
    """
    Transform the services record to a dict ready to be shown as a response. 
    If the short parameter is set to True, it will create a dict based on this shortened format.
    """
    response = dict(record)
    if not short: 
        # create a dict for the organization info
        organization = {}
        organization['id'] = response.pop('organization_stable_id')
        organization['name'] = response.pop('organization_name')
        organization['description'] = response.pop('organization_description')
        organization['address'] = response.pop('address')
        organization['welcome_url'] = response.pop('organization_welcome_url')
        organization['contact_url'] = response.pop('contact_url')
        organization['logo_url'] = response.pop('logo_url')
        organization['info'] = response.pop('info')
        
        # create the service dict
        response["id"] = response.pop("service_stable_id")
        response["name"] = response.pop("service_name")
        response["serviceType"] = response.pop("service_type")
        response["apiVersion"] = response.pop("api_version")
        response["serviceUrl"] = response.pop("service_url")
        response["entryPoint"] = response.pop("entry_point")
        response["organization"] = organization
        response["description"] = response.pop("service_description")
        response["version"] = response.pop("version")
        response["open"] = response.pop("open")
        response["welcomeUrl"] = response.pop("service_welcome_url")
        response["alternativeUrl"] = response.pop("alternative_url")
        # response["createDateTime"] = response.pop("create_date_time") 
        # response["updateDateTime"] = response.pop("update_date_time")
        response["createDateTime"] = dumps(response.pop("create_date_time"), default=json_serial)
        response["updateDateTime"] = dumps(response.pop("update_date_time"), default=json_serial)

    else: 
        # create the short service dict
        response["id"] = response.pop("service_stable_id")
        response["name"] = response.pop("service_name")
        response["serviceUrl"] = response.pop("service_url")
        response["serviceType"] = response.pop("service_type")
        response["open"] = response.pop("open")

    return response


# ----------------------------------------------------------------------------------------------------------------------
#                                         MAIN QUERY TO THE DATABASE
# ----------------------------------------------------------------------------------------------------------------------

async def fetch_filtered_services(db_pool, processed_request):
    """
    Fetch the services based on the filter parameters given.
    """
    # Get the parameters
    service_type = None if not processed_request.get('serviceType') else processed_request.get('serviceType')
    list_format =  None if not processed_request.get('listFormat') else processed_request.get('listFormat')
    version = None if not processed_request.get('apiVersion') else processed_request.get('apiVersion')

    list_services = ["'" + service_type + "'"] if service_type else ["'GA4GHBeacon'", "'GA4GHAggregator'", "'GA4GHRegistry'"]
    version = ["'" + version + "'"] if version else ['version']

    # Take one connection from the database pool
    async with db_pool.acquire(timeout=180) as connection:
        # Fetch different parameters depending on the list_format
        if not list_format or list_format == 'long':
            try:
                query = f"""SELECT *
                           FROM service WHERE
                           service_type IN ({",".join(list_services)})
                           AND version IN ({",".join(version)});
                           """
                LOG.debug(f"QUERY to fetch services info: {query}")           
                statement = await connection.prepare(query)
                db_response = await statement.fetch()
            except Exception as e:
                raise BeaconServerError(f'Query service DB error: {e}')
        elif list_format == 'short': # returns only id, name, serviceURL, ServiceType and open.

            try:
                query = f"""SELECT service_stable_id, service_name, service_url, service_type, open
                           FROM service WHERE
                           service_type IN ({",".join(list_services)})
                           AND version IN ({",".join(version)});
                           """
                LOG.debug(f"QUERY to fetch short services info: {query}")           
                statement = await connection.prepare(query)
                db_response = await statement.fetch()
            except Exception as e:
                raise BeaconServerError(f'Query short service DB error: {e}')
        services = []
        for record in list(db_response):
            transformed_service = transform_services(record, short=True) if list_format == 'short' else transform_services(record)
            services.append(transformed_service)
        return services



# ----------------------------------------------------------------------------------------------------------------------
#                                                SERVICES HANDLER
# ----------------------------------------------------------------------------------------------------------------------

async def services_handler(db_pool, processed_request, request):
    """Construct the `Beacon` app services dict.

    :return beacon_services: A dict that contain the services about this ``Beacon``.
    """

    # Return an error for the parameters that are not implemented
    if processed_request.get('model'):
        processed_request.pop('model')
        raise BeaconServicesBadRequest(processed_request, request.host, "The 'model' parameter is not supported yet.")  

    # Query the DB to get all the services (the filtering is done inside the fetch_filtered_services function)
    services = await fetch_filtered_services(db_pool, processed_request)

    return services



# FIRST IMPLEMENTATION: works only if just the self-beacon service is shown
# async def services_handler(db_pool, processed_request, request):
#     """Construct the `Beacon` app services dict.

#     :return beacon_services: A dict that contain the services about this ``Beacon``.
#     """
#     # Handle the query options and show what is asked for
#     serviceType = processed_request.get('serviceType')
#     model = processed_request.get('model')
#     listFormat = processed_request.get('listFormat')
#     version = processed_request.get('apiVersion')

#     # Return an error for the parameters that are not implemented
#     if serviceType:
#         raise BeaconServicesBadRequest(processed_request, request.host, "The 'serviceType' parameter is not supported yet.")
#     if version:
#         raise BeaconServicesBadRequest(processed_request, request.host, "The 'apiVersion' parameter is not supported yet.")  


#     # First, we decide which model we will show, the default is Beacon-v1
#     if model == "GA4GH-ServiceInfo-v0.1":
#         serviceInfo = GA4GH_ServiceInfo_v01(request.host)
#     elif model == "Beacon-v1":
#         serviceInfo = Beacon_v1(request.host)
#     else: 
#         serviceInfo = Beacon_v1(request.host)

#     # Then, we leave it full length or we shorten it, the default is full
#     if listFormat == "short": 
#         if model == "GA4GH-ServiceInfo-v0.1":
#             raise BeaconServicesBadRequest(processed_request, request.host, f"The combination of 'model': {model} and 'format': {listFormat} is not supported")
#         else:
#             required = ["id", "name", "serviceUrl", "serviceType", "open"]
#             serviceInfo = {k: v for k, v in serviceInfo.items() if k in required}

#     return serviceInfo 

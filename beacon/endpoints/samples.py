# # SAMPLES


class SamplesParameters(RequestParameters):
    hello = Field()
    
    def correlate(self, req, values):
        pass
#     """
#     It  takes a dictionary of the request parameters and checks the correct
#     combination of parameters, the lack of required parameters, etc. It takes
#     the validation a step further from the syntax validation that is done with
#     the JSON schema. 
#     """

#     def bad_request(m):
#         raise BeaconBadRequest(query_params, request.host, m)

#     start = query_params.get("start")
#     end = query_params.get("end")

#     if end and not start:
#         bad_request("'end' can't be provided without 'start'")

#     # Define values with the result of the get()
#     referenceName = query_params.get("referenceName")
#     assemblyId = query_params.get("assemblyId")

#     if start and (not referenceName or not assemblyId):
#         bad_request("'referenceName' and 'assemblyId' are requiered when 'start' is given")

#     referenceBases = query_params.get("referenceBases")
#     alternateBases = query_params.get("alternateBases")

#     if not start and (referenceBases or alternateBases):
#         bad_request("'start' is needed when using 'referenceBases' or 'alternateBases'")
     
#     ## to be continued...?






def intermediate_formulation(response):
    return response


proxy = SamplesParameters()
def handler(request):
    qparams_raw, qparams_processed = await proxy.fetch(request)
    
    response = {}
    return json_response(response)

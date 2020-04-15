# -*- coding: utf-8 -*-

"""Database Connection."""

import sys
import logging
import asyncio
from contextlib import asynccontextmanager
from functools import wraps
import traceback
# import inspect

import asyncpg

from .. import conf
from ..api.exceptions import BeaconServerError

LOG = logging.getLogger(__name__)

class DBConnection():
    """Databse connection setup."""

    db_pool = None

    async def connect(self, force=False):
        """Get the database connection (which encapsulates a database session).

        Upon success, the connection is cached.
        """
        if force:
            self.close()

        if self.db_pool:
            return

        LOG.info("Creating a connection pool")
        # Connection pool handles reconnections and keeps some expensive connections open for reuse
        self.db_pool = await asyncpg.create_pool(host=conf.database_url,
                                                 port=conf.database_port,
                                                 user=conf.database_user,
                                                 password=conf.database_password,
                                                 database=conf.database_name,
                                                 server_settings={'search_path': conf.database_schema},
                                                 # min_size=0, # initializing with 0 connections allows the web server to
                                                 # start and also continue to live
                                                 max_queries=getattr(conf, 'database_max_queries', 50000),
                                                 max_size=20, # for now limiting the number of connections in the pool
                                                 timeout=getattr(conf, 'database_timeout', 120),
                                                 command_timeout=getattr(conf, 'database_command_timeout', 180),
                                                 max_cached_statement_lifetime=0,
                                                 max_inactive_connection_lifetime=180)
        # Ping the db
        async with self.db_pool.acquire() as conn:
            try:
                conn.execute('SELECT 1;')
                LOG.debug('Ping successful')
            except (asyncpg.exceptions._base.InterfaceError,
                    asyncpg.exceptions._base.PostgresError) as e:
                LOG.error('DB Error: %s', e)
                raise BeaconServerError(f'DB Error: {e}')

    def asyncgen_execute(self, func):
        async def inner(*args, **kwargs):
            async with self.connection() as connection:
                async for obj in func(connection, *args, **kwargs):
                    yield obj
        return inner

    def coroutine_execute(self, func):
        async def inner(*args, **kwargs):
            async with self.connection() as connection:
                return await func(connection, *args, **kwargs)
        return inner

    # def execute(self, func):
    #     if inspect.isasyncgenfunction(func):
    #         return self.asyncgen_execute(func)
    #     else:
    #         return self.coroutine_execute(func)

    @asynccontextmanager
    async def connection(self):
        if self.db_pool is None:
            await self.connect()
        LOG.debug('----------- acquiring connection')
        conn = await self.db_pool.acquire()
        try:
            yield conn
        except (asyncpg.exceptions._base.InterfaceError,
                asyncpg.exceptions._base.PostgresError) as e:
            LOG.error('DB Error: %s', e)
            traceback.print_exc()
            raise BeaconServerError(f'DB Error: {e}')
        finally:
            LOG.debug('----------- releasing connection')
            self.db_pool.release(conn)

    async def close(self):
        """Close DB Connection."""
        LOG.debug("Closing the database")
        if self.db_pool:
            try:
                await asyncio.wait_for(self.db_pool.close(), timeout=10)
            except asyncio.TimeoutError:
                LOG.error('Timeout after 10s!')
            self.db_pool = None

def simple_listener(c,m):
    LOG.debug(m)

######################################
#           Business logic           #
######################################

# Instantiate the global connection
pool = DBConnection()

# We might be able to use postgres partitioning
# https://www.postgresql.org/docs/12/ddl-partitioning.html
# We can use the 3 access types: PUBLIC, REGISTERED and CONTROLLED
#
# Returns a generator of record, make sure to consume them before the connection is closed
@pool.asyncgen_execute
async def fetch_datasets_access(connection, datasets=None):
    """
    Retrieve available datasets as triples (access_type::str, id::int, datasetId::str)

    In this case, any error executing the database request is captured and an empty list is returned.
    """
    LOG.info('Retrieving info about the available datasets (id and access type).')
    LOG.debug('Originally selecting datasets: %s', datasets)
    #async with connection.transaction():
    where_clause = ' WHERE stable_id = ANY($1)' if datasets else ''
    query = f"""SELECT access_type, id, stable_id FROM {conf.database_schema}.beacon_dataset{where_clause};"""
    LOG.debug("QUERY datasets access: %s", query)
    try:
        statement = await connection.prepare(query)
        coro = statement.fetch(datasets) if datasets else statement.fetch()
        response = await coro
        for record in response:
            yield (record['access_type'], record['id'], record['stable_id']) # not using record: copy
    except Exception as e:
        LOG.error("DB error while retrieving datasets: %s", e)

# Returns a generator of record, make sure to consume them before the connection is closed
@pool.asyncgen_execute
async def fetch_datasets_metadata(connection, transform=None):
    """
    Execute query for returning dataset metadata.
    """
    LOG.info('Retrieving datasets metadata')
    query = f"""SELECT stable_id                AS "datasetId",
                       description              AS "description",
                       access_type              AS "accessType",
                       reference_genome         AS "assemblyId",
                       COALESCE(variant_cnt, 0) AS "variantCount",
                       COALESCE(call_cnt   , 0) AS "callCount",
                       COALESCE(sample_cnt , 0) AS "sampleCount"
                FROM {conf.database_schema}.beacon_dataset;"""
    LOG.debug("QUERY: %s", query)
    response = await connection.fetch(query)
    for record in response:
        yield transform(record) if callable(transform) else record
    # return [collections.namedtuple('Dataset Metadata', record.keys())(*record.values())
    #         for record in response]

# Returns a generator of record, make sure to consume them before the connection is closed
@pool.asyncgen_execute
async def data_summary(connection, qparams):
    """
    Contact the DB to fetch the information about the datasets. 
    :misses: set to True for retrieving data about datasets without the queried variant
    :accessible_missing: list of accessible datasets without the variant.
    Returns list of datasets dictionaries. 
    """
    LOG.info('Retrieving data_summary')
    dollars = ", ".join([ f"${i}" for i in range(1, 14)]) # 1..13
    LOG.debug("dollars: %s", dollars)
    query = f"""SELECT dataset_id   AS "_internal_id",
                       variant_cnt  AS "variantCount",
                       call_cnt     AS "callCount",
                       sample_cnt   AS "sampleCount",
                       frequency    AS "frequency",
                       num_variants AS "numVariants"
                FROM {conf.database_schema}.query_data_summary_response({dollars});"""
    LOG.debug("QUERY: %s", query)
    statement = await connection.prepare(query)
    db_response = await statement.fetch(qparams.variantType,
	                                qparams.start,
	                                qparams.startMin,
	                                qparams.startMax,
	                                qparams.end,
	                                qparams.endMin,
	                                qparams.endMax,
	                                qparams.referenceName,
	                                qparams.referenceBases,
	                                qparams.alternateBases,
	                                qparams.assemblyId,
	                                [record[1] for record in qparams.datasetIds], # list of int
	                                qparams.filters) # filters as-is
        
    for record in db_response:
        yield record
        # yield (True,
        #        record["_internal_id"],
        #        record["variantCount"],
        #        record["callCount"],
        #        record["sampleCount"],
        #        float(record["frequency"] or 0), # is it ok with 0.0 ?
        #        # 0 if record["frequency"] is None else float(record["frequency"])
        #        record.get("numVariants", 0))
    
    # keys = ("exists","_internal_id","variantCount","callCount","sampleCount","frequency","numVariants")
    # for record in db_response:
    #     yield collections.namedtuple('Data summary', keys)(*response)



# Returns a generator of record, make sure to consume them before the connection is closed
@pool.coroutine_execute
async def patients(connection, qparams, individual_id, process=None):
    """
    Contacts the DB to fetch the info.
    Returns a pd.DataFrame with the response. 
    """
    connection.add_log_listener(simple_listener)
    dollars = ", ".join([ f"${i}" for i in range(1, 18)]) # 1..17
    query = f"""SELECT * FROM {conf.database_schema}.query_patients({dollars});"""
    LOG.debug("QUERY: %s", query)
    statement = await connection.prepare(query)
    db_response = await statement.fetch(None,                   # _variant_type text,
	                                qparams.start,          # _start integer,
	                                qparams.startMin,       # _start_min integer,
	                                qparams.startMax,       # _start_max integer,
	                                qparams.end,            # _end integer,
	                                qparams.endMin,         # _end_min integer,
	                                qparams.endMax,         # _end_max integer,
	                                qparams.referenceName,  # _chromosome character varying,
	                                qparams.referenceBases, # _reference_bases text,
	                                qparams.alternateBases, # _alternate_bases text,
	                                qparams.assemblyId,     # _reference_genome text,
	                                '', #[record[1] for record in qparams.datasetIds], # _dataset_ids int[],
	                                #[record[2] for record in qparams.datasetIds], # _dataset_names text[],
	                                None,                   # _biosample_stable_id text,
	                                individual_id,          # _individual_stable_id text,
	                                qparams.filters,        # filters as-is,  # _filters text[],
	                                qparams.skip,           # _skip integer,
	                                qparams.limit)          # _limit integer
    
    if not db_response or not callable(process):
        LOG.debug(f"No response for this query.")
        return False, []

    return process(db_response)


# Returns a generator of record, make sure to consume them before the connection is closed
@pool.asyncgen_execute
async def fetch_filtering_terms(connection):
    """
    Execute query for returning the filtering terms.
    """
    # async with connection.transaction():
    query = "SELECT ontology, term, label FROM ontology_term;"
    db_response = await connection.fetch(query)
    for record in db_response:
        yield record


# Returns a generator of record, make sure to consume them before the connection is closed
@pool.asyncgen_execute
async def access_levels_datasets(connection):
    """ Fetch the special datasets (with different access levels).
    They are stored in the dataset_access_level_table in the DB.
    Return two dicts prepared to be shown in the response (one for displayDatasetDifferences=false, the other for true).
    """
    LOG.debug('fetch special datasets access levels info')
    query = """SELECT dt.stable_id    AS dataset_id,
                      al.parent_field AS parent_field,
                      al.field        AS field,
                      al.access_level AS access_level
               FROM dataset_access_level_table al
               JOIN beacon_dataset dt
               ON al.dataset_id=dt.id;"""
    LOG.debug("QUERY: %s", query)
    db_response = await connection.fetch(query)
    for record in db_response:
        yield record

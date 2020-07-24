# -*- coding: utf-8 -*-

"""Database Connection."""

import sys
import logging
from contextlib import asynccontextmanager
from functools import wraps
import traceback
# import inspect

import asyncpg

from .. import conf
from .exceptions import BeaconServerError

LOG = logging.getLogger(__name__)

class DBConnection():
    """Databse connection setup."""

    db_pool = None

    async def connect(self, force=False):
        """Get the database connection (which encapsulates a database session).

        Upon success, the connection is cached.
        """
        if force:
            await self.close()

        if self.db_pool:
            return

        LOG.info("Creating a connection pool to %s:%s", conf.database_url, conf.database_port)
        # Connection pool handles reconnections and keeps some expensive connections open for reuse
        self.db_pool = await asyncpg.create_pool(host=conf.database_url,
                                                 port=conf.database_port,
                                                 user=conf.database_user,
                                                 password=conf.database_password,
                                                 database=conf.database_name,
                                                 server_settings={'search_path': conf.database_schema,
                                                                  'application_name': conf.database_app_name},
                                                 min_size=0, # initializing with 0 connections allows the web server to
                                                 # start and also continue to live
                                                 max_queries=getattr(conf, 'database_max_queries', 50000),
                                                 max_size=10, # for now limiting the number of connections in the pool
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
                raise ValueError(f'DB Error: {e}') # not using a beacon error. We can ping _before_ the server starts.

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
                asyncpg.exceptions._base.PostgresError,
                asyncpg.exceptions.UndefinedFunctionError) as e:
            LOG.error('DB Error: %s', e)
            # traceback.print_exc()
            raise BeaconServerError(f'DB Error: {e}')
        finally:
            LOG.debug('----------- releasing connection')
            await self.db_pool.release(conn)

    async def close(self):
        """Close DB Connection."""
        LOG.debug("Closing the database")
        if self.db_pool:
            self.db_pool.terminate()
        self.db_pool = None


######################################
#           Business logic           #
######################################

# Instantiate the global connection
pool = DBConnection()


# Get the latest modification data of a DB dataset 
@pool.coroutine_execute
async def get_last_modified_date(connection):
    LOG.info('Retrieving last modified date')

    query = f"""SELECT MAX(last_uploaded) FROM {conf.database_schema}.beacon_dataset;"""
    LOG.debug("QUERY: %s", query)
    return await connection.fetchval(query)


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



# Returns a generator of record, make sure to consume them before the connection is closed
@pool.asyncgen_execute
async def fetch_filtering_terms(connection):
    """
    Execute query for returning the filtering terms.
    """
    # async with connection.transaction():
    query = "SELECT ontology, term, label FROM ontology_term;"
    response = await connection.fetch(query)
    for record in response:
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
    response = await connection.fetch(query)
    for record in response:
        yield record


# Returns a generator of record, make sure to consume them before the connection is closed
@pool.asyncgen_execute
async def fetch_viral_variants(connection, start, end, reference, alternate):
    LOG.info('Retrieving viral variant information')

    dollars = ", ".join([ f"${i}" for i in range(1, 14)]) # 1..13
    LOG.debug("dollars: %s", dollars)
    query = f"""SELECT * FROM {conf.database_schema}.query_variants({dollars}) ORDER BY start ASC, reference ASC;"""
    LOG.debug("QUERY: %s", query)
    statement = await connection.prepare(query)
    response = await statement.fetch(None, # _variant_type text,
                                     start, # _start integer,
                                     None, # _start_min integer,
                                     None, # _start_max integer,
                                     None if end is None else end+1, # _end integer,
                                     None, # _end_min integer,
                                     None, # _end_max integer,
                                     reference, # _reference_bases text,
                                     alternate, # _alternate_bases text,
                                     None, # _biosample_stable_id text,
                                     None, # _filters text[],
                                     None, # _offset integer,
                                     None) # _limit integer
    for record in response:
        yield record




@pool.asyncgen_execute
async def fetch_gene_to_region(connection, term, limit):
    LOG.info('Retrieving viral variant information')

    query = f"""SELECT t.class as cls, t.start, t.end, t.name 
                FROM {conf.database_schema}.gene_to_region_table t
                WHERE t.name ILIKE  '%' || $1 || '%' 
                ORDER BY char_length(t.name) ASC, t.name ASC -- length order, then lexicographic order
                LIMIT $2;"""
    LOG.debug("QUERY: %s", query)
    statement = await connection.prepare(query)
    response = await statement.fetch(str(term), limit)
    for record in response:
        yield record
        
@pool.coroutine_execute
async def get_nsamples(connection):
    LOG.info('Retrieving viral number of samples')

    query = f"""SELECT COUNT(*) FROM {conf.database_schema}.sample_table;"""
    LOG.debug("QUERY: %s", query)
    return await connection.fetchval(query)


# SNP query endpoint
# Returns a generator of record, make sure to consume them before the connection is closed
@pool.asyncgen_execute
async def fetch_snp_variants(connection, start, end, reference, alternate):
    LOG.info('Retrieving SNP viral variant information')

    query = f"""SELECT * FROM {conf.database_schema}.query_snp($1, $2, $3)
                WHERE variant_type = 'SNP'
                AND dataset_stable_id NOT IN ('GISAID')
                ORDER BY start ASC, reference ASC;"""
    LOG.debug("QUERY: %s", query)
    statement = await connection.prepare(query)
    response = await statement.fetch(start, reference, alternate)
    for record in response:
        yield record




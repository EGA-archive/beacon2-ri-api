# -*- coding: utf-8 -*-

"""Database Connection."""

import sys
import logging
import asyncio
from contextlib import asynccontextmanager
from functools import wraps

import asyncpg

from .. import conf
from ..api.exceptions import BeaconServerError

LOG = logging.getLogger(__name__)

class DBConnection():
    """Databse connection setup."""

    db_pool = None
    interval = getattr(conf, 'database_connection_interval', 1) # in seconds
    attempts = getattr(conf, 'database_connection_attempts', 30)

    def __init__(self, on_failure=None):
        self.on_failure = on_failure

    async def connect(self, force=False):
        """Get the database connection (which encapsulates a database session).

        Upon success, the connection is cached.
        """
        if force:
            self.close()

        if self.db_pool:
            return

        LOG.info("Initializing a connection | Attempts: %d", self.attempts)

        backoff = self.interval
        for count in range(self.attempts):
            try:
                LOG.debug("Connection attempt %d", count)
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
                LOG.debug("Connection successful")
                return
            except Exception as e:
                LOG.debug("Database connection error: %r", e)
            except psycopg2.InterfaceError as e:
                LOG.debug("Invalid connection parameters: %r", e)
                break
            sleep(backoff)
            backoff = (2 ** (count // 10)) * self.interval
            # from  0 to  9, sleep 1 * self.interval secs
            # from 10 to 19, sleep 2 * self.interval secs
            # from 20 to 29, sleep 4 * self.interval secs ... etc

        # fail to connect
        if self.on_failure and callable(self.on_failure):
            LOG.error("Failed to connect.")
            self.on_failure()

    @asynccontextmanager
    async def connection(self):
        """Return DB Cursor, thus reusing it."""
        if self.db_pool is None:
            await self.connect()
        async with self.db_pool.acquire() as conn:
            try:
                yield conn
            except (asyncpg.exceptions._base.InterfaceError,
                    asyncpg.exceptions._base.PostgresError) as e:
                LOG.error('DB Error: %s', e)
                raise BeaconServerError(f'DB Error: {e}')

    async def close(self):
        """Close DB Connection."""
        LOG.debug("Closing the database")
        if self.db_pool:
            try:
                await asyncio.wait_for(self.db_pool.close(), timeout=10)
            except asyncio.TimeoutError:
                LOG.error('Timeout: 10 seconds for the closing the database')
            self.db_pool = None

######################################
#           Business logic           #
######################################

# Instantiate the global connection
pool = DBConnection()

# We might be able to use postgres partitioning
# https://www.postgresql.org/docs/12/ddl-partitioning.html
# We can use the 3 access types: PUBLIC, REGISTERED and CONTROLLED
async def fetch_datasets_access(datasets=None):
    """Retrieve 3 lists of the available datasets depending on the access type"""
    LOG.info('Retrieving info about the available datasets (id and access type).')
    LOG.debug('Originally selecting datasets: %s', datasets)
    async with pool.connection() as connection:
        #async with connection.transaction():
        where_clause = ' WHERE stable_id = ANY($1)' if datasets else ''
        query = f"""SELECT access_type, id, stable_id FROM {conf.database_schema}.beacon_dataset{where_clause};"""
        LOG.debug("QUERY datasets access: %s", query)
        try:
            statement = await connection.prepare(query)
            if datasets:
                response = await statement.fetch(datasets)
            else:
                response = await statement.fetch()
            return [(record['access_type'], record['id'], record['stable_id'])
                    for record in response]
        except Exception as e:
            LOG.error("DB error while retrieving datasets: %s", e)
            return []

async def fetch_datasets_metadata():
    """
    Execute query for returning dataset metadata.
    """
    LOG.info('Retrieving info about the available datasets (id and access type).')
    async with pool.connection() as connection:
        query = """SELECT stable_id                as "datasetId",
                          description              as "description",
                          access_type              as "accessType",
                          reference_genome         as "assemblyId",
                          COALESCE(variant_cnt, 0) as "variantCount",
                          COALESCE(call_cnt   , 0) as "callCount",
                          COALESCE(sample_cnt , 0) as "sampleCount"
                   FROM {conf.database_schema}.beacon_dataset;"""

        response = await connection.fetch(query)
        return [collections.namedtuple('Dataset Metadata', record.keys())(*record.values())
                for record in response]

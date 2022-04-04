import logging
import asyncpg
from asyncpg import Pool
from typing import Dict, Optional

from beacon.utils.json import json_decoder, json_encoder

LOG = logging.getLogger(__name__)

class Permissions():
    """Base class, just to agree on the interface."""
    def __init__(self, *args, **kwargs):
        pass

    async def initialize(self):
        raise NotImplementedError('Overload this function in a subclass')

    async def get(self, username, requested_datasets=None):
        """Return an iterable for the granted datasets for the given username and within a requested list of datasets."""
        raise NotImplementedError('Overload this function in a subclass')

    async def close(self):
        raise NotImplementedError('Overload this function in a subclass')



class DummyPermissions(Permissions):
    """
    Dummy permissions plugin
    
    We hard-code the dataset permissions.
    """

    db: Dict = {}

    def __init__(self, *args, **kwargs):
        # Dummy permission database
        self.db = {
            "john": ["GiaB", "dataset-registered", "dataset-controlled"],
            "jane": ["GiaB", "dataset-registered"],
        }

    async def initialize(self):
        pass

    async def get(self, username, requested_datasets=None):
        datasets = set(self.db.get(username))
        if requested_datasets:
            return set(requested_datasets).intersection(datasets)
        else:
            return datasets

    async def close(self):
        pass


class PostgresPermissions(Permissions):
    """
    Postgres permissions plugin
    
    """
    db: Optional[Pool] = None
    args = []
    kwargs = {}

    def __init__(self, *args, **kwargs):
        LOG.info("Creating a connection pool with %s and %s", args, kwargs)
        self.args = args
        self.kwargs = kwargs

    async def initialize(self):
        import asyncpg
        # Connection pool handles reconnections and keeps some expensive connections open for reuse
        self.db = await asyncpg.create_pool(*self.args, **self.kwargs)


    async def get(self, username, requested_datasets=None):
        try:
            assert(self.db is not None)
            async with self.db.acquire() as conn:
                await conn.set_type_codec('jsonb', encoder=json_encoder, decoder=json_decoder, schema='pg_catalog')            
                query = "SELECT dataset FROM datasets where username = $1 and datasets IN $2;"
                response = await conn.fetch(query, username, requested_datasets)
                return [r['dataset'] async for r in response]
        except (asyncpg.exceptions._base.InterfaceError,
                asyncpg.exceptions._base.PostgresError,
                asyncpg.exceptions.UndefinedFunctionError) as e:
            LOG.error('DB Error: %s', e)
            return None

    async def close(self):
        """Close DB Connection."""
        LOG.debug("Closing the database")
        if self.db:
            self.db.terminate()
        self.db = None

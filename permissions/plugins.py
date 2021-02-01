import logging

LOG = logging.getLogger(__name__)

class Permissions():
    """Base class, just to agree on the interface."""
    def __init__(self, *args, **kwargs):
        pass

    async def initialize(self):
        raise NotImplementedError('Overload this function in a subclass')

    async def get(self, username):
        raise NotImplementedError('Overload this function in a subclass')

    async def close(self):
        raise NotImplementedError('Overload this function in a subclass')



class DummyPermissions(Permissions):
    """
    Dummy permissions plugin
    
    We hard-code the dataset permissions.
    """

    db = None

    def __init__(self, *args, **kwargs):
        # Dummy permission database
        self.db = {
            "john": ["GiaB", "dataset-registered", "dataset-controlled"],
            "jane": ["GiaB", "dataset-registered"],
        }

    async def initialize(self):
        pass

    async def get(self, username):
        return self.db.get(username)

    async def close(self):
        pass


class PostgresPermissions(Permissions):
    """
    Postgres permissions plugin
    
    """
    db = None
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


    async def get(self, username):
        try:
            async with self.db.acquire() as conn:
                await conn.set_type_codec('jsonb', encoder=json_encoder, decoder=json_decoder, schema='pg_catalog')            
                query = "SELECT dataset FROM datasets where username = $1;"
                response = await connection.fetch(query, username)
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

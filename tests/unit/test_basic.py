import unittest
from unittest import mock

import asynctest
from aiohttp import web
from beacon_api.app import init, main, initialize


# from test.support import EnvironmentVarGuard


class TestBasicFunctionsApp(asynctest.TestCase):
    """Test App Base.
    Testing basic functions from web app.
    """

    def setUp(self):
        """Initialise fixtures."""
        pass

    def tearDown(self):
        """Remove setup variables."""
        pass

    @mock.patch('beacon_api.app.web')
    def test_main(self, mock_webapp):
        """Should start the webapp."""
        main()
        mock_webapp.run_app.assert_called()

    async def test_init(self):
        """Test init type."""
        server = await init()
        self.assertIs(type(server), web.Application)

    @asynctest.mock.patch('beacon_api.app.set_cors')
    async def test_initialize(self, mock_cors):
        """Test create db pool, should just return the result of init_db_pool.
        We will mock the init_db_pool, thus we assert we just call it.
        """
        app = {}
        with asynctest.mock.patch('beacon_api.app.init_db_pool') as db_mock:
            await initialize(app)
            db_mock.assert_called()

if __name__ == '__main__':
    unittest.main()
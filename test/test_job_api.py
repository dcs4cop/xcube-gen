import os
import unittest

import requests_mock

from test.config import SH_CFG
from xcube_gen.jobapi import JobApi


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        os.environ["XCUBE_GEN_API_SERVER_URL"] = "https://test"
        os.environ["XCUBE_GEN_AUTH_AUD"] = 'https://xcube-gen.brockmann-consult.de/api/v1/'
        os.environ["XCUBE_GEN_AUTH_CLIENT_ID"] = "sdfvdsvsdv"
        os.environ["XCUBE_GEN_AUTH_DOMAIN"] = "https://edc.eu.auth0.com"
        os.environ["XCUBE_GEN_API_SERVER_PORT"] = "8000"
        os.environ["XCUBE_GEN_AUTH_CLIENT_SECRET"] = "dfvsdvdfsv"
        os.environ["XCUBE_GEN_API_USER_NAME"] = "duffy_duck@supermail.com"

    @requests_mock.Mocker()
    def test_jobapi(self, m):
        m.post('https://edc.eu.auth0.com/oauth/token', json={'access_token': 'dsafsafs'})

        expected = 'a663fb671b2e5afb75c2879362633c351'
        api = JobApi()

        self.assertEqual("https://test", api._api_url)
        self.assertEqual("8000", api._api_port)
        self.assertEqual("dfvsdvdfsv", api._auth_client_secret)
        self.assertEqual("sdfvdsvsdv", api._auth_client_id)
        self.assertEqual("https://xcube-gen.brockmann-consult.de/api/v1/", api._auth_aud)
        self.assertEqual("https://edc.eu.auth0.com", api._auth_domain)
        self.assertEqual("duffy_duck@supermail.com", api._user_name)
        self.assertEqual(expected, api._user_id)

        self.assertEqual({'access_token': 'dsafsafs'}, api._token)

    @requests_mock.Mocker()
    def test_create(self, m):
        expected = {'job_id': 'adsc', 'status': {'error': False}}

        m.post('https://edc.eu.auth0.com/oauth/token', json={'access_token': 'dsafsafs'})
        m.put('https://test:8000/jobs/a663fb671b2e5afb75c2879362633c351', json=expected)

        api = JobApi()
        res = api.create(SH_CFG)
        self.assertDictEqual(expected, res)

    @requests_mock.Mocker()
    def test_status(self, m):
        expected = {'result': 'ok'}
        m.post('https://edc.eu.auth0.com/oauth/token', json={'access_token': 'dsafsafs'})
        m.get('https://test:8000/jobs/a663fb671b2e5afb75c2879362633c351/xcube-gen-a7a8f791',
              json=expected)

        api = JobApi()
        res = api.status('xcube-gen-a7a8f791')
        self.assertDictEqual(expected, res)

    @requests_mock.Mocker()
    def test_list(self, m):
        expected = {'result': ['job1', 'job2']}
        m.post('https://edc.eu.auth0.com/oauth/token', json={'access_token': 'dsafsafs'})
        m.get('https://test:8000/jobs/a663fb671b2e5afb75c2879362633c351',
              json=expected)

        api = JobApi()
        res = api.list()
        self.assertDictEqual(expected, res)

    @requests_mock.Mocker()
    def test_delete(self, m):
        expected = {'result': 'ok'}
        m.post('https://edc.eu.auth0.com/oauth/token', json={'access_token': 'dsafsafs'})
        m.delete('https://test:8000/jobs/a663fb671b2e5afb75c2879362633c351/xcube-gen-a7a8f791',
                 json=expected)

        api = JobApi()
        res = api.delete('xcube-gen-a7a8f791')
        self.assertDictEqual(expected, res)


if __name__ == '__main__':
    unittest.main()

# The MIT License (MIT)
# Copyright (c) 2020 by the xcube development team and contributors
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import hashlib
import os
from typing import Union

import requests
from dotenv import load_dotenv

from xcube_gen import api
from xcube_gen.typedefs import AnyDict, Error, JsonObject


class JobApi:
    def __init__(self):
        load_dotenv()

        self._user_name = os.getenv("XCUBE_GEN_API_USER_NAME")
        self._api_url = os.getenv("XCUBE_GEN_API_SERVER_URL")
        self._api_prefix = os.getenv("XCUBE_GEN_API_SERVER_PREFIX")
        self._api_port = os.getenv("XCUBE_GEN_API_SERVER_PORT")
        self._auth_aud = os.getenv("XCUBE_GEN_AUTH_AUD")
        self._auth_client_id = os.getenv("XCUBE_GEN_AUTH_CLIENT_ID")
        self._auth_domain = os.getenv("XCUBE_GEN_AUTH_DOMAIN")
        self._auth_client_secret = os.getenv("XCUBE_GEN_AUTH_CLIENT_SECRET")

        self._token = self._get_token_for_client()
        # self._user_name = self._get_user_info_from_auth0(self._token['access_token'])
        self._user_id = 'a' + hashlib.md5(self._user_name.encode()).hexdigest()

    @property
    def whoami(self):
        return self._user_name

    @property
    def service(self):
        return f"{self._api_url}:{self._api_port}{self._api_prefix}"

    def _get_token_for_client(self) -> dict:
        try:
            token = requests.post("https://edc.eu.auth0.com/oauth/token",
                                  json={
                                      "client_id": self._auth_client_id,
                                      "client_secret": self._auth_client_secret,
                                      "audience": self._auth_aud,
                                      "grant_type": "client_credentials"
                                  })

            token.raise_for_status()
            return token.json()
        except BaseException as e:
            raise str(e)

    def _get_user_info_from_auth0(self, token: str):
        endpoint = "https://edc.eu.auth0.com/userinfo"
        headers = {'Authorization': 'Bearer %s' % token}

        req = requests.get(endpoint, headers=headers)

        req.raise_for_status()

        return req.json()

    def create(self, cfg: JsonObject) -> dict:
        """

        :param cfg:
        :return:
        """

        print("accessing", f"{self._api_url}:{self._api_port}{self._api_prefix}/jobs/{self._user_id}")

        res = requests.put(f"{self._api_url}:{self._api_port}{self._api_prefix}/jobs/{self._user_id}",
                           headers={"Authorization": f"Bearer {self._token['access_token']}"},
                           json=cfg)

        if res.status_code == 404:
            return {'message': 'User not found'}

        res.raise_for_status()

        return res.json()

    def delete(self, job_id: str) -> Union[AnyDict, Error]:
        """

        :param user_id:
        :param job_id:
        :return:
        """

        res = requests.delete(f"{self._api_url}:{self._api_port}/jobs/{self._user_id}/{job_id}", headers={
            "Authorization": f"Bearer {self._token['access_token']}"
        })

        if res.status_code == 404:
            return {'message': 'Job not found'}
        res.raise_for_status()

        return res.json()

    def list(self) -> JsonObject:
        """

        :param user_id:
        :return:
        """

        res = requests.get(f"{self._api_url}:{self._api_port}/jobs/{self._user_id}", headers={
            "Authorization": f"Bearer {self._token['access_token']}"
        })

        if res.status_code == 404:
            return {'message': 'User not found'}
        res.raise_for_status()

        return res.json()

    def status(self, job_id: str) -> AnyDict:
        """

        :param user_id:
        :param job_id:
        :return:
        """

        res = requests.get(f"{self._api_url}:{self._api_port}/jobs/{self._user_id}/{job_id}", headers={
            "Authorization": f"Bearer {self._token['access_token']}"
        })

        if res.status_code == 404:
            return {'message': 'Job not found'}
        res.raise_for_status()
        return res.json()

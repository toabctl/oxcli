# -*- coding: utf-8 -*-
#
# Copyright 2016 Thomas Bechtold <thomasbechtold@jpberlin.de>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import requests


class OxCliSessionException(Exception):
    pass


class OxCliSession(object):
    def __init__(self, base_url, username, password):
        self._base_url = base_url
        self._api_url = "/ajax"
        self._url = self._base_url + self._api_url
        self._username = username
        self._password = password
        self._cookies = None
        self._session_id = None

    def request(self, verb, url, kwargs):
        # do a login
        # TODO(toabctl): check also if current session expired
        if not self._session_id:
            self.login()

        # update data with the session_id
        if verb.lower() in ("get"):
            params = kwargs.get("params", {})
            params.update({"session": self._session_id})
            kwargs["params"] = params
        else:
            data = kwargs.get("data", {})
            data.update({"session": self._session_id})
            kwargs["data"] = data

        method = getattr(requests, verb.lower())
        url = self._url + url

        response = method(url, cookies=self._cookies, **kwargs)
        if response.status_code == 200:
            return response
        else:
            raise OxCliSessionException("[%s] url '%s'" % (
                response.satus_code, url)
            )

    def login(self):
        d = {
            "action": "login",
            "name": self._username,
            "password": self._password
        }
        r = requests.post(self._url + "/login", data=d)
        if r.status_code == 200:
            self._cookies = r.cookies
            self._session_id = r.json()["session"]
        else:
            raise OxCliSessionException("[%s] login failed: %s" % (
                r.status_code, r.text)
            )

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

from collections import namedtuple

from cliff.lister import Lister

from oxcli.common import folder_list


def contacts_list(session):
    """list contacts from all available folders"""
    headers = ["id", "name", "email1", "birthday"]
    ContactsList = namedtuple("ContactsList", headers)

    args = {
        "action": "all",
        "columns": "1,500,555,511"  # id, display_name,email1,birthday
    }
    r = session.request("get", "/contacts", {"params": args})
    return (headers,
            [ContactsList._make(contact) for contact in r.json()["data"]])


class ContactsFolderList(Lister):

    def take_action(self, parsed_args):
        return folder_list(self.app._session, "contacts")


class ContactsList(Lister):

    def take_action(self, parsed_args):
        return contacts_list(self.app._session)

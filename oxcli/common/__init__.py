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


def folder_list(session, content_type):
    """list folders for the given content type"""
    headers = ["id", "title"]
    FolderList = namedtuple("FolderList", headers)
    args = {
        "action": "allVisible",
        "content_type": content_type,
        "columns": "1,300"  # id, title
    }
    r = session.request("get", "/folders", {"params": args})
    for visibility, folders in r.json()["data"].items():
        return (headers,
                [FolderList._make(folder) for folder in folders])

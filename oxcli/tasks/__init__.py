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


def tasks_list(session):
    """list tasks from all available folders"""
    headers = ["id", "folder", "title", "last_modified"]
    TasksList = namedtuple("TasksList", headers)
    # get all folders
    _, tasks_folder_list = folder_list(session, "tasks")

    tasks = []
    for tasks_folder in tasks_folder_list:
        args = {
            "action": "all",
            "folder": tasks_folder.id,
            "columns": "1,200,5"  # id, folder
        }
        r = session.request("get", "/tasks", {"params": args})
        for task in r.json()["data"]:
            # add the folder name to the right position
            task.insert(1, tasks_folder.title)
            tasks.append(TasksList._make(task))
    return (headers, tasks)


class TasksFolderList(Lister):

    def take_action(self, parsed_args):
        return folder_list(self.app._session, "tasks")


class TasksList(Lister):

    def take_action(self, parsed_args):
        return tasks_list(self.app._session)

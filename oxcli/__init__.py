#!/usr/bin/python
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

from __future__ import print_function

import argparse
from collections import namedtuple
import os
import sys

from config import config_get
from session import OxCliSession

from tabulate import tabulate


# path to the user configuration file
USER_CONFIG_PATH = os.path.expanduser('~/.oxcli.ini')


def folder_list(session, content_type):
    """list folders for the given content type"""
    FolderList = namedtuple("FolderList", ["id", "title"])
    args = {
        "action": "allVisible",
        "content_type": content_type,
        "columns": "1,300"
    }
    r = session.request("get", "/folders", {"params": args})
    for visibility, folders in r.json()["data"].items():
        return [FolderList._make(folder) for folder in folders]


def tasks_list(session):
    """list tasks from all available folders"""
    TasksList = namedtuple("TasksList", ["id", "folder", "title",
                                         "last_modified"])
    # get all folders
    tasks_folder_list = folder_list(session, "tasks")

    tasks = []
    for tasks_folder in tasks_folder_list:
        args = {
            "action": "all",
            "folder": tasks_folder.id,
            "columns": "1,200,5"
        }
        r = session.request("get", "/tasks", {"params": args})
        for task in r.json()["data"]:
            # add the folder name to the right position
            task.insert(1, tasks_folder.title)
            tasks.append(TasksList._make(task))
    return tasks


def parse_tasks(args, session):
    """parse command line arguments for subcommand 'tasks'"""
    if args["folder_list"]:
        folders = folder_list(session, "tasks")
        print(tabulate(folders, headers="keys"))
        sys.exit(0)
    elif args["list"]:
        tasks = tasks_list(session)
        print(tabulate(tasks, headers="keys"))
        sys.exit(0)
    else:
        sys.exit(1)


def parse_args():
    """parse command line arguments"""
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='commands')

    # tasks parser
    parser_tasks = subparsers.add_parser('tasks',
                                         help='tasks related commands')
    parser_tasks.add_argument('--folder-list', action='store_true',
                              help='list task folders')
    parser_tasks.add_argument('--list', action='store_true',
                              help='list tasks')
    parser_tasks.set_defaults(func=parse_tasks)

    return vars(parser.parse_args())


def main():
    """main entry point"""
    args = parse_args()

    # get/create a config
    conf = config_get(USER_CONFIG_PATH)
    # create a session
    s = OxCliSession(conf['url'], conf['user'], conf['password'])
    # do something useful now!
    args["func"](args, s)


# useful for debugging
if __name__ == "__main__":
    main()

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

import logging
import os
import sys

from config import config_get
from session import OxCliSession

from cliff.app import App
from cliff.commandmanager import CommandManager

from oxcli import version

# path to the user configuration file
USER_CONFIG_PATH = os.path.expanduser('~/.oxcli.ini')


class OxCliApp(App):

    def __init__(self):
        super(OxCliApp, self).__init__(
            description='command line client for Open-Xchange',
            version=version.version_string(),
            command_manager=CommandManager('oxcli.cmds'),
            deferred_help=True,
        )
        self._config = None
        self._session = None

    def initialize_app(self, argv):
        self.LOG.debug('initialize_app')
        logging.getLogger("requests").setLevel(logging.WARNING)
        self._config = config_get(USER_CONFIG_PATH)
        self._session = OxCliSession(self._config['url'],
                                     self._config['user'],
                                     self._config['password'])
        self.LOG.debug('config and session ready')

    def prepare_to_run_command(self, cmd):
        self.LOG.debug('prepare_to_run_command %s', cmd.__class__.__name__)

    def clean_up(self, cmd, result, err):
        self.LOG.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            self.LOG.debug('got an error: %s', err)


def main(argv=sys.argv[1:]):
    """main entry point"""
    app = OxCliApp()
    return app.run(argv)


# useful for debugging
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

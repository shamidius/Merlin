#
# Copyright (c) 2015 EPAM Systems, Inc. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright notice, this
# list of conditions and the following disclaimer in the documentation and/or
# other materials provided with the distribution.
# Neither the name of the EPAM Systems, Inc. nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# See the NOTICE file and the LICENSE file distributed with this work
# for additional information regarding copyright ownership and licensing.
#

import threading
import time
import os

import unittest2
from unittest2.case import skipUnless
from merlin.common.test_utils import has_command

from merlin.tools.flume import Flume
import merlin.common.shell_command_executor as shell

PORT = 41414

TIME_TO_OPEN_PORT = 60


class AgentThread(threading.Thread):
    def run(self):
        Flume.agent(agent="a1",
                    conf_file=os.path.join(os.path.dirname(__file__),
                                           'resources/flume/flume.conf')).run()


@skipUnless(has_command('flume-ng') and has_command('netstat'), "flume-ng and netstat clients should be installed ")
class TestFlume(unittest2.TestCase):
    def setUp(self):
        super(TestFlume, self).setUp()
        shell.execute_shell_command('fuser -k -n tcp {0}'.format(PORT))

    def test_agent(self):
        thread = AgentThread()
        thread.daemon = True
        thread.start()
        time.sleep(TIME_TO_OPEN_PORT)
        cmd = shell.execute_shell_command('netstat -lntu')
        self.assertTrue("41414" in cmd.stdout, cmd.stdout)

    def tearDown(self):
        shell.execute_shell_command('fuser -k -n tcp {0}'.format(PORT))

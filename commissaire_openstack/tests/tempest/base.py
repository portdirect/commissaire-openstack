#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from oslo_log import log
from tempest import config
from tempest import test

CONF = config.CONF
lOG = log.getLogger(__name__)


class BaseCommissaire_OpenstackTest(test.BaseTestCase):

    credentials = ['primary']

    @classmethod
    def skip_checks(cls):
        super(BaseCommissaire_OpenstackTest, cls).skip_checks()
        if not CONF.service_available.commissaire_openstack:
            skip_msg = 'Commissaire_Openstack is disabled'
            raise cls.skipException(skip_msg)

    @classmethod
    def setup_clients(cls):
        super(BaseCommissaire_OpenstackTest, cls).setup_clients()
        pass

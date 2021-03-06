#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


import os

from oslo_config import cfg
from tempest.test_discover import plugins

from ironic_inspector.test.inspector_tempest_plugin import config


class InspectorTempestPlugin(plugins.TempestPlugin):
    def load_tests(self):
        base_path = os.path.split(os.path.dirname(
            os.path.abspath(__file__)))[0]
        test_dir = "inspector_tempest_plugin/tests"
        full_test_dir = os.path.join(base_path, test_dir)
        return full_test_dir, base_path

    def register_opts(self, conf):
        conf.register_opt(config.service_option,
                          group='service_available')
        conf.register_group(config.baremetal_introspection_group)
        conf.register_opts(config.BaremetalIntrospectionGroup,
                           group="baremetal_introspection")
        if os.path.exists('/tmp/ironic-inspector-grenade'):
            # FIXME(dtantsur): pretend like Neutron does not exist due to
            # random failures, see https://bugs.launchpad.net/bugs/1621791.
            cfg.CONF.set_override('neutron', False, 'service_available')

    def get_opt_lists(self):
        return [
            (config.baremetal_introspection_group.name,
             config.BaremetalIntrospectionGroup),
            ('service_available', [config.service_option])
        ]

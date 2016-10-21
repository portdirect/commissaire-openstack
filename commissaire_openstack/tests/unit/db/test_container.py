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

"""Tests for manipulating Containers via the DB API"""
from oslo_utils import uuidutils
import six

from commissaire_openstack.common import exception
from commissaire_openstack.tests.unit.db import base
from commissaire_openstack.tests.unit.db import utils


class DbContainerTestCase(base.DbTestCase):

    def test_create_container(self):
        utils.create_test_container()

    def test_create_container_already_exists(self):
        utils.create_test_container()
        self.assertRaises(exception.ResourceExists,
                          utils.create_test_container)

    def test_get_container_by_id(self):
        container = utils.create_test_container()
        res = self.dbapi.get_container_by_id(self.context, container.id)
        self.assertEqual(container.id, res.id)
        self.assertEqual(container.uuid, res.uuid)

    def test_get_container_by_uuid(self):
        container = utils.create_test_container()
        res = self.dbapi.get_container_by_uuid(self.context,
                                               container.uuid)
        self.assertEqual(container.id, res.id)
        self.assertEqual(container.uuid, res.uuid)

    def test_get_container_by_name(self):
        container = utils.create_test_container()
        res = self.dbapi.get_container_by_name(self.context,
                                               container.name)
        self.assertEqual(container.id, res.id)
        self.assertEqual(container.uuid, res.uuid)

    def test_get_container_that_does_not_exist(self):
        self.assertRaises(exception.ContainerNotFound,
                          self.dbapi.get_container_by_id, self.context, 99)
        self.assertRaises(exception.ContainerNotFound,
                          self.dbapi.get_container_by_uuid,
                          self.context,
                          uuidutils.generate_uuid())

    def test_list_container(self):
        uuids = []
        for i in range(1, 6):
            container = utils.create_test_container(
                uuid=uuidutils.generate_uuid())
            uuids.append(six.text_type(container['uuid']))
        res = self.dbapi.list_container(self.context)
        res_uuids = [r.uuid for r in res]
        self.assertEqual(sorted(uuids), sorted(res_uuids))

    def test_list_container_sorted(self):
        uuids = []
        for _ in range(5):
            container = utils.create_test_container(
                uuid=uuidutils.generate_uuid())
            uuids.append(six.text_type(container.uuid))
        res = self.dbapi.list_container(self.context, sort_key='uuid')
        res_uuids = [r.uuid for r in res]
        self.assertEqual(sorted(uuids), res_uuids)

        self.assertRaises(exception.InvalidParameterValue,
                          self.dbapi.list_container,
                          self.context,
                          sort_key='foo')

    def test_list_container_with_filters(self):
        container1 = utils.create_test_container(
            name='container-one',
            uuid=uuidutils.generate_uuid())
        container2 = utils.create_test_container(
            name='container-two',
            uuid=uuidutils.generate_uuid())

        res = self.dbapi.list_container(self.context,
                                        filters={'name': 'container-one'})
        self.assertEqual([container1.id], [r.id for r in res])

        res = self.dbapi.list_container(self.context,
                                        filters={'name': 'container-two'})
        self.assertEqual([container2.id], [r.id for r in res])

        res = self.dbapi.list_container(self.context,
                                        filters={'name': 'bad-container'})
        self.assertEqual([], [r.id for r in res])

        res = self.dbapi.list_container(
            self.context,
            filters={'name': container1.name})
        self.assertEqual([container1.id], [r.id for r in res])

    def test_destroy_container(self):
        container = utils.create_test_container()
        self.dbapi.destroy_container(container.id)
        self.assertRaises(exception.ContainerNotFound,
                          self.dbapi.get_container_by_id,
                          self.context, container.id)

    def test_destroy_container_by_uuid(self):
        container = utils.create_test_container()
        self.dbapi.destroy_container(container.uuid)
        self.assertRaises(exception.ContainerNotFound,
                          self.dbapi.get_container_by_uuid,
                          self.context, container.uuid)

    def test_destroy_container_that_does_not_exist(self):
        self.assertRaises(exception.ContainerNotFound,
                          self.dbapi.destroy_container,
                          uuidutils.generate_uuid())

    def test_update_container(self):
        container = utils.create_test_container()
        old_image = container.image
        new_image = 'new-image'
        self.assertNotEqual(old_image, new_image)

        res = self.dbapi.update_container(container.id,
                                          {'image': new_image})
        self.assertEqual(new_image, res.image)

    def test_update_container_not_found(self):
        container_uuid = uuidutils.generate_uuid()
        new_image = 'new-image'
        self.assertRaises(exception.ContainerNotFound,
                          self.dbapi.update_container,
                          container_uuid, {'image': new_image})

    def test_update_container_uuid(self):
        container = utils.create_test_container()
        self.assertRaises(exception.InvalidParameterValue,
                          self.dbapi.update_container, container.id,
                          {'uuid': ''})

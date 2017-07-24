# coding: utf-8
# Copyright © 2017-2019 Zuercher Hochschule fuer Angewandte Wissenschaften.
# All Rights Reserved.
#
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

from __future__ import absolute_import

# from six import BytesIO
from flask import json

# from esm.models.catalog import Catalog
# from esm.models.empty import Empty
# from esm.models.error import Error
from esm.models.plan import Plan
from esm.models.manifest import Manifest
from esm.models.service_type import ServiceType
from . import BaseTestCase

from adapters.log import LOG
from adapters.datasource import STORE


class TestCatalogController(BaseTestCase):
    """ CatalogController integration test stubs """

    def setUp(self):
        super().setUp()
        self.test_plan = Plan(
            id='testplan', name='testing plan', description='plan for testing',
            metadata=None, free=True, bindable=False
        )
        self.test_service = ServiceType(
            id='test', name='test_svc',
            description='this is a test service',
            bindable=False,
            tags=['test', 'tester'],
            metadata=None, requires=[],
            plan_updateable=False, plans=[self.test_plan],
            dashboard_client=None)

        self.test_manifest = Manifest(
            id='test', plan_id=self.test_plan.id, service_id=self.test_service.id,
            manifest_type='dummy', manifest_content=''
        )

    def tearDown(self):
        super().tearDown()
        store = STORE
        store.delete_service()
        store.delete_manifest()

    def test_catalog(self):
        """
        Test case for catalog

        Gets services registered within the broker
        """
        headers = [('X_Broker_Api_Version', '2.12')]
        response = self.client.open('/v2/catalog',
                                    method='GET',
                                    headers=headers)
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_register_service(self):
        """
        Test case for register_service

        Registers the service with the catalog.
        """
        headers = [('X_Broker_Api_Version', '2.12')]
        LOG.debug('Sending service registration content of:\n {content}'.format(content=json.dumps(self.test_service)))
        response = self.client.open('/v2/et/catalog',
                                    method='PUT',
                                    data=json.dumps(self.test_service),
                                    content_type='application/json',
                                    headers=headers)
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_store_manifest(self):
        """
        Test case for store_manifest

        takes deployment description of a software service and associates with a service and plan
        """
        headers = [('X_Broker_Api_Version', '2.12')]
        LOG.debug('Sending service registration content of:\n {content}'.format(content=json.dumps(self.test_service)))
        response = self.client.open('/v2/et/catalog',
                                    method='PUT',
                                    data=json.dumps(self.test_service),
                                    content_type='application/json',
                                    headers=headers)
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

        headers = [('X_Broker_Api_Version', '2.12')]
        LOG.debug('Sending service registration content of:\n {content}'.format(content=json.dumps(self.test_manifest)))
        response = self.client.open('/v2/et/manifest/{manifest_id}'.format(manifest_id=self.test_manifest.id),
                                    method='PUT',
                                    data=json.dumps(self.test_manifest),
                                    content_type='application/json',
                                    headers=headers)
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
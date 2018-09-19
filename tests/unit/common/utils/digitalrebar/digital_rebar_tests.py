# Copyright 2017 ARICENT HOLDINGS LUXEMBOURG SARL and Cable Television
# Laboratories, Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import unittest
import json

from snaps_boot.provision.hardware.digitalrebar.digital_rebar import DigitalRebar


class DigitalRebarTests(unittest.TestCase):
    """
    Tests for functions located in digital_rebar
    """

    def test_authorize(self):
        r = DigitalRebar('rocketskates', 'r0cketsk8ts', 'https://10.197.113.165:8092')
        r.authorize()
        self.assertTrue(r.isAuthorized())

    def test_post_subnet(self):
        r = DigitalRebar('rocketskates', 'r0cketsk8ts', 'https://10.197.113.165:8092')
        r.authorize()
        self.assertTrue(r.isAuthorized())

        result = r.delete('subnets', 'ens5')

        body  = {u'Available': True, u'Subnet': u'10.1.1.10/24', u'Errors': [], u'Name': u'ens5', u'Pickers': [u'hint', u'nextFree', u'mostExpired'], u'OnlyReservations': False, u'Strategy': u'MAC', u'ActiveLeaseTime': 60, u'Documentation': u'', u'Enabled': True, u'Options': [{u'Code': 3, u'Value': u'10.1.1.10'}, {u'Code': 6, u'Value': u'10.1.1.10'}, {u'Code': 15, u'Value': u'openstacklocal'}, {u'Code': 1, u'Value': u'255.255.255.0'}, {u'Code': 28, u'Value': u'10.1.1.255'}], u'ReservedLeaseTime': 7200, u'ReadOnly': False, u'Meta': {}, u'ActiveEnd': u'10.1.1.254', u'Proxy': False, u'NextServer': u'', u'Unmanaged': False, u'Validated': True, u'ActiveStart': u'10.1.1.10', u'Description': u''}
        result = r.post('subnets', body)
        self.assertNotEqual(401, result)
        self.assertEqual(result['Name'], 'ens5')
        self.assertEqual(result['Subnet'], '10.1.1.10/24')

        result = r.get('subnets')
        self.assertNotEqual(401, result)
        self.assertEqual(2, len(result))

        result = r.get('subnets', 'ens4')
        self.assertNotEqual(401, result)
        self.assertEqual(result['Name'], 'ens4')
        self.assertEqual(result['Subnet'], '10.1.0.10/24')

        result = r.get('subnets', 'ens5')
        self.assertNotEqual(401, result)
        self.assertEqual(result['Name'], 'ens5')
        self.assertEqual(result['Subnet'], '10.1.1.10/24')

        result = r.delete('subnets', 'ens5')
        self.assertEqual(result['Name'], 'ens5')
        self.assertEqual(result['Subnet'], '10.1.1.10/24')



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


import requests
import urllib3

urllib3.disable_warnings()

class DigitalRebar:
    def __init__(self, username, password, url):
        self.username = username
        self.password = password
        self.url = url
        self.token = ''

    def authorize(self):
        r = requests.get(self.url + '/api/v3/users/rocketskates/token?ttl=28800', auth=(self.username, self.password), verify=False)
        if (r.status_code == 200):
            body = r.json()
            self.token = body['Token']
        else:
            print 'Failed Authorizing ' + str(r.status_code)

    def isAuthorized(self):
        return self.token != ''

    def get(self, resource, id=None):
        if not self.isAuthorized():
            self.authorize()
        headers = {'Authorization': 'Bearer ' + self.token}
        actualResource = resource
        if id != None:
            actualResource = actualResource + '/' + id
        r = requests.get(self.url + '/api/v3/' + actualResource, headers=headers, verify=False)
        if r.status_code == 200:
            return r.json()
        else:
            print 'Error on Get ' + str(r.status_code)
            print r.json()
            return r.status_code

    def post(self, resource, body):
        if not self.isAuthorized():
            self.authorize()
        headers = {'Authorization': 'Bearer ' + self.token}
        actualResource = resource
        r = requests.post(self.url + '/api/v3/' + actualResource, headers=headers, json=body, verify=False)
        if r.status_code == 201:
            return r.json()
        else:
            print 'Error on Post ' + str(r.status_code)
            print r.json()
            return r.status_code

    def delete(self, resource, id):
        if not self.isAuthorized():
            self.authorize()
        headers = {'Authorization': 'Bearer ' + self.token}
        actualResource = resource + '/' + id
        r = requests.delete(self.url + '/api/v3/' + actualResource, headers=headers, verify=False)
        if r.status_code == 200:
            return r.json()
        else:
            print 'Error on Delete ' + str(r.status_code)
            print r.json()
            return r.status_code




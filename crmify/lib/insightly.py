from json.decoder import JSONDecodeError
import os
import requests
import base64


class Insightly(object):
    base_url = 'https://api.insight.ly/'

    def __init__(self, version='v2.2', api_key=None):
        self.version = version
        self.api_key = api_key

    def get_url(self, path):
        return self.base_url + self.version + path

    def make_request(self, path, method='GET', **args):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic ' + str(base64.b64encode(self.api_key.encode('ascii')), encoding='ascii')
        }

        resp = requests.request(method, self.get_url(path), headers=headers, **args)

        if not resp.ok:
            resp.raise_for_status()

        try:
            return resp.json()
        except JSONDecodeError:
            return resp.content

    def read(self, resource, **args):
        return self.make_request('/' + resource, **args)

    def update(self, resource, data):
        return self.make_request('/' + resource, method='PUT', json=data)

    def create(self, resource, data):
        return self.make_request('/' + resource, method='POST', json=data)

    def delete(self, resource, id):
        return self.make_request('/' + os.path.join(resource, id), method='DELETE')
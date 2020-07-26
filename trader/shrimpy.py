import base64
import hashlib
import hmac
import requests
import time

from django.conf import settings


class Shrimpy:

    __instance = None

    @staticmethod
    def get_shrimpy_instance():
        if Shrimpy.__instance is None:
            return Shrimpy()
        return Shrimpy.__instance

    def __init__(self):
        if Shrimpy.__instance is not None:
            raise Exception('Shrimpy uses Singleton design pattern')
        self.api_key = settings.SHRIMPY_API_KEY
        self.secret_key = settings.SHRIMPY_SECRET_KEY
        self.nonce = int(time.time() * 1000)
        self.base_url = 'https://dev-api.shrimpy.io'
        self.headers = {
            'Content-Type': 'application/json',
            'DEV-SHRIMPY-API-KEY': self.api_key,
            'DEV-SHRIMPY-API-NONCE': str(self.nonce),
            }

        Shrimpy.__instance = self

    def assign_signature_to_header(self, method, request_path, body=''):
        prehash_string = ''.join([request_path, method, str(self.nonce), body])
        secret_key = base64.b64decode(self.secret_key)
        prehash_string = prehash_string.encode('ascii')
        signature = hmac.new(secret_key, prehash_string, hashlib.sha256)
        signature_b64 = base64.b64encode(signature.digest()).decode('utf-8')
        self.headers['DEV-SHRIMPY-API-SIGNATURE'] = signature_b64

    def get_supported_exchanges(self):
        method = 'GET'
        request_path = '/v1/list_exchanges'
        self.assign_signature_to_header(method, request_path)
        request = requests.get(f'{self.base_url}{request_path}', headers=self.headers)
        return request

    def get_ticker(self, exchange):
        method = 'GET'
        request_path = f'/v1/exchanges/{exchange}/ticker'
        self.assign_signature_to_header(method, request_path)
        request = requests.get(f'{self.base_url}{request_path}', headers=self.headers)
        return request








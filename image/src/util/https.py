from dataclasses import dataclass
from typing import Union
import requests

@dataclass
class Response:
    status: int
    body: Union[dict, list]

@dataclass
class HttpClient:
    base: str
    headers: dict
    
    def get(self, endpoint, headers={}, params={}):
        return self.request('GET', endpoint, headers=headers, params=params)

    def post(self, endpoint, body=None, headers={}, params={}, files={}):
        return self.request('POST', endpoint, body=body, headers=headers, params=params, files=files)

    def put(self, endpoint, body=None, headers={}, params={}):
        return self.request('PUT', endpoint, body=body, headers=headers, params=params)

    def delete(self, endpoint, headers={}, params={}):
        return self.request('DELETE', endpoint, headers=headers, params=params)
    
    def patch(self, endpoint, body=None, headers={}, params={}):
        return self.request('PATCH', endpoint, body=body, headers=headers, params=params)

    def request(self, method, endpoint, body=None, headers={}, params={}, files={}):
        url = f'{self.base}{endpoint}'

        headers = self.headers | headers

        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            json=body,
            files=files,
        )
        status = response.status_code

        try:
            body = response.json()
        except ValueError:
            body = response.text
            
        return Response(status, body)
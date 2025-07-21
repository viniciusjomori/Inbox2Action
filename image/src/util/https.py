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

    def post(self, endpoint, headers={}, params={}, body=None, files={}):
        return self.request('POST', endpoint, headers=headers, params=params, body=body, files=files)

    def put(self, endpoint, headers={}, params={}, body=None):
        return self.request('PUT', endpoint, headers=headers, params=params, body=body)

    def delete(self, endpoint, headers={}, params={}):
        return self.request('DELETE', endpoint, headers=headers, params=params)
    
    def patch(self, endpoint, headers={}, params={}, body=None):
        return self.request('PATCH', endpoint, headers=headers, params=params, body=body)

    def request(self, method, endpoint, headers={}, params={}, body=None, files={}):
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
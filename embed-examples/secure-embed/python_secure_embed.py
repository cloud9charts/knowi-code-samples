"""
generate a secure embed dashboard using the Management API
"""

import json
from typing import List

import requests

host = 'https://www.knowi.com/api/1.0'
knowi_client_id = 'fsdfad12323nln12'  # update client id
knowi_client_secret = 'fsdfad12323nln12'  # update client secret
user_content_filter = [{"fieldName": "team", "values": ["Facebook"], "operator": "="}]  # update content filter to hash
knowi_dash_id = 123456  # update with dashboard (or widget) ID to embed


class Knowi:
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        rsp = requests.post(host + '/login',
                            data={'client_id':     self.client_id,
                                  'client_secret': self.client_secret}).json()

        self.auth_header = {'Authorization': f"Bearer {rsp.get('access_token')}"}

    def dashboard_secure_url(self, dash_id: int, content_filter: List[dict]):
        rsp = requests.post(host + f'/dashboards/{dash_id}/share/url/secure',
                            headers=self.auth_header,
                            data={"contentFilters": json.dumps(content_filter)})
        if rsp.ok:
            print(rsp.json())


def run():
    k = Knowi(knowi_client_id, knowi_client_secret)
    k.dashboard_secure_url(knowi_dash_id, user_content_filter)


run()

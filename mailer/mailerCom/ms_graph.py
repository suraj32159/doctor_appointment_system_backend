import json
import logging
from abc import ABC

import environ
import requests

logger = logging.getLogger(__name__)

env = environ.Env()
environ.Env.read_env()

GRAPH_BASE_URL = "https://graph.microsoft.com/v1.0"

DEFAULT = "default"
SCOPES = {DEFAULT: "https://graph.microsoft.com/.default"}

ME = "me"
APPLICATION = "application"
# TODO: change email address here once production credentials are received
TENANTS = {ME: "/me", APPLICATION: "/users/ziena@adnhcompassme.com"}

SEND_MAIL = "sendMail"
ENDPOINTS = {SEND_MAIL: "/sendMail"}


class Auth2Utils(ABC):
    def _get_access_token(self):
        data = {
            "grant_type": "client_credentials",
            "client_id": env.str("auth2_client_id"),
            "scope": SCOPES[DEFAULT],
            "client_secret": env.str("auth2_client_secret"),
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded", "Accept": "*/*"}
        files = []

        tenant_id = env.str("auth2_tenant_id")
        response = requests.post(
            url=f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token",
            json=data,
            data=data,
            headers=headers,
            files=files,
        )
        token = json.loads(response.text).get("access_token")
        return token

    def get_headers(self):
        access_token = self._get_access_token()
        return {
            "Content-Type": "application/json",
            "Accept": "*/*",
            "Authorization": f"Bearer {access_token}",
        }


class Auth2MailerMixin(Auth2Utils):
    def sendMailAsSignedInUser(self, message):
        tenant = TENANTS[ME]
        endpoint = ENDPOINTS[SEND_MAIL]
        url = f"{GRAPH_BASE_URL}{tenant}{endpoint}"
        headers = self.get_headers()
        data = json.dumps(message)
        response = requests.post(url, headers=headers, data=data)
        return response

    def sendMailAsApplication(self, message):
        tenant = TENANTS[APPLICATION]
        endpoint = ENDPOINTS[SEND_MAIL]
        url = f"{GRAPH_BASE_URL}{tenant}{endpoint}"
        headers = self.get_headers()
        response = requests.post(url, headers=headers, data=message)
        return response

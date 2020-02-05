import os

from dotenv import load_dotenv
import requests

load_dotenv()

HOST = "https://knowi.com"
KNOWI_CUSTOMER_TOKEN = os.environ.get("KNOWI_CUSTOMER_TOKEN")  # update with Knowi Customer Token
EMAIL = 'email@company.com'  # email of single sign on user to create


class Knowi:
    def __init__(self, customer_token):
        self.customer_token = customer_token

    def create_sso_user(self, *, email):
        """ create sso user token for existing/new user """
        payload = {"user":             email,
                   "ssoCustomerToken": self.customer_token}
        rsp = requests.post(HOST + '/sso/user/create', data=payload)
        if rsp.ok:
            user_token = rsp.text
            print(f'*** NEW SSO USER TOKEN CREATED: {user_token} ***')

            return user_token

    @staticmethod
    def create_user_session(*, email, user_token):
        """ initiate sso user session """
        payload = {"user":      email,
                   "userToken": user_token}
        rsp = requests.post(HOST + '/sso/session/create', data=payload)
        if rsp.ok:
            session_token = rsp.text
            login_url = f"{HOST}/sso/user/login?token={session_token}"
            print(f'*** NEW SSO USER SESSION CREATED: {session_token} ***')

            return login_url


def run():
    knowi = Knowi(customer_token=KNOWI_CUSTOMER_TOKEN)
    user = knowi.create_sso_user(email=EMAIL)
    session = knowi.create_user_session(email=EMAIL, user_token=user)

    print(session)


run()

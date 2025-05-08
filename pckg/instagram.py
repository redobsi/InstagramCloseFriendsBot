import requests
import uuid
import json
import random
import time
from urllib.parse import urlencode


def regex_extract(string, pattern):
    import re
    matches = re.findall(pattern, string)
    return [match for match in matches if match != '']


def random_string(length):
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    return ''.join(random.choice(characters) for _ in range(length))


def get_timestamp():
    return str(int(time.time()))


def generate_headers(extra_headers=None):
    if extra_headers is None:
        extra_headers = {}

    headers = {
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'i.instagram.com',
        'ig-intended-user-id': '0',
        'User-Agent': 'Instagram 361.0.0.46.88 Android (30/11; 418dpi; 1080x2215; Genymobile/Samsung; Galaxy S24; vbox86p; vbox86; en_US; 674674763)',
        'x-bloks-is-layout-rtl': 'false',
        'X-Bloks-Prism-AX-Base-Colors-Enabled': 'false',
        'X-Bloks-Prism-Button-Version': 'INDIGO_PRIMARY_BORDERED_SECONDARY',
        'X-Bloks-Prism-Colors-Enabled': 'true',
        'X-Bloks-Prism-Font-Enabled': 'false',
        'x-bloks-version-id': '16e9197b928710eafdf1e803935ed8c450a1a2e3eb696bff1184df088b900bcf',
        'x-fb-client-ip': 'True',
        'X-FB-Connection-Type': 'MOBILE.LTE',
        'X-FB-HTTP-Engine': 'Liger',
        'x-fb-server-cluster': 'True',
        'x-ig-app-id': '567067343352427',
        'x-ig-app-locale': 'en_US',
        'X-IG-Attest-Params': '{"attestation":[{"version":2,"type":"keystore","errors":[-1013],"challenge_nonce":"","signed_nonce":"","key_hash":""}]}',
        'x-ig-bandwidth-speed-kbps': '-1.000',
        'x-ig-bandwidth-totalbytes-b': '0',
        'x-ig-bandwidth-totaltime-ms': '0',
        'x-ig-capabilities': '3brTv10=',
        'x-ig-connection-type': 'MOBILE(LTE)',
        'x-ig-device-id': str(uuid.uuid4()),
        'x-ig-device-locale': 'en_US',
        'x-ig-family-device-id': str(uuid.uuid4()),
        'x-ig-mapped-locale': 'en_US',
        'x-ig-nav-chain': '',
        'x-ig-timezone-offset': '0',
        'x-ig-www-claim': '0',
        'x-pigeon-rawclienttime': get_timestamp(),
        'x-pigeon-session-id': f'UFS-{uuid.uuid4()}-0',
    }
    headers.update(extra_headers)
    return headers


class Bot:
    def __init__(self):
        self.values = {}

    def get_session(self):
        with open('session.json', 'r') as f:
            return json.load(f)

    def make_request(self, url, method, extra_headers=None, body=None):
        headers = generate_headers(extra_headers)
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers)
            else:
                response = requests.post(url, headers=headers, data=body)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print('Request failed:', e)
            if e.response:
                print('Response status code:', e.response.status_code)
                print('Response body:', e.response.text)

    def sign_in(self, username, password):
        android_id = f'android-{random_string(13)}'
        url = 'https://i.instagram.com/api/v1/bloks/async_action/com.bloks.www.bloks.caa.login.async.send_login_request/'

        headers = {
            'x-ig-android-id': android_id,
            'x-ig-nav-chain': f'com.bloks.www.caa.login.login_homepage:com.bloks.www.caa.login.login_homepage:1:button:{get_timestamp()}::'
        }

        client_input_params = {
            "contact_point": username,
            "password": f"#PWD_INSTAGRAM_BROWSER:0:&:{password}",
            "device_id": android_id,
            "login_attempt_count": 1,
            "try_num": 1,
            "family_device_id": str(uuid.uuid4()),
            "flash_call_permission_status": {
                "READ_PHONE_STATE": "DENIED",
                "READ_CALL_LOG": "DENIED",
                "ANSWER_PHONE_CALLS": "DENIED"
            },
            "accounts_list": [],
            "device_emails": [],
            "event_step": "home_page"
        }

        server_params = {
            "login_source": "Login",
            "waterfall_id": str(uuid.uuid4()),
            "device_id": str(uuid.uuid4()),
            "credential_type": "password",
            "username_text_input_id": "mg5hsu:98",
            "password_text_input_id": "mg5hsu:98"
        }

        params = json.dumps({
            "client_input_params": client_input_params,
            "server_params": server_params
        })

        bk_client_context = json.dumps({
            "bloks_version": "16e9197b928710eafdf1e803935ed8c450a1a2e3eb696bff1184df088b900bcf",
            "styles_id": "instagram"
        })

        bloks_versioning_id = "16e9197b928710eafdf1e803935ed8c450a1a2e3eb696bff1184df088b900bcf"

        body = urlencode({
            'params': params,
            'bk_client_context': bk_client_context,
            'bloks_versioning_id': bloks_versioning_id
        })

        response = self.make_request(url, 'POST', headers, body)
        if not response:
            return {"complete": False, "values": None}

        data = response.json()
        action = data.get("layout", {}).get("bloks_payload", {}).get("action", "")

        import re
        token_pattern = re.compile(r'Bearer\sIGT:[^\s]+')
        tokens = token_pattern.findall(action)

        if tokens:
            cleaned_tokens = [token.split('\\')[0] for token in tokens]
            www_claim = re.findall(r'hmac.\w+', action)
            user_id_match = re.search(r'"ig-set-ig-u-ds-user-id\\":\s*(\d+)', action)

            if www_claim:
                self.values['www_claim'] = www_claim[0]
            if user_id_match:
                self.values['ig_u_ds_user_id'] = user_id_match.group(1)

            self.values['token'] = cleaned_tokens[0]

            response = self.make_request(
                'https://i.instagram.com/api/v1/multiple_accounts/get_account_family/',
                'GET',
                {
                    'x-ig-nav-chain': headers['x-ig-nav-chain'],
                    'Authorization': self.values['token']
                }
            )

            self.values['ig_u_rur'] = response.headers.get('ig-set-ig-u-rur')
            self.values['ig_u_shbid'] = response.headers.get('ig-set-ig-u-shbid')
            self.values['ig_u_shbts'] = response.headers.get('ig-set-ig-u-shbts')
            self.values['android_id'] = android_id

            return {
                "complete": True,
                "values": self.values
            }
        else:
            return {
                "complete": False,
                "values": None
            }

    def add_close_friend(self, pk_id):
        session = self.get_session()
        url = f'https://i.instagram.com/api/v1/stories/private_stories/add_member/'
        headers = {
            'Authorization': session['token'],
            'ig_u_rur': session['ig_u_rur'],
            'x-ig-www-claim': session['www_claim'],
            'android_id': session['android_id']
        }

        body_object = {
            "_uuid": str(uuid.uuid4()),
            "source": "settings",
            "module": "audience_selection",
            "user_id": str(pk_id)
        }

        signed_body = urlencode(body_object)
        response = self.make_request(url, 'POST', headers, signed_body)
        return response.json() if response else None


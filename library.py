import requests
from auxiliary import Auxiliary
from config import *
import random


class Multilogin:

    def __init__(self, token, port):
        self.token = token
        self.port = port

    def get_uid_acc(self):
        headers = {
            'accept': 'application/json, text/plain, */*',
            'token': self.token,
        }
        response = requests.get(
            'https://app.multiloginapp.com/rest/v1/plans/current', headers=headers)

        result = response.json()
        return result['uid']

    def get_profiles(self):
        headers = {
            'accept': 'application/json, text/plain, */*',
            'token': self.token,
        }
        url = 'https://app.multiloginapp.com/clb/rest/v1/t/{uid}/m/{uid}/p'
        uid = self.get_uid_acc()
        valid_url = url.replace('{uid}', uid)
        response = requests.get(
            valid_url, headers=headers)

        return response.json()

    def get_profile_info(self, uuid):
        headers = {
            'accept': 'application/json, text/plain, */*',
            'token': self.token
        }
        json_data = {
            'sid': '00000000-0000-0000-0000-000000000000'
        }

        response = requests.post(f'http://127.0.0.1:{self.port}/clb/p/{uuid}',
            headers=headers, json=json_data)

        result = response.json()

        return {
            'name': result['name'],
            'notes': Auxiliary(result).get_notes(),
            'useragent': result['container']['navUserAgent'],
            'proxyEnabled': Auxiliary(result).get_proxy_enabled(),
            'proxy': Auxiliary(result).get_proxy(proxy_type=Auxiliary(result).get_proxy_type()),
            'googleServicesEnabled': result['googleServices'],
            'platform': Auxiliary(result).get_platform(),
            'language': result['container']['navigator']['langHdr'],
            'os': result['osType'],
            'fonts': result['fonts'],
            'cpu_cores': result['container']['navigator']['hardwareConcurrency'],
            'screen_resolution': f"{result['container']['scrWidth']}x{result['container']['scrHeight']}",
            'audio_inputs': result['mediaDevicesAudioInputs'],
            'video_inputs': result['mediaDevicesVideoInputs'],
            'audio_outputs': result['mediaDevicesAudioOutputs'],
            'webGLMetadata': Auxiliary(result).get_webGLMetadata()
        }


class GoLogin:
    def __init__(self, token):
        self.token = token

    def create_profile(self, data):
        headers = {
            'Authorization': 'Bearer ' + self.token,
            'User-Agent': 'Selenium-API'
        }

        json_data = {
            'name': data['name'],
            'notes': data['notes'],
            'browserType': 'chrome',
            'os': data['os'],
            'googleServicesEnabled': data['googleServicesEnabled'],
            'navigator': {
                'userAgent': data['useragent'],
                'resolution': data['screen_resolution'],
                'language': data['language'],
                'platform': data['platform'],
                'doNotTrack': False,
                'hardwareConcurrency': data['cpu_cores'],
                'deviceMemory': 1,
                'maxTouchPoints': 0,
            },
            'proxyEnabled': data['proxyEnabled'],
            # 'proxy': data['proxy'],
            'fonts': {
                'families': data['fonts'],
                'enableMasking': True,
                'enableDomRect': True
            },
            'mediaDevices': {
                'videoInputs': data['video_inputs'],
                'audioInputs': data['audio_inputs'],
                'audioOutputs': data['audio_outputs'],
                'enableMasking': False
            },
            'webGLMetadata': data['webGLMetadata'],
        }

        if json_data['proxyEnabled'] != False:
            json_data['proxy'] = data['proxy']

        response = requests.post('https://api.gologin.com/browser', headers=headers, json=json_data)

        return response

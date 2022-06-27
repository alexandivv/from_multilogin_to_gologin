import requests
from config import GOLOGIN_TOKEN


class Auxiliary:
    def __init__(self, result):
        self.result = result

    def get_notes(self):
        try:
            notes = self.result['notes']
            return notes
        except KeyError:
            notes = ''
            return notes

    def get_proxy_type(self):
        if self.result['proxyType'] == 0:
            proxy_type = 'no_proxy'
            return proxy_type
        elif self.result['proxyType'] == 1:
            proxy_type = 'http'
            return proxy_type
        elif self.result['proxyType'] == 2:
            proxy_type = 'socks4'
            return proxy_type
        elif self.result['proxyType'] == 3:
            proxy_type = 'socks5'
            return proxy_type
        elif self.result['proxyType'] == 5:
            proxy_type = 'ssh'
            return proxy_type

    def get_proxy_enabled(self):
        if self.result['proxyType'] == 0:
            return False
        else:
            return True

    def get_proxy(self, proxy_type):
        if proxy_type == 'no_proxy':
            return {}
        else:
            return {
                'mode': proxy_type,
                'host': self.result['proxyHost'],
                'port': self.result['proxyPort'],
                'username': self.result['proxyUser'],
                'password': self.result['proxyPass'],
            }

    def get_webGLMetadata(self):
        return {
            'mode': 'mask',
            'vendor': self.result['container']['webGlVendor'],
            'renderer': self.result['container']['webGlRenderer']
        }

    def get_platform(self):
        if self.result['osType'] == 'mac':
            platform = 'mac'
            return platform
        elif self.result['osType'] == 'win':
            platform = 'Win32'
            return platform
        elif self.result['osType'] == 'lin':
            platform = 'lin'

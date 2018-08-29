"""
Sensifai Python Client
"""

import os
import json
import logging
import requests

from http.client import HTTPSConnection

# Logging in console
logger = logging.getLogger('sensifai')
formatter = logging.Formatter('%(message)s')

logger.handlers = []
ch = logging.StreamHandler()
ch.setFormatter(formatter)

logger.addHandler(ch)
logger.setLevel(logging.DEBUG)

class ApiError(Exception):
    pass

class RestError(Exception):
    pass

class SensifaiApi(object):
    def __init__(self, token = None, host = None):
        """
        Initialize SensifaiApi

        Parameters
        ----------
        token : string
            to get your key visit https://developer.sensifai.com
        host : string
            default to https://api.sensifai.com unless you set
            SENSIFAI_API_BASE enviroment variable
        """

        if token:
            self.token = token
        else:
            self.token = os.environ.get("SENSIFAI_API_TOKEN", None)

        if not self.token:
            raise ApiError("Token is Required")

        if host:
            self.host = host
        else:
            self.host = os.environ.get("SENSIFAI_API_BASE", None)

        if not self.host:
            self.host = 'https://api.sensifai.com'

        self._user_agent = 'Sensifai Python Client'

    def video_by_file(self, file):
        if not isinstance(file, str):
            raise ApiError("File should be a path on your system")

        api = '/v1/upload_video'
        url = self.host + api
        files = {
            'file': (file.split('/')[-1], open(file, 'rb'))
        }
        headers = {
            "access_token": self.token
        }
        try:
            conn = requests.post(
                                    url,
                                    files = files,
                                    headers = headers
                                )
            logger.debug('HTTP Status Code: %d' % conn.status_code)
            if (conn.status_code == 202):
                media_id = json.loads(conn.text)['task_id']
                logger.debug("File uploaded successfully.\nmedia_id: %s" % media_id)
                return media_id
            else:
                logger.debug("Result: %s" % conn.text)
                raise RestError("Status Code: ", conn.status_code)
        except Exception as e:
            logger.debug(e)
            raise RestError("Problem in uploading video...")

    def video_by_url(self, video_url):
        if not isinstance(video_url, str):
            raise ApiError("video_url should be str")

        api = '/v1/upload_video_url'
        url = self.host + api
        payload = {
            "video_url": video_url,
        }
        headers = {
            "access_token": self.token,
            "Content-type": "application/json"
        }
        try:
            conn = requests.post(
                                    url,
                                    data = json.dumps(payload),
                                    headers = headers
                                )
            logger.debug('HTTP Status Code: %d' % conn.status_code)
            if (conn.status_code == 202):
                media_id = json.loads(conn.text)['task_id']
                logger.debug("File uploaded successfully.\nmedia_id: %s" % media_id)
                return media_id
            else:
                logger.debug("Result: %s" % conn.text)
                raise RestError("Status Code: ", conn.status_code)
        except Exception as e:
            logger.debug(e)
            raise RestError("Problem in uploading video...")

    def image_by_file(self, file):
        if not isinstance(file, str):
            raise ApiError("File should be a path on your system")

        api = '/v1/upload_image'
        url = self.host + api
        files = {
            'file': (file.split('/')[-1], open(file, 'rb'))
        }
        headers = {
            "access_token": self.token
        }
        try:
            conn = requests.post(
                                    url,
                                    files = files,
                                    headers = headers,
                                    timeout = 1200
                                )
            logger.debug('HTTP Status Code: %d' % conn.status_code)
            if (conn.status_code == 200):
                result = json.loads(conn.text)
                logger.debug("Result: %s" % conn.text)
                return result
            else:
                logger.debug("Result: %s" % conn.text)
                raise RestError("Status Code: ", conn.status_code)
        except Exception as e:
            logger.debug(e)
            raise RestError("Problem in uploading image...")

    def image_by_url(self, image_url):
        if not isinstance(image_url, str):
            raise ApiError("Image url should be string")

        api = '/v1/upload_image_url'
        url = self.host + api
        payload = {
            "image_url" : image_url,
        }
        headers = {
            "access_token": self.token,
            "Content-type": "application/json"
        }
        try:
            conn = requests.post(
                                    url,
                                    data = json.dumps(payload),
                                    headers = headers,
                                    timeout = 1200
                                )
            logger.debug('HTTP Status Code: %d' % conn.status_code)
            if (conn.status_code == 200):
                logger.debug("Result: %s" % conn.text)
                result = json.loads(conn.text)
                return result
            else:
                logger.debug("Result: %s" % conn.text)
                raise RestError("Status Code: ", conn.status_code)
        except Exception as e:
            logger.debug(e)
            raise RestError("Problem in uploading image...")

    def predict_video(self, media_id):
        if not isinstance(media_id, str) or not media_id:
            raise ValueError("media_id should be valid string")

        api = '/v1/get_video_result/'
        url = self.host + api + media_id
        headers = {
            "access_token": self.token,
        }
        try:
            conn = requests.get(
                                    url,
                                    headers = headers
                                )
            logger.debug('HTTP Status Code: %d' % conn.status_code)
            if (conn.status_code == 200):
                return json.loads(conn.text)
            elif (conn.status_code == 102):
                logger.debug("Converting file...")
                return "Please Wait Until Convert Complete"
            else:
                logger.debug("Result: %s" % conn.text)
                raise RestError("Status Code: %s", conn.status_code)
        except Exception as e:
            raise RestError("Rest Error", e)

    def start_video_model(self, **kwargs):
        if not kwargs:
            raise ValueError('url or file must be provided as keyword arguments')
        if 'url' in kwargs and 'file' in kwargs:
            raise ValueError('either url or file should be provided as keyword arguments, not both')

        media_id = ""
        if 'url' in kwargs:
            media_id = self.video_by_url(kwargs['url'])
        elif 'file' in kwargs:
            media_id = self.video_by_file(kwargs['file'])
        return media_id


    def start_image_model(self, **kwargs):
        if not kwargs:
            raise ValueError('url or file must be provided as keyword arguments')
        if 'url' in kwargs and 'file' in kwargs:
            raise ValueError('either url or file should be provided as keyword arguments, not both')

        result = None
        if 'url' in kwargs:
            result = self.image_by_url(kwargs['url'])
        elif 'file' in kwargs:
            result = self.image_by_file(kwargs['file'])
        return result

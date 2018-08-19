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
formatter = logging.Formatter('%(levelname)s - %(message)s')

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

        body, content_type, content_length = encode_multipart_data(file)
        conn = HTTPSConnection(self.host)

        headers = self._set_boilerplate_headers(**{
            'Content-Type': content_type,
            'Content-Length': content_length
        })

        url = '/v1/upload_video'
        conn.request('POST', url, body, headers)

        try:
            res = conn.getresponse()
            logger.debug('http status: %d' % res.status)
            if (res.status == 200):
                res = res.read()
                media_id = json.loads(res.decode('ascii'))['media_id']
                logger.debug("file uploaded successfully. media_id: %s" % media_id)
                return media_id
            else:
                logger.debug(res.read())
                raise RestError("status code: ", res.status)
        except Exception as e:
            logger.debug(e)
            raise RestError("Problem in uploading video....")

    def video_by_url(self, video_url):
        if not isinstance(video_url, str):
            raise ApiError("video_url should be str")

        url = '/v1/upload_video_url'
        conn = HTTPSConnection(self.host)

        body = {'video_url': video_url}
        body = json.dumps(body).encode('ascii')

        headers = self._set_boilerplate_headers(**{'Content-Type': 'application/json'})

        conn.request('POST', url, body, headers)

        try:
            res = conn.getresponse()
            logger.debug('http status: %d' % res.status)
            if (res.status == 200):
                res = res.read()
                media_id = json.loads(res.decode('ascii'))['media_id']
                logger.debug("file uploaded successfully. media_id: %s" % media_id)
                return media_id
            else:
                logger.debug(res.read())
                raise RestError("http status: %d" % res.status)
        except Exception as e:
            logger.debug(e)
            raise RestError("Problem in uploading video....")

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
                                    headers = headers
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
                                    headers = headers
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

    def predict_video(self, media_id, models):
        if not isinstance(media_id, str) or media_id == "":
            raise ValueError("media_id should be valid string")

        if not isinstance(models, list):
            raise ApiError("models should be list")

        url = '/api/models/video'
        conn = HTTPSConnection(self.host)

        body = {'media_id': media_id, 'models': models}
        body = json.dumps(body).encode('ascii')

        headers = self._set_boilerplate_headers(**{'Content-Type': 'application/json'})

        conn.request('POST', url, body, headers)
        try:
            res = conn.getresponse()
            resp = res.read().decode('ISO-8859-1')
            logger.debug('http status: %d' % res.status)
            logger.debug('http response: %s' % resp)
            if (res.status == 200):
                return json.loads(resp)
            if (res.status == 102):
                logger.debug("Converting file")
                return json.loads(resp)
        except Exception as e:
            raise RestError("Rest Error", e)

    def start_video_model(self, models, **kwargs):
        if not kwargs:
            raise ValueError('url or file must be provided as keyword arguments')
        if 'url' in kwargs and 'file' in kwargs:
            raise ValueError('either url or file should be provided as keyword arguments, not both')

        media_id = ""
        if 'url' in kwargs:
            media_id = self.video_by_url(kwargs['url'])
        elif 'file' in kwargs:
            media_id = self.video_by_file(kwargs['file'])
        return self.predict_video(media_id, models)


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

    def get_video_results(self, task_id):
        url = '/api/models/get_video_results'
        conn = HTTPSConnection(self.host)

        body = {'task_id': task_id}
        body = json.dumps(body).encode('ascii')

        headers = self._set_boilerplate_headers(**{'Content-Type': 'application/json'})

        conn.request('POST', url, body, headers)

        try:
            res = conn.getresponse()
            resp = res.read().decode('ISO-8859-1')
            logger.debug('http status: %d' % res.status)
            if (res.status == 200):
                return json.loads(resp)
            if (res.status == 102):
                logger.debug("http response: %s" % 'Still in progress')
                return
        except Exception as e:
            raise RestError("Rest Error", e)


    def _set_boilerplate_headers(self, **kwargs):
        headers = {}
        headers['Authorization'] = 'Bearer %s' % self.token
        headers['User-Agent'] = self._user_agent
        if kwargs:
            for (k,v) in kwargs.items():
                headers[k] = v
        return headers

import os
import json
from http.client import HTTPSConnection
from urllib.request import (
    Request,
    urlopen,
)

from utils import (
    encode_multipart_data,
)


class ApiError(Exception):
    pass


class SensifaiApi(object):
    def __init__(self, token=None, host=None):
        if token:
            self.token = token
        else:
            self.token = os.environ.get("SENSIFAI_API_TOKEN", None)

        if not self.token:
            raise ApiError("Please provide token")

        if host:
            self.host = host
        else:
            self.host = os.environ.get("SENSIFAI_API_BASE", None)

        if not self.host:
            self.host = 'api.sensifai.com'

        self._user_agent = 'Sensifai Python Client'


    def video_by_file(self, file):
        body, content_type, content_length = encode_multipart_data(file)
        conn = HTTPSConnection(self.host)

        headers = {}

        headers['Content-Type'] = content_type
        headers['Content-Length'] = content_length
        headers['Authorization'] = 'Bearer %s' % self.token
        headers['User-Agent'] = self._user_agent

        url = '/api/models/media_video_by_file'
        conn.request('POST', url, body, headers)
        res = conn.getresponse()

        res = res.read()
        return json.loads(res.decode('ascii'))['media_id']



    def video_by_url(self, video_url):
        if not isinstance(video_url, str):
            raise ApiError("video_url should be str")

        url = '/api/models/media_video_by_url'
        conn = HTTPSConnection(self.host)
        
        body = {'video_url': video_url}
        body = json.dumps(body).encode('ascii')

        headers = {}

        headers['Content-Type'] = 'application/json'
        headers['Authorization'] = 'Bearer %s' % self.token
        headers['User-Agent'] = self._user_agent

        conn.request('POST', url, body, headers)
        res = conn.getresponse()

        res = res.read()
        return json.loads(res.decode('ascii'))['media_id']


    def image_by_file(self, file):
        body, content_type, content_length = encode_multipart_data(file)
        conn = HTTPSConnection(self.host)

        headers = {}

        headers['Content-Type'] = content_type
        headers['Content-Length'] = content_length
        headers['Authorization'] = 'Bearer %s' % self.token
        headers['User-Agent'] = self._user_agent

        url = '/api/models/media_image_by_file'
        conn.request('POST', url, body, headers)
        res = conn.getresponse()

        res = res.read()
        return json.loads(res.decode('ascii'))['media_id']


    def image_by_url(self, image_url):
        if not isinstance(image_url, str):
            raise ApiError("image_url should be str")

        url = '/api/models/media_image_by_url'
        conn = HTTPSConnection(self.host)

        body = {'image_url': image_url}
        body = json.dumps(body).encode('ascii')
        
        headers = {}

        headers['Content-Type'] = 'application/json'
        headers['Authorization'] = 'Bearer %s' % self.token
        headers['User-Agent'] = self._user_agent

        conn.request('POST', url, body, headers)
        res = conn.getresponse()

        res = res.read()
        return json.loads(res.decode('ascii'))['media_id']


    def predict_image(self, media_id, models):
        if not isinstance(media_id, str):
            raise ApiError("media_id should be string")

        if not isinstance(models, list):
            raise ApiError("models should be list")

        url = '/api/models/image'
        conn = HTTPSConnection(self.host)

        body = {'media_id': media_id, 'models': models}
        body = json.dumps(body).encode('ascii')

        headers = {}

        headers['Content-Type'] = 'application/json'
        headers['Authorization'] = 'Bearer %s' % self.token
        headers['User-Agent'] = self._user_agent

        conn.request('POST', url, body, headers)
        res = conn.getresponse()

        res = res.read()
        return json.loads(res.decode('ascii'))

    def predict_video(self, media_id, models):
        if not isinstance(media_id, str):
            raise ApiError("media_id should be string")

        if not isinstance(models, list):
            raise ApiError("models should be list")

        url = '/api/models/video'
        conn = HTTPSConnection(self.host)

        body = {'media_id': media_id, 'models': models}
        body = json.dumps(body).encode('ascii')

        headers = {}

        headers['Content-Type'] = 'application/json'
        headers['Authorization'] = 'Bearer %s' % self.token
        headers['User-Agent'] = self._user_agent

        conn.request('POST', url, body, headers)
        res = conn.getresponse()

        res = res.read()
        return json.loads(res.decode('ascii'))


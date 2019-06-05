"""
Sensifai Python Client
"""

import os
import json
import logging
import requests

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
            default to Https://dev-api.sensifai.com unless you set
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
            self.host = 'https://api.sensifai.com/api/'

        self._user_agent = 'Sensifai Python Client'

    def upload_by_urls(self, urls):
        if not isinstance(urls, list):
            raise ApiError("urls should be list")

        payload = {
        'query':'mutation( $token: String!, $urls: [String!]! ){uploadByUrl( token: $token, urls: $urls){result error succeed{file taskId} cannotUpload}}',
        'variables':{'urls':urls,
                     'token':self.token}
        }
        headers = {
            "content-type": "application/json"
        }
        try:
            conn = requests.post(
                                    self.host,
                                    data = json.dumps(payload),
                                    headers = headers
                                )
            logger.debug('HTTP Status Code: %d' % conn.status_code)
            if (conn.status_code == 200):
                data = json.loads(conn.text)['data']['uploadByUrl']
                if data['result']:
                    logger.debug("File uploaded successfully.")
                    return {'succeed':data['succeed'], 'cannotUpload':data['cannotUpload']}
                else:
                    logger.error("error: {}").format(data['error'])
            else:
                logger.error("Result: %s" % conn.text)
                raise RestError("Status Code: ", conn.status_code)
        except Exception as e:
            logger.error(e)
            raise RestError("Something went wrong, contact to support")

    def upload_by_files(self, files):
        if not isinstance(files, list):
            raise ApiError("Files should be a list")
        file_place = '[' + ', '.join(['null' for i in files]) + ']'
        file_map = json.dumps({ str(k): ["variables.files.{}".format(k)] for k in range(0,len(files))})
        files_dict = {"{}".format(i):(v, open(v, 'rb')) for i,v in enumerate(files)}
        payload = {
            'operations': (None, '{"query": "mutation($files: [Upload!]!, $token :String!) { uploadByFile(files: $files, token:$token ) { error result succeed{file taskId} cannotUpload} }", "variables": { "files": ' + file_place + ' ,"token":"' + self.token  + '"}}'),
            'map': (None, file_map),
        }
        payload.update(files_dict)
        try:
            conn = requests.post(
                                    self.host,
                                    files = payload
                                )
            logger.debug('HTTP Status Code: %d' % conn.status_code)
            if (conn.status_code == 200):
                data = json.loads(conn.text)['data']['uploadByFile']
                if data['result']:
                    logger.debug("File uploaded successfully.")
                    return {'succeed':data['succeed'], 'cannotUpload':data['cannotUpload']}
                else:
                    logger.error("error: {}").format(data['error'])
            else:
                logger.error("Result: %s" % conn.text)
                raise RestError("Rest Error", e)

        except Exception as e:
            logger.error(e)
            raise RestError("Something went wrong, contact to support")

    def get_result(self, task_id):

        if not isinstance(task_id, str) or not task_id:
            raise ValueError("task_id should be valid string")

        payload = {
        'query': 'query( $taskId: String! ){apiResult( taskId: $taskId){ ...on ImageResult{isDone errors imageResults{nsfwResult{type probability value}logoResult{description}landmarkResult{description}taggingResult{label probability}faceResult{detectedBoxesPercentage probability detectedFace label}}} ... on VideoResult{fps duration isDone framesCount errors videoResults{startSecond endSecond startFrame endFrame thumbnailPath taggingResult{label probability}actionResult{label probability}celebrityResult{name frequency} sportResult{label probability}nsfwResult{probability type value}}}}}',
        'variables':{'taskId':task_id}
        }
        headers = {
            "content-type": "application/json"
        }
        try:
            conn = requests.post(
                                    self.host,
                                    data = json.dumps(payload),
                                    headers = headers
                                )
            logger.debug('HTTP Status Code: %d' % conn.status_code)
            if (conn.status_code == 200):
                data = json.loads(conn.text)['data']['apiResult']
                return data
            else:
                logger.debug("Result: %s" % conn.text)
                raise RestError("Status Code: %s", conn.status_code)
        except Exception as e:
            raise RestError("Rest Error", e)


    def start_model(self, **kwargs):
        if not kwargs:
            raise ValueError('url or file must be provided as keyword arguments')
        if 'urls' in kwargs and 'files' in kwargs:
            raise ValueError('either url or file should be provided as keyword arguments, not both')

        task_id = None
        if 'urls' in kwargs:
            task_id = self.upload_by_urls(kwargs['urls'])
        elif 'files' in kwargs:
            task_id = self.upload_by_files(kwargs['files'])
        return task_id


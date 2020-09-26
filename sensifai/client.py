"""
Sensifai Python Client
"""

import os
import json
import logging
import requests

from sensifai.payloads import (
    upload_by_url_payload,
    upload_by_file_payload,
    default_response_query,
    get_result_payload,
)
from sensifai.exceptions import ApiError, ClientError
from sensifai.responses import upload_response_maker, get_result_response_maker

logger = logging.getLogger("sensifai")


class SensifaiApi(object):
    def __init__(self, **kwargs):
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

        self.token = kwargs.get("token", os.environ.get("SENSIFAI_API_TOKEN", None))

        if not self.token:
            raise ClientError("token is Required")

        self.host = kwargs.get(
            "host", os.environ.get("SENSIFAI_API_BASE", "https://api.sensifai.com/api/")
        )

        self._user_agent = "Sensifai Python Client"

        formatter = logging.Formatter("%(message)s")

        logger.handlers = []
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        quiet = kwargs.get("quiet", True)
        if quiet:
            logger.setLevel(logging.ERROR)
        else:
            logger.setLevel(logging.DEBUG)

    def upload_by_urls(self, urls):
        if not isinstance(urls, list):
            raise ClientError("urls should be list")

        payload, headers = upload_by_url_payload(urls, self.token)

        try:
            conn = requests.post(self.host, data=json.dumps(payload), headers=headers)
            data = json.loads(conn.text)["data"]["uploadByUrl"]

            response = upload_response_maker(data)
            logger.debug(str(response))
            return response

        except Exception as e:
            raise ApiError(e)

    def upload_by_files(self, files):
        if not isinstance(files, list):
            raise ClientError("Files should be a list")

        payload = upload_by_file_payload(files, self.token)
        try:
            conn = requests.post(self.host, files=payload)

            data = json.loads(conn.text)["data"]["uploadByFile"]

            response = upload_response_maker(data)
            logger.debug(str(response))
            return response

        except Exception as e:
            raise ApiError(e)

    def get_result(self, task_id, new_query={}):
        if not isinstance(task_id, str) or not task_id:
            raise ClientError("task_id should be valid string")

        query = new_query
        if not new_query:
            query = default_response_query()

        image_query = video_query = ""

        for key, value in query.get("videoResults", {}).items():
            video_query += f"{key}{{{' '.join(value)}}}" if value else f"{key} "

        for key, value in query.get("imageResults", {}).items():
            image_query += f"{key}{{{' '.join(value)}}}" if value else f"{key} "

        payload, headers = get_result_payload(
            image_query, video_query, task_id, self.token
        )

        try:
            conn = requests.post(self.host, data=json.dumps(payload), headers=headers)

            data = json.loads(conn.text)
            response = get_result_response_maker(data)
            return response

        except Exception as e:
            raise ApiError(e)

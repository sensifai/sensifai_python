import json


def upload_by_url_payload(urls, token):
    payload = {
        "query": "mutation( $token: String!, $urls: [String!]! ){uploadByUrl( token: $token, urls: $urls){result error succeed{file taskId} cannotUpload}}",
        "variables": {"urls": urls, "token": token},
    }
    headers = {"content-type": "application/json"}
    return payload, headers


def upload_by_file_payload(files, token):
    file_place = f"[{', '.join('null' for i in files)}]"
    file_map = json.dumps(
        {str(k): [f"variables.files.{k}"] for k in range(0, len(files))}
    )
    files_dict = {f"{i}": (v, open(v, "rb")) for i, v in enumerate(files)}
    payload = {
        "operations": (
            None,
            f'{{"query": "mutation($files: [Upload!]!, $token :String!) {{ uploadByFile(files: $files, token:$token ) {{ error result succeed{{file taskId}} cannotUpload}} }}", "variables": {{ "files": {file_place}  ,"token": "{token}"}}}}',
        ),
        "map": (None, file_map),
    }
    payload.update(files_dict)

    return payload


def default_response_query():
    query = {
        "imageResults": {
            "nsfwResult": ("type", "probability", " value"),
            "logoResult": ("description",),
            "landmarkResult": ("description",),
            "taggingResult": ("label", "probability"),
            "faceResult": (
                "detectedBoxesPercentage",
                "probability",
                "detectedFace",
                "label",
            ),
        },
        "videoResults": {
            "startSecond": tuple(),
            "endSecond": tuple(),
            "startFrame": tuple(),
            "endFrame": tuple(),
            "thumbnailPath": tuple(),
            "taggingResult": ("label", "probability"),
            "actionResult": ("label", "probability"),
            "celebrityResult": ("name", "frequency"),
            "sportResult": ("label", "probability"),
            "nsfwResult": ("type", "probability", "value"),
        },
    }
    return query


def get_result_payload(image_query, video_query, task_id, token):
    if image_query:
        image_query = (
            f" ...on ImageResult{{isDone errors imageResults{{{image_query}}}}}"
        )
    if video_query:
        video_query = f" ...on VideoResult{{fps duration isDone framesCount errors videoResults{{{video_query}}}}}"

    result_query = f"query( $taskId: String!, $token: String! ){{apiResult( taskId: $taskId, token: $token ){{{image_query}{video_query}}}}}"
    payload = {"query": result_query, "variables": {"taskId": task_id, "token": token}}

    headers = {"content-type": "application/json"}
    return payload, headers

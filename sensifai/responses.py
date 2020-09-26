from sensifai.exceptions import ApiError


def upload_response_maker(data):
    error = data.get("error", None)
    if error:
        raise ApiError(error)
    response = {
        "succeed": data.get("succeed", None),
        "cannotUpload": data.get("cannotUpload", None),
    }
    return response


def get_result_response_maker(data):
    error = data.get("errors", None)
    if error:
        raise ApiError(error)

    response = data.get("data", {}).get("apiResult", {})
    return response

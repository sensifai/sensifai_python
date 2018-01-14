Sensifai API Python Client
====================

Sensifai API Python Client

Overview
---------------------
This Python client provides a wrapper around Sensifai <a href="https://developers.sensifai.com"> Image and Video recognition API</a>.


Installation
---------------------
The API client is available on Pip. You can simply install it with a `pip install`
```sh
pip install sensifai 
```

For more details on the installation, please refer to https://developers.sensifai.com/installation

Requirements
---------------------
You need a SENSIFAI_API_TOKEN.You can get a free limited `token` from https://developers.sensifai.com

## Usage

```python
from sensifai_python.rest import SensifaiApi

s = SensifaiApi(token)

media_id = s.video_by_file('your-video-file.mp4')

result = s.predict_video(media_id, ['tagging', 'nsfw', 'action'])
```



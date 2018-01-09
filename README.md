# Sensifai API Python Client

## Installation

```sh
pip install sensifai_python
```

## Usage

```python
from sensifai_python.rest import SensifaiApi

s = SensifaiApi(token)

media_id = s.video_by_file('your-video-file.mp4')

result = s.predict_video(media_id, ['tagging', 'nsfw', 'action'])
```


Sensifai API Python Client
====================

Sensifai API Python Client

Overview
---------------------
This Python client provides a wrapper around Sensifai <a href="https://developer.sensifai.com"> Image and Video recognition API</a>.


Installation
---------------------
The API client is available on Pip. You can simply install it with a `pip install`
```sh
pip install sensifai 
```

For more details on the installation, please refer to https://developer.sensifai.com/installation

Requirements
---------------------
You need a SENSIFAI_API_TOKEN.You can get a free limited `token` from https://developer.sensifai.com




## Video recognition sample
---------------------
The following example will setup the client and predict video attributes.First of all you need to import library and define an instance from `SensifaiApi` class using `SENSIFAI_API_TOKEN`

```python

#import Library
from sensifai import SensifaiApi

# Initialize an instance with Your Private token
private_token="xxx_yyy_zzz_Your_Token"
api_call = SensifaiApi(private_token, [host= "host#xxx.sensifai.com"])
```
after importing library and setting api token you are able to start a new task by giving a file/link and determine models from our pre-trained models. you can choose multiple models based on your needs when you create the application  in developer profile page .Currently our api supports the following models: 

+ tagging  for shot detection and video annotation 
+ face : face detection and celebrity recognition
+ action : Action Recognition
+ nsfw : Not safe for work 

If wanting to predict a link, use `start_video_model` with  `url` attribute.
```python
# Call by Video URL
task_meta = api_call.start_video_model( url="link to video")
```

otherwise ,If you want to predict a local file, use `start_video_model` with  `file` attribute.
```python

# Call by Video File
task_meta = api_call.start_video_model( file="path to video")
```
We use a non-blocking procedure, due to the fact that processing long videos can takes too long (upto an hour).  To retrieve results you need to call `get_video_results` method. if the result is not ready you recieve htp 102 code, otherwise The response will be a JSON structure.
```python

#To retrieve results:
result = api_call.predict_video(task_meta['task_id'])
```
Here's how to save all the predicted concepts associated with the video.

```python

#To save as a JSON file
import json
JSON_FILE_PATH="/home/foo/result.json"
json.dump(result,open(JSON_FILE_PATH,'w'))

```
## Image recognition sample
---------------------

The following example will setup the client and predict image attributes.First of all you need to import library and define an instance from `SensifaiApi` class using `SENSIFAI_API_TOKEN`

```python

#import Library
from sensifai import SensifaiApi

# Initialize an instance with Your Private token
private_token="xxx_yyy_zzz_Your_Token"
api_call = SensifaiApi(private_token , host = "host#xxx.sensifai.com")
```

start a new task by giving a file/link and models. you can choose multiple models in developer profile page when creating the application .

+ Currently our api supports the following # models : 
+ tagging  for shot detection and video annotation 
+ face : face detection and celebrity recognition
+ logo : Logo and brand recognition
+ Landmark : landmark and famous places recognition
+ nsfw : Not safe for work 

Its time to start the prediction procedure. If wanting to predict a link, use `start_image_model` with  `url` attribute.otherwise ,If you want to predict a local file, use `start_image_model` with  `file` attribute.


```python
# Call by Image URL
result = api_call.start_image_model(url="link to image")

# Call by Image File
result = api_call.start_image_model(file="path to image")
```

```
And finally, here's how to save all the predicted concepts associated with the image.
```python
#To save as a JSON file
import json
JSON_FILE_PATH="/home/foo/result.json"
json.dump(result,open(JSON_FILE_PATH,'w'))

```


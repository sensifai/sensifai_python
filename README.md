Sensifai API Python Client
====================

Sensifai API Python Client

Overview
---------------------
This Python client provides a wrapper around Sensifai <a href="https://developer.sensifai.com"> Image and Video recognition API</a>.


Installation
---------------------
The API client is available on Pip. You can simply install it with ` pip install`
```sh
pip3 install sensifai -U
```

For more details on the installation, please refer to https://developer.sensifai.com/installation

Requirements
---------------------
You need a SENSIFAI_API_TOKEN. You can get a free limited `token` from https://developer.sensifai.com




## Video recognition sample
---------------------
The following example will set up the client and predict video attributes. First of all, you need to import the library and define an instance from `SensifaiApi` class using `SENSIFAI_API_TOKEN`

```python

#import Library
from sensifai import SensifaiApi

# Initialize an instance with Your Private token
private_token="xxx_yyy_zzz_Your_Token"
api_call = SensifaiApi(private_token)
```
after importing library and setting API token you are able to start a new task by giving a file/link and determine models from our pre-trained models. you can choose multiple models based on your needs when you create the application in the developer profile page. Currently, our API supports the following models: 

+ tagging  for shot detection and video annotation 
+ face: face detection and celebrity recognition
+ action : Action Recognition
+ NSFW: Not safe for work 

If wanting to predict a link, use `start_video_model` with  `url` attribute.
```python
# Call by Video URL
task_meta = api_call.start_video_model( url="link to video")
```

otherwise , If you want to predict a local file, use `start_video_model` with  `file` attribute.
```python

# Call by Video File
task_meta = api_call.start_video_model( file="path to video")
```
We use a non-blocking procedure, due to the fact that processing long videos can take too long (up to an hour). Also, initialization of the machines can take between 1-5 minutes for the first run. To retrieve results you need to call `get_video_results` method. if the result is not ready you receive HTTP 102 code, otherwise, The response will be a JSON structure. if you don't send a request for more than 15 minutes, we turn the system off automatically and if you send a new request after this gap, you have to wait for initialization time.
```python

#To retrieve results:
result = api_call.get_video_result(task_meta['task_id'])
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

The following example will set up the client and predict image attributes. First of all, you need to import the library and define an instance from `SensifaiApi` class using `SENSIFAI_API_TOKEN`

```python

#import Library
from sensifai import SensifaiApi

# Initialize an instance with Your Private token
private_token="xxx_yyy_zzz_Your_Token"
api_call = SensifaiApi(private_token )
```

start a new task by giving a file/link and models. you can choose multiple models in developer profile page when creating the application.

Currently our API supports the following  models : 
+ tagging  for shot detection and video annotation 
+ face: face detection and celebrity recognition
+ logo: Logo and brand recognition
+ Landmark: landmark and famous places recognition
+ NSFW: Not safe for work 

It's time to start the prediction procedure. If wanting to predict a link, use `start_image_model` with  `url` attribute. otherwise, If you want to predict a local file, use `start_image_model` with  `file` attribute.


```python
# Call by Image URL
task_meta =  = api_call.start_image_model(url="link to image")

# Call by Image File
task_meta =  = api_call.start_image_model(file="path to image")
```
We use a non-blocking procedure, due to the fact that initializing the machines can take 1-5 minutes based on the models you choose.   To retrieve results you need to call `get_image_results` method. if the result is not ready you receive HTTP 102 code, otherwise, The response will be a JSON structure. if you get the result for the first image, you'll be able to get the result for next images very quickly. if you don't send a request for more than 15 minutes, we turn the system off automatically and if you send a new request after this gap, you have to wait for initialization time.  

```python

#To retrieve results:
result = api_call.get_image_result(task_meta['task_id'])
```

```
And finally, here's how to save all the predicted concepts associated with the image.
```python
#To save as a JSON file
import json
JSON_FILE_PATH="/home/foo/result.json"
json.dump(result,open(JSON_FILE_PATH,'w'))

```


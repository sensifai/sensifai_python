Sensifai API Python Client
====================

Sensifai API Python Client

Overview
---------------------
This Python client provides a wrapper around Sensifai [https://developer.sensifai.com](Image and Video recognition API).


Installation
---------------------
The API client is available on Pip. You can simply install it with ` pip install`
```sh
pip3 install sensifai -U
```

For more details on the installation, please refer to https://developer.sensifai.com/installation

Please always make sure that you'll use the latest version of our SDK.


#### Sample Usage
---------------------

The following example will set up the client and predict video attributes. First of all, you need to import the library and define an instance from `SensifaiApi` class using `SENSIFAI_API_TOKEN`. You can get a free limited `token` from https://developer.sensifai.com  by creating an application. 

```python
from sensifai import SensifaiApi
```
first of all, create an instance of SensifaiApi

```python
token = 'Your_token_that_you_create_in_panel'
sensifai_api = SensifaiApi(token = token)
```
after that, call `upload_by_files` or `upload_by_urls` with appropriate list. let's see an example:

```python
# url example for image urls
urls_list = ['https://url1.png', 'http://url2.jpg']
# url example for video urls
# urls_list = ['https://url1.avi', 'http://url2.mp4']
task_dict = sensifai_api.upload_by_urls(urls_list) 

# file example
files_list = ['/home/user/1.png', '/var/file/video.jpg']
task_dict = sensifai_api.upload_by_files(files_list)
```
as you can see, `upload_by_files` and `upload_by_urls` return a variable that is a dictionary contain `succeed` that a list of dictionaries with `file` and `taskId` and `cannotUpload` that are links that cannot upload list contain the links that the server failed to get them or conflict with the token. for example, if you set a video token for an instance and send image with it, they won't be processed and return cannot upload list.



at the end, to retrieve result of a task, pass it through `get_result` . Please don't remember to pass a single task id! this function won't work with a list of task id.

```python
results = sensifai_api.get_result(task_id)
```

Notice: result type is dictionary. there are two variables that always present in the result, isDone, and errors. the first one defines the state of a task. if all selected services are ready, isDone will be true, otherwise it will be false if the task id belongs to an image, you'll get imageResults in your dictionary and for video, you'll get videoResults.

if task id belongs to a video, you'll get fps, duration, and framesCount too. imageResults is a dictionary of selected service results that you choose when you're creating the application. videoResults is a list of shots that every shot is a dictionary contains startSecond, endSecond, startFrame, endFrame, thumbnailPath and selected service result that you choose when you're creating the token.

Here's how to save all the predicted concepts associated with the video.



```python
import json
from pprint import pprint
                                         

for id in task_dict["succeed"]: 
    result = sensifai_api.get_result(id["taskId"]) 
    pprint(id["file"]) 
    JSON_FILE_PATH="/home/foo/{}-result.json".format(id["file"])
    json.dump(result,open(JSON_FILE_PATH,'w'))  
    pprint(result) 
    pprint("_____________________________") 


#To save as a JSON file
```

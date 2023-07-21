import datetime
import glob
import json
import os.path

from fastapi import FastAPI, Response, status
from pydantic import BaseModel

app = FastAPI()


# @app.get('/')
# def get_hello_world():
#     return {'answer': 'Hello world'}
#
#
# @app.get('/items/{item_id}')
# def get_item(item_id:int):
#     return {'item_id': item_id}

ACTIVITIES_FOLDER = 'activities'


class Activity(BaseModel):
    id: int
    name: str
    date: datetime.datetime


def find_activity(activity_id=0):
    print(f'activity_{activity_id if activity_id else ""}.json')
    return glob.glob(os.path.join(ACTIVITIES_FOLDER, f'activity_{activity_id if activity_id else "*"}.json'))


@app.get('/activities/get/all')
def get_activity():
    files = find_activity()
    res = []
    for file in files:
        with open(file, 'r') as f:
            res.append(json.loads(f.read()))
    return res
    # return [pydantic.parse_file_as(Activity, file) for file in files]


@app.get('/activities/get/{activity_id}')
def get_activity(activity_id: int, response: Response):
    files = find_activity(activity_id)
    if files:
        with open(files[0], 'r') as f:
            return json.loads(f.read())
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {}


@app.post('/activities/add/{activity_id}')
def add_activity(activity_id: int, activity: Activity, response: Response):
    file = find_activity(activity_id)
    if file:
        response.status_code = status.HTTP_302_FOUND
        return False
    else:
        with open(os.path.join(ACTIVITIES_FOLDER, f'activity_{activity_id}.json'), 'w') as f:
            f.write(activity.model_dump_json())
    return True


@app.put('/activities/update/{activity_id}')
def update_activity(activity_id: int, activity: Activity, response: Response):
    files = find_activity(activity_id)
    if files:
        with open(files[0], 'w') as f:
            f.write(activity.model_dump_json())
        return True
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return False


@app.delete('/activities/delete/{activity_id}')
def update_activity(activity_id: int, response: Response):
    files = find_activity(activity_id)
    if files:
        os.remove(files[0])
        return True
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return False
import pytest
import requests

ENDPOINT = 'https://todo.pixegami.io/'


def test_call_root_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200

def test_create_task_endpoint():
    payload = create_payload()
    response = create_task(payload)
    assert response.status_code == 200 

def test_get_task_endpoint():
    payload = create_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    response_data = create_task_response.json()
    task_id = response_data['task']['task_id']
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 200
    task_data = get_task_response.json()
    assert task_data['content'] == payload['content']

def test_update_task_endpoint():
    payload = create_payload()
    create_response = create_task(payload)
    assert create_response.status_code == 200
    task_response = create_response.json()
    new_payload = {
        'user_id': task_response['task']['user_id'],
        'task_id': task_response['task']['task_id'],
        'is_done': True,
        'content': 'updated content'
    }
    update_response = update_task(new_payload)
    assert update_response.status_code == 200 

def test_delete_task_endpoint():
    payload = create_payload()
    create_response = create_task(payload)
    assert create_response.status_code == 200
    task_response = create_response.json()
    task_id = task_response['task']['task_id']
    delete_response = delete_task(task_id)
    assert delete_response.status_code == 200

def test_list_tasks_endpoint():
    user_id = 'test_user'
    list_tasks_response = list_tasks(user_id)
    response = list_tasks_response.json()
    assert list_tasks_response.status_code == 200 
    assert len(response['tasks']) == 10

def create_payload():
    payload = {
        "content": "new task",
        "user_id": "test_user",
        "task_id": "task1",
        "is_done": False
    }
    return payload

def create_task(payload):
    return requests.put(ENDPOINT + 'create-task', json=payload)

def get_task(task_id):
    return requests.get(ENDPOINT + f'get-task/{task_id}')

def update_task(payload):
    return requests.put(ENDPOINT + 'update-task', json=payload)

def delete_task(task_id):
    return requests.delete(ENDPOINT + f'delete-task/{task_id}')

def list_tasks(user_id):
    return requests.get(ENDPOINT + f'list-tasks/{user_id}')
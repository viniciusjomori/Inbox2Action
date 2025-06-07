from typing import Literal
from src.util.https import HttpClient
from src.util import directory

from datetime import datetime
import os

api_key = os.getenv('CLICKUP_API_KEY')

priority_map = {
    'baixa': 4,
    'normal': 3,
    'alta': 2,
    'urgente': 1
}

http_client = HttpClient(
    base='https://api.clickup.com/api/v2/',
    headers={
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": api_key
    } 
)

def create_task(
        name: str,
        description: str,
        tags: list,
        priority: Literal['baixa', 'normal', 'alta', 'urgente'],
        due_date: datetime,
        list_id: str
):

    priority = priority_map[priority]
    due_date = int(due_date.timestamp()) * 1000

    response = http_client.post(
        f"list/{list_id}/task",
        body={
            "name": name,
            "description": description,
            "tags": tags,
            "priority": priority,
            "due_date": due_date
        }
    )

    task_id = response.body['id']

    if response.status != 200:
        print(response.body)
        raise Exception('Erro ao criar tarefa!')
    
    for file in directory.ls_files('/tmp/attachs'):
        attach(task_id, file)
    
    return task_id

def get_lists(space_id, archived=False):
    response = http_client.get(
        endpoint=f'space/{space_id}/list',
        params={'archived': archived}
    )

    return response.body['lists']

def attach(task_id, filename):
    http_client.post(
        f'task/{task_id}/attachment',
        headers={"content-type": None},
        files={"attachment": (filename, open(f'/tmp/attachs/{filename}', "rb"))}
    )
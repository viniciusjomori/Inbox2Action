from typing import Literal
from src.util.https import HttpClient

from datetime import datetime
import os
import io

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

    if response.status != 200:
        print(response.body)
        raise Exception('Erro ao criar tarefa!')
    
    return response.body['id']

def get_lists(space_id, archived=False):
    response = http_client.get(
        endpoint=f'space/{space_id}/list',
        params={'archived': archived}
    )

    return response.body['lists']

def attach_file(task_id, filename, content):
    if isinstance(content, str):
        content = content.encode('utf-8')

    file_stream = io.BytesIO(content)
    file_stream.name = filename

    http_client.post(
        f'task/{task_id}/attachment',
        headers={"content-type": None},
        files={"attachment": (filename, file_stream)}
    )
from typing import Literal
from pydantic_ai import Agent
from pydantic import BaseModel, Field
from datetime import datetime
import os
import json

from src.service import clickup

system_prompt = f"""
Você é um agente que vai receber um email e deve transforma-lo em uma tarefa.
Se o prazo não for especificado, considere como a data de hoje
Se o prioridade não for especificada, considere como 'urgente'

Horário atual: {datetime.now()}
"""

class List(BaseModel):
    id: str = Field(description='ID da lista')
    name: str = Field(description='Nome da lista')

class Task(BaseModel):
    name: str = Field(description='Nome da tarefa')
    description: str = Field(description='Descrição da Tarefa')
    due_date: datetime = Field(description='Data de vencimento da tarefa')
    priority: Literal['baixa', 'normal', 'alta', 'urgente'] = Field(description='Prioridade da tarefa')
    tags: list[str] = Field(description='Tags da tarefa')
    list: List = Field(description='Lista a qual a tarefa pertence')

task_agent = Agent(
    model='openai:gpt-4o',
    system_prompt=system_prompt,
    output_type=Task
)

@task_agent.system_prompt
def context_list() -> str:
    space_id = os.getenv('CLICKUP_SPACE_ID')
    lists = clickup.get_lists(space_id)

    lists = [{'id': l['id'], 'name': l['name'], 'description': l['content']} for l in lists]
    return f"Você deve escolher uma lista para a tarefa. As listas disponíveis são: {json.dumps(lists)}"

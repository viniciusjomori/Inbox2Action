from typing import Literal
from pydantic_ai import Agent
from pydantic import BaseModel, Field
from datetime import datetime
import os
import json

from src.service import clickup

username = os.getenv("USERNAME")

system_prompt = f"""
# Agente de Tarefas

## Quem você é
Um assistente especializado em transformar emails em tarefas.

## Quem eu sou
{username}, o responsável pelas tarefas

## Qual seu objetivo
Transformar um email em uma tarefa estruturada
Prefira tarefas **direcionadas a mim**; se não houver, então escolha tarefas **solicitadas por mim**.

## Observações:
- Ignore saudações, rodapés e informações irrelevantes à execução da tarefa.
- Horário atual: {datetime.now()}
- Dia da semana: {datetime.now().strftime('%A')}
"""

class List(BaseModel):
    id: str = Field(description='ID da lista')
    name: str = Field(description='Nome da lista')

class Task(BaseModel):
    name: str = Field(description='Nome da tarefa. É um resumo em poucas palavras do que deve ser feito')
    description: str = Field(description='Descrição da Tarefa.')
    due_date: datetime = Field(
        description='Data da tarefa. Se não informado, será a data atual',
        default=datetime.now(),
    )
    priority: Literal[1, 2, 3, 4] = Field(
        description='Prioridade da tarefa. Quanto menor, mais importante. Se não informado, será 1',
        default=1,
    )
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

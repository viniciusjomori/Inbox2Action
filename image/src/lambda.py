import asyncio
import json

from src.agents.task_agent import task_agent
from src.util import html, rawemail, directory
from src.util.directory import File
from src.aws import s3, ses
from src.service import clickup

def extract_attachs(raw_email, content):
    rawemail.extract_attachs(raw_email, path='/tmp/attachs')

    if content['text/html']:
        content = content['text/html']
        cids = rawemail.extract_inline_images(raw_email)

        for old, new in cids.items():
            content = content.replace(f'cid:{old}', f'data:image/png;base64,{new}')
    
    else:
        content = content['text/plain']

    file = File('email.html', content)
    directory.create_file(file, '/tmp/attachs')

def send_email(raw_email, result, task_id):
    email = rawemail.extract_sender(raw_email)
    content = html.create_task_table(
        id=task_id,
        name=result.output.name,
        description = result.output.description,
        priority = result.output.priority,
        due_date = result.output.due_date,
        list_name=result.output.list.name,
        tokens=result.usage().request_tokens,
    )
    ses.send_email(
        content=content,
        to=[email],
        subject=f'{result.output.name} [Task {task_id}]'
    )

async def async_hendler(event, context):
    file = event['Records'][0]['s3']['object']['key']
    raw_email = s3.get_content(file)
    subject: str = rawemail.extract_subject(raw_email)
    content = rawemail.extract_content(raw_email)
    
    extract_attachs(raw_email, content)

    result = await task_agent.run(json.dumps({
        'subject': subject,
        'content': content['text/plain'][:3000]
    }))

    task_id = clickup.create_task(
        name = result.output.name,
        description = result.output.description,
        tags = result.output.tags,
        priority = result.output.priority,
        due_date = result.output.due_date,
        list_id = result.output.list.id
    )

    send_email(
        raw_email=raw_email,
        result=result,
        task_id=task_id,
    )

    return {
        'status': 200,
        'body': {
            'name': result.output.name,
            'description': result.output.description,
            'due_date': result.output.due_date.isoformat(),
            'priority': result.output.priority,
            'tags': result.output.tags,
            'list': result.output.list.name,
            'tokens': result.usage().request_tokens,
        }
    }

def handler(event, context):
    return asyncio.run(async_hendler(event, context))
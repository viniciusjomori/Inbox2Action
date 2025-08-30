import asyncio
import json
import logging
import os

logger = logging.getLogger()
logger.setLevel(os.getenv("LOG_LEVEL", "INFO").upper())

from src.agents.task_agent import task_agent
from src.util import html, rawemail
from src.aws import s3, ses
from src.service import clickup

context_size = int(os.getenv('TASK_CONTEXT_SIZE', 3000))

def attach_files(task_id, raw_email, content):
    attachs: list = rawemail.extract_attachs(raw_email)

    if content['text/html']:
        content = content['text/html']
        cids = rawemail.extract_inline_images(raw_email)

        for old, new in cids.items():
            content = content.replace(f'cid:{old}', f'data:image/png;base64,{new}')
    
    else:
        content = content['text/plain']

    attachs.append(('email.html', content))
    
    for filename, bytes in attachs:
        clickup.attach_file(task_id, filename, bytes)

def send_email(email, result, task_id):
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
    message = json.loads(event['Records'][0]['Sns']['Message'])

    logging.info("Fetching s3 object from SNS message...")
    raw_email = s3.from_sns(message)

    logging.info("Extracting subject and content from raw email..")
    subject = message['mail']['commonHeaders']['subject']
    content = rawemail.extract_content(raw_email)
    
    logging.info(f"Forwarding email content to AI Agent (context size: {context_size})...")
    result = await task_agent.run(json.dumps({
        'subject': subject,
        'content': content['text/plain'][:context_size]
    }))

    logging.info("Posting task into ClickUp API...")
    task_id = clickup.create_task(
        name = result.output.name,
        description = result.output.description,
        tags = result.output.tags,
        priority = result.output.priority,
        due_date = result.output.due_date,
        list_id = result.output.list.id
    )
    
    logging.info("Uploading attachments to ClickUp task...")
    attach_files(task_id, raw_email, content)

    logging.info("Sending confirmation email...")
    send_email(
        email=message['mail']['commonHeaders']['returnPath'],
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
    logging.info("Lambda execution start")
    logging.info("Lambda event payload: %s", event)

    res = asyncio.run(async_hendler(event, context))
    logging.info("Lambda execution complete")
    logging.info("Lambda response: %s", res)
    
    return res
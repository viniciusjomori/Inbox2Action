from email import message_from_string
from email.policy import default
from email import policy
from email.parser import BytesParser
from email.utils import parseaddr
from io import BytesIO
import base64
from typing import Tuple

def extract_content(raw_email: str):
    msg = message_from_string(raw_email, policy=default)

    content = {
        'text/plain': None,
        'text/html': None
    }

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition", ""))
            
            if content_type in content and "attachment" not in content_disposition:
                content[content_type] = part.get_content()
    else:
        content_type = msg.get_content_type()
        if content_type in content:
            content[content_type] = msg.get_content()

    return content

def extract_attachs(raw_email: str) -> list[Tuple]:
    attachs = []
    
    raw_bytes = raw_email.encode('utf-8')
    msg = BytesParser(policy=policy.default).parse(BytesIO(raw_bytes))

    for part in msg.iter_attachments():
        content_disposition = part.get_content_disposition()
        if content_disposition == 'attachment':
            attachs.append((
                part.get_filename(),
                part.get_payload(decode=True)
            ))
    return attachs

def extract_subject(raw_email: str) -> str:
    msg = message_from_string(raw_email, policy=default)
    return msg.get('Subject', '')

def extract_sender(raw_email: str) -> str:
    msg = message_from_string(raw_email, policy=default)
    name, email = parseaddr(msg.get('From', ''))
    return email

def extract_inline_images(raw_email: str):
    raw_bytes = raw_email.encode("utf-8")
    msg = BytesParser(policy=policy.default).parse(BytesIO(raw_bytes))

    cids = {}

    for part in msg.walk():
        content_type = part.get_content_type()
        content_disposition = part.get_content_disposition()
        content_id = part.get("Content-ID")

        if content_type.startswith("image/") and (content_disposition == "inline" or content_id):
            cid = content_id.strip("<>") if content_id else "inline_image"

            bytes = base64 \
                .b64encode(part.get_payload(decode=True)) \
                .decode('utf-8')

            cids[cid] = bytes

    return cids
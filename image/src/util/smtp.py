from email import message_from_string
from email.policy import default
from email import policy
from email.parser import BytesParser
from io import BytesIO

from src.util import directory
from src.util.directory import File

def extract_content(raw_email: str):
    msg = message_from_string(raw_email, policy=default)

    conteudos = {
        'text/plain': None,
        'text/html': None
    }

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition", ""))
            
            if content_type in conteudos and "attachment" not in content_disposition:
                conteudos[content_type] = part.get_content()
    else:
        # Caso não seja multipart, assume que o conteúdo principal está no corpo
        content_type = msg.get_content_type()
        if content_type in conteudos:
            conteudos[content_type] = msg.get_content()

    return conteudos

def extract_attachs(raw_email: str, path='/tmp'):
    raw_bytes = raw_email.encode('utf-8')
    msg = BytesParser(policy=policy.default).parse(BytesIO(raw_bytes))

    for part in msg.iter_attachments():
        attach = File(
            name=part.get_filename(),
            content=part.get_payload(decode=True)
        )
        directory.create_file(attach, path)

def extract_subject(raw_email: str) -> str:
    msg = message_from_string(raw_email, policy=default)
    return msg.get('Subject', '')
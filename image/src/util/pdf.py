from xhtml2pdf import pisa
import os

def from_html(html_content: str, dir_path, filename: str):
    os.makedirs(dir_path, exist_ok=True)

    with open(f'{dir_path}/{filename}', "wb") as file:
        pisa_status = pisa.CreatePDF(html_content, dest=file)
    return not pisa_status.err
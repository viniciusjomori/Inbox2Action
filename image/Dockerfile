FROM public.ecr.aws/lambda/python:3.11

ENV TZ=America/Sao_Paulo

COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install -r requirements.txt

COPY src ${LAMBDA_TASK_ROOT}/src

CMD [ "src.lambda.handler" ]
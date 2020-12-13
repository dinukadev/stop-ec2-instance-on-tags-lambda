FROM python:3.6-slim

ENV AWS_DEFAULT_REGION=ap-southeast-2
ENV TZ=UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN pip install --upgrade pip

RUN pip install pipenv
ADD Pipfile /home/ec2-stop-lambda/
ADD *.py /home/ec2-stop-lambda/
ADD serverless.yml /home/ec2-stop-lambda/

WORKDIR /home/ec2-stop-lambda

RUN pipenv install --dev

ENTRYPOINT exec pipenv run test

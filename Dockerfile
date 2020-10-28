
FROM ubuntu:18.04
RUN apt-get update && \
apt-get install -y --no-install-recommends python3 python3-virtualenv

RUN apt-get install -y build-essential
RUN apt-get install -y python3-dev

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m virtualenv --python=/usr/bin/python3 $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install tensorflow==1.14.0
RUN pip install gpt-2-simple==0.7.1
RUN pip install flask

COPY app.py .
COPY generate_tweets.py .
COPY main.py .


COPY ./gpt /gpt
COPY ./models /models
COPY ./checkpoint /checkpoint
COPY ./data /data
COPY ./static /static
COPY ./template /template


CMD ["python", "app.py"]
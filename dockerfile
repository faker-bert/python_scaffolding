FROM python:3.8.16-slim-buster
RUN apt update -y && \
    mkdir /usr/local/src/{{project_name}}
COPY  . /usr/local/src/{{project_name}}
WORKDIR /usr/local/src/{{project_name}}
ENV PYTHONPATH  "${PYTHONPATH}:/usr/local/src/{{project_name}}:/usr/local/src/{{project_name}}/www"
RUN pip install -r requirements.txt -i https://pypi.douban.com/simple/
ENV LC_ALL=en_US.utf8 LANG=en_US.utf8
# CMD uvicorn app.__main__:app --host 0.0.0.0 --port 8000
CMD ["bash"]
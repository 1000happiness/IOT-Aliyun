FROM python:3.6-alpine
RUN pip install aliyun-iot-linkkit
RUN pip install tornado
COPY ./  /iot
RUN chmod +x /iot/main.py
EXPOSE 8091
WORKDIR /iot
ENTRYPOINT ["python", "/iot/main.py"]



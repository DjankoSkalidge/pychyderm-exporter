FROM python:3.7
COPY pycharm-exporter.py /
RUN pip install prometheus_client, pachypy
EXPOSE 9426
CMD [ "python", "pycharm-exporter.py","-h", "pachd", "-p", "9426" ]
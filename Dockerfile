FROM python:3.7
COPY pychyderm-exporter.py /
RUN pip install prometheus_client, pachypy
EXPOSE 9426
CMD [ "python", "pychyderm-exporter.py","-h", "pachd", "-p", "9426" ]
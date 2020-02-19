FROM python:3.7
COPY src/pychyderm-exporter.py /
RUN pip install prometheus_client python-pachyderm
EXPOSE 9426
CMD [ "python", "pychyderm-exporter.py","--host", "pachd", "--port", "650" ]
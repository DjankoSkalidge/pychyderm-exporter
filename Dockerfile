FROM python:3.7
COPY pychyderm-exporter.py /
RUN pip install prometheus_client pachypy python-pachyderm
EXPOSE 9426
CMD [ "python", "pychyderm-exporter.py","-i", "pachd", "-p", "9426" ]
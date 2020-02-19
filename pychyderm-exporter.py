import argparse
from prometheus_client import start_http_server, Gauge
import time
import pachypy
import pandas as pd

pipelines = pd.DataFrame()
gauges = dict()
succescounters = dict()
failcounters = dict()
last_job_succes = True


def update_gauges(client):
    global gauges, pipelines
    pipelines = client.list_pipelines()
    for index, pipeline in pipelines.iterrows():
        key = pipeline["pipeline"]
        if key in gauges:
            if pipeline["jobs_succes"] > succescounters[key]:
                gauges[key].set(0)
                succescounters[key] = pipeline["jobs_succes"]
            if pipeline["jobs_failure"] > failcounters[key]:
                gauges[key].set(1)
                succescounters[key] = pipeline["jobs_failure"]


def main():
    global gauges, pipelines
    args = parse_args()
    port = args.port
    host = args.host

    pachyclient = pachypy.PachydermClient(host=host, port=port)
    start_http_server(port=port)
    pipelines = pachyclient.list_pipelines()
    for index, pipeline in pipelines.iterrows():
        g = Gauge("{}_last_job".format(pipeline["pipeline"]),
                  "Last Job status of pipeline {}".format(pipeline["pipeline"]))
        gauges[pipeline["pipeline"]] = g
        succescounters[pipeline["pipeline"]] = pipeline["jobs_success"]
        failcounters[pipeline["pipeline"]] = pipeline["jobs_failure"]
    while True:
        update_gauges(pachyclient)
        time.sleep(60)


def parse_args(args=None):
    parser = argparse.ArgumentParser(description='Prometheus exporter for PachyDerm metrics')
    parser.add_argument("-i", "--host", type=str, default="pachd", help="Host of pachd")
    parser.add_argument("-p", "--port", type=int, default=9426,
                        help="port number")
    return parser.parse_args(args=args)


if __name__ == '__main__':
    main()

import argparse
from prometheus_client import start_http_server, Gauge
import time
import python_pachyderm

gauges = dict()
succescounters = dict()
failcounters = dict()


def update_gauges(client):
    global gauges
    pipelines = client.list_pipeline().pipeline_info
    for pipeline in pipelines:
        name = str(pipeline.pipeline.name).replace("-", "_")
        if name in gauges:
            print("{} updated".format(name))
            gauges[name].set(pipeline.last_job_state)
            # if pipeline.job_counts[3] > succescounters[name]:
            #     gauges[name].set(0)
            #     succescounters[name] = pipeline.job_counts[3]
            # if pipeline.job_counts[2] > failcounters[name]:
            #     gauges[name].set(1)
            #     succescounters[name] = pipeline.job_counts[2]


def main():
    global gauges
    args = parse_args()
    port = args.port
    host = args.host

    pachyclient = python_pachyderm.Client().new_from_pachd_address("{}:{}".format(host, port))
    start_http_server(port=9426)
    pipelines = pachyclient.list_pipeline().pipeline_info
    for pipeline in pipelines:
        name = str(pipeline.pipeline.name).replace("-", "_")

        last_job_state = pipeline.last_job_state
        g = Gauge("{}_last_job".format(name),
                  "Last Job status of pipeline {}".format(name))
        gauges[name] = g
        succescounters[name] = pipeline.job_counts[3]
        failcounters[name] = pipeline.job_counts[2]
    while True:
        update_gauges(pachyclient)
        time.sleep(60)


def parse_args(args=None):
    parser = argparse.ArgumentParser(description='Prometheus exporter for PachyDerm metrics')
    parser.add_argument("-i", "--host", type=str, default="pachd", help="Host of pachd")
    parser.add_argument("-p", "--port", type=int, default=30650,
                        help="port number")

    return parser.parse_args(args=args)


if __name__ == '__main__':
    main()

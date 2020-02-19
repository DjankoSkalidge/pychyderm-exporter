# pychyderm-exporter

Exports metrics from the pachyderm cluster on port 9426. These metrics are available to a prometheus server running on K8s.

## Installation
Can be deployed as a pod on a Kubernetes cluster with the following command:
```shell script
kubectl apply -f https://github.com/DjankoSkalidge/pychyderm-exporter/blob/master/deployment/pychyderm-exporter.yaml
```
This will create a service, and a deployment with one pod.

## Metrics
The following metrics will be exported:
 - The status of the last job for every pipeline. <pipeline_name>_last_job
 
## Build docker image from source
1. Clone the repo
2. ```docker build <path_to_repo> <your_repo>/<your_tagname>```
3. ```docker push <your_repo>/<your_tagname>:latest```

## Execute locally
### Requirements
 - Prometheus Client: ```pip install prometheus_client```
 - Pachyderm Client: ```pip install python-pachyderm```
 
### Command
```python src/pychyderm-exporter.py --host <pachd_host> --port <pachd_port>```

If the pachd service is of type ```NodePort```, it can be reached by providing the ip adress of a kubernetes node as the ```<pachd_host>```. 

The port is 30650 by default.

### Functionality
This will expose metrics on http://localhost:9426/metrics

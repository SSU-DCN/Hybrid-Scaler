# Hybrid-Scaler
A Design of Horizontal PoD Autoscaler with Varying PoD's Resources for Kubernetes
One of the main challenges in deploying container service is providing the scalability to satisfy the service performance and avoid resource wastage as well. To deal with this challenge, Kubernetes provides the scaling ability in terms of both vertical and horizontal scaling modes. Several existing autoscaling methods make efforts to improve the default autoscalers in Kubernetes, however, most of these works only focus on one scaling mode at the same time, which results in some limitations. Only horizontal scaling may lead to low utilization of containers due to the fixed number of resources for each instance, especially in the low-request period. In contrast, only vertical scaling may not ensure the quality of service (QoS) requirements in case of burst workload due to reaching the upper limit. It is also necessary to provide burst identification for auto-scalers to guarantee service performance. In our thesis, we propose a design of horizontal pod autoscaler with varying pod’s resources for Kubernetes, a new hybrid approach that considers a combination of vertical and horizontal abilities to satisfy the QoS requirement while optimizing the utilization of containers. Our proposal uses a proactive method based on the deep learning model to forecast the future demand of the application and combines it with a burst identification module, which makes scaling decisions more effective. Experimental results illustrate the improvement in maintaining the response time below the QoS constraint whereas remaining high utilization of the deployment compared with existing baseline methods in single scaling mode.
# Guideline
##	Init Kubernetes cluster
-	On master node:
```
./master.sh
```
-	On worker nodes:
```
./worker.sh
```

##	Add on requirements for cluster
List of requirements:
On master node run:
-	Nginx ingress controller 1
```
cd  installation/ingress-controller-1/deployments
kubectl apply -f common/ns-and-sa.yaml
kubectl apply -f common/default-server-secret.yaml
kubectl apply -f common/nginx-config.yaml
kubectl apply -f common/ingress-class.yaml
kubectl apply -f rbac/rbac.yaml
kubectl apply -f deployment/nginx-ingress.yaml
kubectl create -f service/nodeport.yaml
```

-	Nginx ingress controller 2
```
cd  installation/ingress-controller-2/deployments
kubectl apply -f common/ns-and-sa.yaml
kubectl apply -f common/default-server-secret.yaml
kubectl apply -f common/nginx-config.yaml
kubectl apply -f common/ingress-class.yaml
kubectl apply -f rbac/rbac.yaml
kubectl apply -f deployment/nginx-ingress.yaml
kubectl create -f service/nodeport.yaml
```

-	Prometheus & Grafana
```
cd  installation/ prometheus
kubectl apply -f prometheus/
kubectl apply -f node-exporter/
kubectl apply -f kube-state-metrics-configs/
kubectl apply -f grafana/
```

-	Locust_exporter: install on master (.24.13) and worker1 (.24.14)
```
sudo docker run -d --net=host containersol/locust_exporter
```
-	Locust:
On master (.24.13)
```
python3 -m venv $HOME/generator1
source $HOME/generator1/bin/activate
pip install -U pip
pip3 install locust
```

On worker (.24.14)
```
python3 -m venv $HOME/generator2
source $HOME/generator2/bin/activate
pip install -U pip
pip3 install locust
python3 -m venv $HOME/generator1
source $HOME/generator1/bin/activate
pip install -U pip
pip3 install locust
```

## Run application 
On master node:
 - run deployment A:
 ```
 	cd run-app/deploymentA/
	kubectl apply -f deploymentA.yaml
	kubectl apply -f svc-deploymentA.yaml
	kubectl apply -f ingress-resource-1.yaml
 ```

- run deployment B:
```
	cd run-app/deploymentB/
	kubectl apply -f deploymentB.yaml
	kubectl apply -f svc-deploymentB.yaml
	kubectl apply -f ingress-resource-2.yaml
```

- apply HPA to deploymentB
```
	cd run-app/deploymentB/
	kubectl apply -f components.yaml
	kubectl apply -f hpa.yaml
```


- apply ai-scaler to deploymentA ( any minute at second ":5-10")
```
	cd scaler/
	kubectl apply -f demo-scaler.yaml
```

## Run load-generator (any minute at second ":9-11")

 generator1 on master node (192.168.24.13):
 ```
 	source $HOME/generator1/bin/activate
	locust -f longcustomshape.py
 ```

 ```
 	access URL:  192.168.24.13:8089
	host: http://deploya.example.com: 32205    --> start swarming (any minute at second ":9-11")
 ```
 

 generator2 on worker node (192.168.24.14):
```	
	source $HOME/generator2/bin/activate
	locust -f longcustomshape.py

	access URL:  192.168.24.14:8089
	host: http://deployb.example.com: 32725    --> start swarming (any minute at second ":9-11")
```

# How to run scaler
```
sudo apt install python3-dev python3-venv libffi-dev gcc libssl-dev git
python3 -m venv $HOME/demo-daivd
source $HOME/demo-daivd/bin/activate
pip install -U pip
pip install -r requirements.txt
python3 main.py
```
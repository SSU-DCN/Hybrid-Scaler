import schedule
import time
import os
from configs import configs
import requests
import executor
import csv

#warings.filterwarnings(action='ignore')

def get_metric():
    #q = 'rate(nginx_ingress_nginx_http_requests_total{app="nginx-ingress", class="nginx"}[15s])'
    #q = 'sum(rate(nginx_ingress_nginx_http_requests_total{app="nginx-ingress", class="nginx"}[15s]))'  
    q = 'locust_users{instance="192.168.24.10:9646", job="generator1"}'
    test = []
    f = open('./dataset/request.csv', 'a', newline='')
    with f:
        writer = csv.writer(f)
        response = requests.get('{0}/api/v1/query'.format(configs.PROMETHEUS_URL), params={'query': q})
        if bool(response.json()['data']['result']):
            results = response.json()['data']['result'][0]['value'][1]
            results = float(results)
            results = round(results, 3)
            test.append(results)
        if bool(test):
            writer.writerow(test)
def scaler():
    model_path = configs.MODEL_PATH
    scaler_path = configs.SCALER_PATH
    data_path = configs.COLLECTED_DATA_PATH
    #threshold = configs.THRESHOLD
    #deployment_name = configs.DEPLOYMENT_NAME
    threshold = os.getenv("THRESHOLD", configs.THRESHOLD)
    threshold = int(threshold)
    deployment_name = os.getenv('DEPLOYMENT_NAME', configs.DEPLOYMENT_NAME)
    get_metric()
    pred_pods = executor.provisioning(threshold, model_path, scaler_path, data_path)
    cur_pods = executor.get_number_running_pod(deployment_name)
    if pred_pods == cur_pods:
        print("Do nothing")
    elif pred_pods > cur_pods:
        replicas = pred_pods
        cmd = 'kubectl scale deployment/{} --replicas={}'.format(deployment_name, replicas)
        print("Scale up deployment: {} from {} to {}  \n".format(deployment_name,cur_pods, replicas))
        os.system(cmd)
    else:
        replicas = pred_pods
        if replicas > 0:
            cmd = 'kubectl scale deployment/{} --replicas={}'.format(deployment_name, replicas)
            print("Scale down deployment: {} from {} down to {}  \n".format(deployment_name, cur_pods, replicas))
            time.sleep(12)
            os.system(cmd)
def scalerfirst():
    model_path = configs.MODEL_PATH
    scaler_path = configs.SCALER_PATH
    data_path = configs.COLLECTED_DATA_PATH
    #threshold = configs.THRESHOLD
    #deployment_name = configs.DEPLOYMENT_NAME
    threshold = os.getenv("THRESHOLD", configs.THRESHOLD)
    threshold = int(threshold)
    deployment_name = os.getenv('DEPLOYMENT_NAME', configs.DEPLOYMENT_NAME)
    #get_metric()
    pred_pods = executor.provisioning(threshold, model_path, scaler_path, data_path)
    cur_pods = executor.get_number_running_pod(deployment_name)
    if pred_pods == cur_pods:
        print("Do nothing")
    elif pred_pods > cur_pods:
        replicas = pred_pods
        cmd = 'kubectl scale deployment/{} --replicas={}'.format(deployment_name, replicas)
        print("Scale up deployment: {} from {} to {}  \n".format(deployment_name,cur_pods, replicas))
        os.system(cmd)
    else:
        replicas = pred_pods
        if replicas > 0:
            cmd = 'kubectl scale deployment/{} --replicas={}'.format(deployment_name, replicas)
            print("Scale down deployment: {} from {} down to {}  \n".format(deployment_name, cur_pods, replicas))
            os.system(cmd)

if __name__ == '__main__':
    #schedule.every(25).seconds.do(get_metric)
    #schedule.every(30).seconds.do(scaler)
    #scalerfirst()
    schedule.every().minute.at(":00").do(scaler)
    schedule.every().minute.at(":30").do(scaler)
    while True:
        schedule.run_pending()
        time.sleep(1)


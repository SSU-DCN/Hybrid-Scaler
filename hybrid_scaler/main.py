import schedule
import time
import os
from configs import configs
import requests
import csv
import rolling_update
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
            print("collected rps = {}".format(test[0]))
            writer.writerow(test)
def scaler():
    get_metric()
    rolling_update.rolling_update_deployment()

if __name__ == '__main__':
    schedule.every().minute.at(":00").do(scaler)
    schedule.every().minute.at(":30").do(scaler)
    while True:
        schedule.run_pending()
        time.sleep(1)


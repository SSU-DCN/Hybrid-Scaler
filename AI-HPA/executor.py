import os
import predict
from configs import configs
import dataprocessing
import requests
import math

def get_number_running_pod(deployment_name):
    q = 'count(kube_pod_container_status_running{' + 'container="{}"'.format(deployment_name) + '}) by (container)'
    response = requests.get('{0}/api/v1/query'.format(configs.PROMETHEUS_URL), params={'query': q})
    if bool(response.json()['data']['result']):
        results = response.json()['data']['result'][0]['value'][1]
        results = int(results)
    return results
def predict_request_rate(model_path, scaler_path, data_path):
    loaded_model = predict.load_model(model_path)
    loaded_scaler = predict.load_scaler(scaler_path)
    if os.path.exists(data_path):
        df, check = dataprocessing.get_predict_data(data_path)
        if check >= configs.N_STEPS_IN:
            scaled_df = loaded_scaler.transform(df)
            sequense = dataprocessing.split_predict_sequences(scaled_df)
            future_request_value = predict.prediction(loaded_model, loaded_scaler, sequense)
    return future_request_value
def provisioning(threshold, model_path, scaler_path, data_path):
    loaded_model = predict.load_model(model_path)
    loaded_scaler = predict.load_scaler(scaler_path)
    if os.path.exists(data_path):
        df, check = dataprocessing.get_predict_data(data_path)
        if check >= configs.N_STEPS_IN:
            scaled_df = loaded_scaler.transform(df)
            sequense = dataprocessing.split_predict_sequences(scaled_df)
            future_request_value = predict.prediction(loaded_model, loaded_scaler, sequense)
            future_request_value = list(future_request_value.flatten())
    a = future_request_value[0]
    number_pred_pods = math.ceil(a / threshold)
    return number_pred_pods






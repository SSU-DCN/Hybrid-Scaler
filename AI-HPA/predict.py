import matplotlib.pyplot as plt
import numpy as np
from tensorflow import keras
import joblib

def load_model(path):
    return keras.models.load_model(path)

def load_scaler(path):
    return joblib.load(path)

def prediction(model, scaler, sequence):
    predict_value = model.predict(sequence)
    predict_value_scaled = scaler.inverse_transform(predict_value)
    return predict_value_scaled

def evaluate_prediction(predictions, actual, model_name):
    errors = predictions - actual
    mse = np.square(errors).mean()
    rmse = np.sqrt(mse)
    mae = np.abs(errors).mean()
    print(model_name + ':')
    print('Mean Absolute Error: {:.4f}'.format(mae))
    print('Root Mean Square Error: {:.4f}'.format(rmse))
    print('')

def plot_future(prediction, actual_value, name):
    plt.plot(actual_value, c = 'b', label = "Actual Value")
    plt.plot(prediction, c = 'r', label = "Prediction")
    plt.xlabel("Timesteps")
    plt.ylabel("CPU Usage - %")
    plt.title(name)
    plt.legend()
    plt.show()
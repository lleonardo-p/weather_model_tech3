import sys
import re
import json
import xgboost
import numpy as np
import joblib  # Para carregar o modelo serializado


# Função para tratar a string
def convert_to_valid_json(input_string):
    # Substituir as chaves sem aspas para estarem com aspas duplas
    input_string = re.sub(r'(\w+):', r'"\1":', input_string)
    return input_string

# Função para carregar o modelo serializado
def load_model(model_file):
    try:
        model = joblib.load(model_file)
        return model
    except Exception as e:
        print(f"Erro ao carregar o modelo: {e}")
        sys.exit(1)

# Função para predizer a temperatura com base no JSON de entrada
def predict_temperature(input_json, model):
    # Carregar os dados do JSON passado como argumento
    try:
        data = json.loads(input_json)
    except json.JSONDecodeError as e:
        print(f"Erro ao carregar JSON: {e}")
        return
    
    # Prepara os dados para o modelo (removendo "temperature_2m", pois é a variável alvo)
    input_data = np.array([[
        data["rain"],
        data["is_day"],
        data["cloud_cover"],
        data["weather_code"],
        data["precipitation"],
        data["wind_speed_10m"],
        data["wind_direction_10m"],
        data["apparent_temperature"],
        data["relative_humidity_2m"]
    ]])

    # Prever a temperatura usando o modelo carregado
    predicted_temperature = model.predict(input_data)
    
    print(f"Temperatura prevista: {predicted_temperature[0]} °C")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Por favor, forneça o caminho para o modelo serializado e um JSON como argumento.")
        sys.exit(1)

    # Carregar o modelo serializado
    model_file = sys.argv[1]
    model = load_model(model_file)

    # Receber o JSON como argumento
    input_json = sys.argv[2]
    print(input_json)
    input_json = convert_to_valid_json(input_json)
    print(input_json)
    print(type(input_json))


    # Fazer a predição
    predict_temperature(input_json, model)

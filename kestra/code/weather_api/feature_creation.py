import pandas as pd
from sqlalchemy import create_engine
import argparse
from kestra import Kestra
import re

# Função para tratar a string
def convert_to_valid_json(input_string):
    # Substituir as chaves sem aspas para estarem com aspas duplas
    input_string = re.sub(r'(\w+):', r'"\1":', input_string)
    return input_string

def save_to_feature_store(data: dict, db_url: str):
    """
    Recebe um dicionário com dados climáticos, transforma em DataFrame,
    calcula médias móveis das últimas 6 horas e salva no Feature Store (PostgreSQL).
    """
    # Criar DataFrame
    print(f"Data: {data}")
    df = pd.DataFrame(data,index=[0])
    print(f"aqui {df}")
    print(df.columns)
    df['time'] = pd.to_datetime(df['time'], unit='s')  # Converter para datetime
    df.set_index('time', inplace=True)  # Definir como índice

    # Ordenar os dados por tempo
    df = df.sort_values(by="time")

    # Calcular médias móveis das últimas 6 horas
    df['wind_speed_6h_mean'] = df['wind_speed_10m'].rolling('6h', min_periods=1).mean()
    df['precipitation_6h_mean'] = df['precipitation'].rolling('6h', min_periods=1).mean()
    df['temperature_6h_mean'] = df['temperature_2m'].rolling('6h', min_periods=1).mean()

    # Remover NaNs iniciais
    df = df.dropna()

    # Conectar ao banco de dados
    engine = create_engine("postgresql://kestra:k3str4@host.docker.internal:5432/tech3")
    print(df.head())

    # Salvar no PostgreSQL (Feature Store)
    df.to_sql("feature_store", engine, if_exists="append")

    print("Dados salvos com sucesso no Feature Store!")
    df.reset_index(inplace=True)
    df['time'] = df['time'].dt.strftime('%Y-%m-%d %H:%M:%S')
    dict_result = df.to_dict()
    return Kestra.outputs(dict_result)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Salvar dados no Feature Store")
    parser.add_argument("--data", type=str, required=True, help="Dicionário de dados em formato JSON")
    parser.add_argument("--db_url", type=str, required=True, help="String de conexão com PostgreSQL")

    args = parser.parse_args()

    # Converter string JSON para dicionário
    data_dict = convert_to_valid_json(args.data)
    print(f"data_dic {data_dict}")
    print(f"data_dic {type(data_dict)}")
    import json
    data_dict = json.loads(data_dict)


    save_to_feature_store(data_dict, args.db_url)
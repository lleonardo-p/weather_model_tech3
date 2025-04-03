import pandas as pd
import joblib
from sqlalchemy import create_engine
from sklearn.ensemble import RandomForestRegressor

def fetch_latest_data(engine, n=1):
    """
    Busca os n registros mais recentes da tabela 'feature_store'.
    """
    query = f" SELECT * FROM feature_store ORDER BY created_at DESC LIMIT {n};"
    # Consultar o banco de dados
    df = pd.read_sql(query, engine)
    return df

def preprocess_data(df):
    """
    Realiza o pré-processamento dos dados antes de alimentar no modelo.
    """
    # Excluir colunas que não são necessárias para o modelo
    columns_to_keep = [
        'relative_humidity_2m', 'apparent_temperature', 'precipitation', 'rain',
        'weather_code', 'cloud_cover', 'wind_direction_10m', 'wind_speed_10m',
        'is_day', 'wind_speed_6h_mean', 'precipitation_6h_mean', 'temperature_6h_mean'
    ]

    df = df[columns_to_keep]  # Filtra o DataFrame para manter apenas as colunas 
    
    # Certificar-se de que os dados estão no formato correto
    df.fillna(0, inplace=True)  # Preencher valores nulos com 0, se necessário
    
    return df

def load_model(model_path):
    """
    Carrega o modelo serializado (exemplo: XGBoost, Random Forest, etc.).
    """
    model = joblib.load(model_path)  # Carregar o modelo XGBoost com joblib
    return model

def make_predictions(model, df):
    """
    Realiza previsões utilizando o modelo carregado (XGBoost).
    """
    # Converter o DataFrame para DMatrix, que é o formato usado pelo XGBoost
    predictions = model.predict(df)
    return predictions

def save_predictions_to_db(engine, predictions):
    """
    Salva as previsões no banco de dados na tabela 'temperature_predictions'.
    """
    # Criar um DataFrame com as previsões
    prediction_data = pd.DataFrame({
        'predicted_temperature': predictions
    })
    
    # Inserir as previsões na tabela temperature_predictions
    prediction_data.to_sql('temperature_predictions', engine, if_exists='append', index=False)
    print("Previsões salvas no banco de dados com sucesso!")

if __name__ == "__main__":
    # Configurar conexão com o banco de dados
    DB_URL = "postgresql://kestra:k3str4@host.docker.internal:5432/tech3"
    engine = create_engine(DB_URL)

    # Buscar os dados mais recentes
    df = fetch_latest_data(engine, n=1)
    print("Dados brutos carregados:")
    print(df.head())

    # Pré-processar os dados
    df_processed = preprocess_data(df)
    print("Dados processados para o modelo:")
    print(df_processed.head())

    # Carregar modelo serializado
    model_path = "weather_api/model.pkl" # Caminho do modelo salvo
    model = load_model(model_path)

    # Fazer previsões
    predictions = make_predictions(model, df_processed)
    print("Previsões:")
    print(predictions)

    # Salvar as previsões no banco de dados
    save_predictions_to_db(engine, predictions)

from flask import Flask, jsonify
from sqlalchemy import create_engine
import pandas as pd
from flask_cors import CORS  # Importa o CORS

app = Flask(__name__)
CORS(app)  # Ativa CORS para todas as rotas

# Configurar conexão com o banco de dados
DB_URL = "postgresql://kestra:k3str4@localhost:5432/tech3"
engine = create_engine(DB_URL)

@app.route('/latest_prediction', methods=['GET'])
def get_latest_prediction():
    """
    Endpoint para retornar a previsão mais recente de temperatura.
    """
    query = """
    SELECT predicted_temperature, created_at
    FROM temperature_predictions
    ORDER BY created_at DESC
    LIMIT 1;
    """
    # Consultar o banco de dados
    df = pd.read_sql(query, engine)

    # Verificar se há dados
    if df.empty:
        return jsonify({"message": "No predictions found."}), 404

    # Obter o valor da última predição
    latest_prediction = df.iloc[0]
    return jsonify({
        "predicted_temperature": latest_prediction["predicted_temperature"],
        "created_at": latest_prediction["created_at"].strftime('%Y-%m-%d %H:%M:%S')
    })

if __name__ == '__main__':
    app.run(debug=True)

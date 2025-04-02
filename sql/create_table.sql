CREATE TABLE feature_store (
    id SERIAL PRIMARY KEY,
    rain FLOAT,
    time TIMESTAMP,  -- Alterado de BIGINT para TIMESTAMP
    is_day FLOAT,
    cloud_cover FLOAT,
    weather_code FLOAT,
    precipitation FLOAT,
    temperature_2m FLOAT,
    wind_speed_10m FLOAT,
    wind_direction_10m FLOAT,
    apparent_temperature FLOAT,
    relative_humidity_2m FLOAT,
    -- Features agregadas das últimas 6 horas
    wind_speed_6h_mean FLOAT,
    precipitation_6h_mean FLOAT,
    temperature_6h_mean FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Adicionado para registrar o momento de criação
);

CREATE TABLE temperature_predictions (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    predicted_temperature FLOAT
);

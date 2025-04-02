# 3º Tech Challenge - Processo de Previsão de Temperatura

Este projeto visa desenvolver um processo de previsão de temperatura utilizando dados climáticos históricos e dados em tempo real capturados a partir de uma API pública. O objetivo é prever a temperatura ambiente com base em variáveis como umidade relativa, precipitação, velocidade do vento e pressão atmosférica.

## Etapas do Processo

### 1. Análise Exploratória de Dados (EDA)

A primeira etapa do projeto consiste na coleta e análise dos dados históricos de temperatura e variáveis climáticas para compreender padrões e relações entre as variáveis. Durante essa fase, foram realizadas:

- **Visualização de distribuições** para entender como cada variável se comporta.
- **Análise de correlação** entre variáveis climáticas e temperatura.
- **Identificação de outliers** e tratamento de dados inconsistentes.

Abaixo, alguns exemplos das visualizações obtidas:

![Gráfico de distribuição](documentation/img/dist_serie.png)
![Matriz de correlação](documentation/img/corr_features.png)

### 2. Treinamento e Avaliação de Modelos

A segunda etapa consistiu no treinamento de modelos de regressão para prever a temperatura ambiente. Diversos modelos de aprendizado de máquina foram avaliados para determinar o melhor desempenho com base nas métricas:

- **Erro Quadrático Médio (RMSE)**: Mede a diferença entre os valores previstos e reais.
- **Coeficiente de Determinação (R²)**: Avalia o quão bem o modelo explica a variabilidade dos dados.

Abaixo, um resumo das avaliações dos modelos:

![Comparativo de Modelos](documentation/img/teste_modelos.png)

### 3. Fluxo de Dados em Tempo Real

- **Captura de Dados Climáticos:**
  Utilizando a [API Pública do Open-Meteo](https://open-meteo.com/), dados climáticos são capturados a cada 15 minutos. 

- **Persistência dos Dados:**
  Os dados capturados são armazenados em um banco de dados SQL para acesso e análise contínua.

- **Predição de Temperatura:**
  O modelo treinado é utilizado para prever a temperatura ambiente com base nos dados mais recentes.

## Ferramentas Utilizadas

- **Kestra:** Orquestração de workflows para automação dos processos de captura, armazenamento e predição de dados climáticos.
- **Python:** Principal linguagem para processamento de dados, treinamento de modelos e análise.
- **Bibliotecas:**
  - **Pandas**: Manipulação e análise de dados.
  - **NumPy**: Cálculos numéricos e operações com arrays.
  - **Scikit-learn**: Modelos de aprendizado de máquina.
  - **Seaborn e Matplotlib**: Visualização de dados.

## Conclusão

Este projeto combina análise de dados históricos com dados em tempo real para previsão de temperatura ambiente. A utilização de aprendizado de máquina permitiu construir um modelo preciso, enquanto a orquestração com Kestra garantiu um fluxo eficiente e automatizado para coleta, armazenamento e previsão dos dados.
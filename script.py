import requests
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import os
import csv
import plotly.graph_objects as go

# Configurações
API_KEY = "a1adb9102ba0f2def21bce903fc86912"  # Sua chave da API
CITY = "Taboão da Serra,BR"  # Cidade e país
FOLDER_PATH = "dataset"
FILE_PATH = os.path.join(FOLDER_PATH, "dados_climaticos.csv")

# Criar pasta caso não exista
os.makedirs(FOLDER_PATH, exist_ok=True)

# Função para obter dados da API
def get_weather_data(api_key, city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        return temperature, humidity
    else:
        messagebox.showerror("Erro", f"Erro ao acessar a API: {response.status_code}")
        return None, None

# Função para salvar dados no CSV
def save_to_csv(filepath, date_time, temperature, humidity):
    with open(filepath, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date_time, temperature, humidity])

# Função para carregar dados do CSV
def load_csv(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r") as file:
        reader = csv.reader(file)
        next(reader)  # Ignora o cabeçalho
        data = list(reader)
    return data

# Função para gerar o gráfico com Plotly
def plot_graph(data):
    dates = [datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S") for row in data]
    temperatures = [float(row[1]) for row in data]
    humidities = [float(row[2]) for row in data]

    fig = go.Figure()

    # Adicionando as linhas de temperatura e umidade
    fig.add_trace(go.Scatter(x=dates, y=temperatures, mode="lines+markers", name="Temperatura (°C)"))
    fig.add_trace(go.Scatter(x=dates, y=humidities, mode="lines+markers", name="Umidade (%)"))

    # Configurando o layout do gráfico
    fig.update_layout(
        title="Histórico de Temperatura e Umidade - Últimos 20 dias",
        xaxis_title="Data e Hora",
        yaxis_title="Valores",
        template="plotly_dark",  # Tema dark
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
    )
    fig.show()

# Função para processar os dados quando o botão é clicado
def process_data():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    temperature, humidity = get_weather_data(API_KEY, CITY)

    if temperature is not None and humidity is not None:
        save_to_csv(FILE_PATH, current_time, temperature, humidity)

        # Carregar últimos 20 dias de dados
        all_data = load_csv(FILE_PATH)
        last_20_days = [
            row
            for row in all_data
            if datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S") >= datetime.now() - timedelta(days=20)
        ]

        # Mostrar no gráfico
        plot_graph(last_20_days)

# Interface gráfica com tkinter
def create_gui():
    root = tk.Tk()
    root.title("Consulta Climática")

    frame = tk.Frame(root)
    frame.pack(pady=20)

    tk.Label(frame, text="Clique no botão para obter dados de clima").pack()

    btn = tk.Button(frame, text="Gerar Informação", command=process_data)
    btn.pack(pady=10)

    root.mainloop()

# Executar a aplicação
if __name__ == "__main__":
    # Criar o arquivo CSV se não existir
    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["datetime", "temperature", "humidity"])

    # Iniciar a GUI
    create_gui()

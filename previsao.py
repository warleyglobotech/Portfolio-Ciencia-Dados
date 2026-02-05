import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# --- 1. CONFIGURAÇÕES ---
# O nome exato do arquivo que está na sua pasta (vimos no comando dir)
ARQUIVO_DADOS = "Forecast.xlsx - media_movel.csv"

print(f"--> Tentando ler o arquivo: {ARQUIVO_DADOS}")

try:
    # --- 2. LER DADOS ---
    df = pd.read_csv(ARQUIVO_DADOS)
    print("--> Arquivo lido com sucesso!")
    
    # Limpeza: Pegar a coluna 'Real' (que é onde estão os dados nesse CSV)
    dados = df[['Real']].dropna()
    dados.columns = ['Vendas'] # Renomear para facilitar
    dados = dados.reset_index(drop=True)

    # --- 3. CRIAR PREVISÃO ---
    print("--> Calculando previsão inteligente...")
    # Criar modelo Holt-Winters
    modelo = ExponentialSmoothing(dados['Vendas'], seasonal_periods=4, trend='add', seasonal='add').fit()
    
    # Prever 6 passos à frente
    futuro = modelo.forecast(6)

    # --- 4. GERAR GRÁFICO ---
    print("--> Desenhando gráfico...")
    plt.figure(figsize=(10, 6))
    
    # Linha preta (Passado)
    plt.plot(dados.index, dados['Vendas'], label='Histórico Real', color='black', marker='o')
    # Linha verde (Futuro)
    plt.plot(futuro.index, futuro, label='Previsão Futura', color='green', marker='D', linestyle='--')
    
    plt.title('Previsão de Demanda (Pós-Graduação AMD)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Salvar
    plt.savefig('grafico_atividade3.png')
    print("\nSUCESSO TOTAL! 🚀")
    print("Abra a imagem 'grafico_atividade3.png' que apareceu na esquerda.")

except FileNotFoundError:
    print("\n❌ ERRO: O Python não achou o arquivo csv.")
    print("Confira se o nome 'Forecast.xlsx - media_movel.csv' está correto na pasta.")
except KeyError:
    print("\n❌ ERRO: O Python não achou a coluna 'Real'.")
    print("Verifique se o seu CSV tem um cabeçalho escrito 'Real'.")
except Exception as e:
    print(f"\n❌ ERRO INESPERADO: {e}")
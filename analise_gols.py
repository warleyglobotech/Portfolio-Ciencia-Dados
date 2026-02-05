import pandas as pd
import matplotlib.pyplot as plt

# --- 1. CARREGAR DADOS ---
print("Carregando base de gols...")
df_gols = pd.read_csv("campeonato-brasileiro-gols.csv")

# --- 2. ANÁLISE: O REI DO PÊNALTI ---
# Filtra só o que é Penalty
penaltis = df_gols[df_gols['tipo_de_gol'] == 'Penalty']
# Conta os artilheiros
top_batedores = penaltis['atleta'].value_counts().head(5)

print("\n--- TOP 5 BATEDORES DE PÊNALTI ---")
print(top_batedores)

# Gráfico de Barras Horizontal
plt.figure(figsize=(10, 6))
top_batedores.sort_values().plot(kind='barh', color='#2ecc71') # Verde gramado
plt.title('Reis do Pênalti (Pontos Corridos)')
plt.xlabel('Gols de Pênalti')
plt.tight_layout()
plt.savefig('grafico_penaltis.png')
print("Gráfico 'grafico_penaltis.png' salvo!")

# --- 3. ANÁLISE: O MINUTO FATAL ---
# Limpeza de dados: converter "90+2" para "90" para agrupar melhor
def limpar_minuto(m):
    try:
        if isinstance(m, str) and '+' in m:
            return int(m.split('+')[0])
        return int(m)
    except:
        return 0

df_gols['minuto_limpo'] = df_gols['minuto'].apply(limpar_minuto)

# Agrupa e conta
gols_por_minuto = df_gols['minuto_limpo'].value_counts().sort_index()

print("\n--- MOMENTOS MAIS PERIGOSOS ---")
print(gols_por_minuto.sort_values(ascending=False).head(3))

# Gráfico de Linha (A "Curva da Emoção")
plt.figure(figsize=(12, 5))
gols_por_minuto.plot(kind='line', color='#3498db', linewidth=2)
plt.title('Em qual minuto saem os gols?')
plt.xlabel('Minuto do Jogo')
plt.ylabel('Quantidade de Gols')
plt.grid(True, alpha=0.3) # Gradezinha suave
plt.savefig('grafico_minutos.png')
print("Gráfico 'grafico_minutos.png' salvo!")
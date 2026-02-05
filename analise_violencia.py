import pandas as pd
import matplotlib.pyplot as plt

# --- 1. CARREGAR OS DADOS ---
print("Carregando base de dados...")
df_cartoes = pd.read_csv("campeonato-brasileiro-cartoes.csv")
df_partidas = pd.read_csv("campeonato-brasileiro-full.csv")

# --- 2. ANÁLISE 1: OS MAIS INDISCIPLINADOS ---
# Filtra só cartões vermelhos
vermelhos = df_cartoes[df_cartoes['cartao'] == 'Vermelho']
# Conta quantos cada time tomou
top_violentos = vermelhos['clube'].value_counts().head(5)

print("\n--- TOP 5 TIMES COM MAIS CARTÕES VERMELHOS ---")
print(top_violentos)

# Gerar Gráfico de Barras
plt.figure(figsize=(10, 6))
top_violentos.plot(kind='bar', color='#e74c3c') # Cor vermelha
plt.title('Times com mais Cartões Vermelhos (Histórico)')
plt.ylabel('Qtd Cartões')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('grafico_violentos.png') # Salva a imagem na pasta
print("Gráfico 'grafico_violentos.png' salvo com sucesso!")


# --- 3. ANÁLISE 2: IMPACTO NO RESULTADO ---
# Conta cartões por jogo e time
cartoes_por_jogo = vermelhos.groupby(['partida_id', 'clube']).size().reset_index(name='qtd_vermelhos')

# Cruza com a tabela de partidas para ver o vencedor
dados_cruzados = pd.merge(cartoes_por_jogo, df_partidas, left_on='partida_id', right_on='ID', how='inner')

# Função para decidir se ganhou, perdeu ou empatou
def verificar_resultado(linha):
    time_punido = linha['clube']
    vencedor_jogo = linha['vencedor']
    
    if vencedor_jogo == '-': 
        return 'Empate'
    elif vencedor_jogo == time_punido:
        return 'Venceu (Heroico)'
    else:
        return 'Perdeu'

# Aplica a lógica
dados_cruzados['desfecho'] = dados_cruzados.apply(verificar_resultado, axis=1)

# Conta os resultados
impacto = dados_cruzados['desfecho'].value_counts(normalize=True) * 100

print("\n--- O QUE ACONTECE APÓS UMA EXPULSÃO? ---")
print(impacto.round(1).astype(str) + '%')

# Gerar Gráfico de Pizza
plt.figure(figsize=(8, 8))
impacto.plot(kind='pie', autopct='%1.1f%%', colors=['#ff9999','#66b3ff','#99ff99'])
plt.title('Resultado do jogo após ter jogador expulso')
plt.ylabel('')
plt.savefig('grafico_impacto.png')
print("Gráfico 'grafico_impacto.png' salvo com sucesso!")


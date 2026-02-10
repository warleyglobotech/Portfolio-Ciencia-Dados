import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# --- 1. GERADOR DE DADOS (SIMULAÇÃO) ---
# Como não temos o arquivo real, vamos criar um "Mock" de um perfil de Tech
print("--> Gerando dados simulados do Instagram...")

np.random.seed(42) # Para os números serem sempre os mesmos
datas = pd.date_range(start='2025-01-01', periods=50, freq='3D') # 50 posts, um a cada 3 dias
tipos = ['Reels', 'Carrossel', 'Foto Estática', 'Reels', 'Carrossel'] # Pesos diferentes

dados = {
    'Data': datas,
    'Tipo_Post': np.random.choice(tipos, size=50),
    'Likes': np.random.randint(50, 500, size=50),
    'Comentarios': np.random.randint(2, 50, size=50),
    'Salvamentos': np.random.randint(0, 100, size=50),
    'Alcance': np.random.randint(1000, 10000, size=50)
}

df = pd.DataFrame(dados)

# Ajuste: Reels costumam ter mais alcance e likes (vamos simular isso)
df.loc[df['Tipo_Post'] == 'Reels', 'Likes'] += 300
df.loc[df['Tipo_Post'] == 'Reels', 'Alcance'] += 5000
df.loc[df['Tipo_Post'] == 'Carrossel', 'Salvamentos'] += 50

# Salva para você ver o arquivo depois se quiser
df.to_csv('dados_instagram.csv', index=False)
print("✅ Arquivo 'dados_instagram.csv' criado com sucesso!")

# --- 2. ANÁLISE DE DADOS (ETL) ---
print("--> Calculando Engajamento...")

# Criar a métrica "Taxa de Engajamento"
# Fórmula comum: (Likes + Comentarios + Salvamentos) / Alcance * 100
df['Interacoes_Totais'] = df['Likes'] + df['Comentarios'] + df['Salvamentos']
df['Engajamento_Pct'] = (df['Interacoes_Totais'] / df['Alcance']) * 100

# Agrupar por Tipo de Post
performance_tipo = df.groupby('Tipo_Post')[['Interacoes_Totais', 'Engajamento_Pct', 'Alcance']].mean().sort_values('Engajamento_Pct', ascending=False)

print("\n--- RESUMO DA PERFORMANCE ---")
print(performance_tipo)

# --- 3. VISUALIZAÇÃO (DASHBOARD) ---
print("\n--> Gerando gráficos...")
plt.figure(figsize=(14, 6))

# Gráfico 1: Qual formato engaja mais? (Barras)
plt.subplot(1, 2, 1)
sns.barplot(x=performance_tipo.index, y=performance_tipo['Interacoes_Totais'], palette='magma')
plt.title('Média de Interações por Formato')
plt.ylabel('Total de Interações (Likes + Coment + Salvos)')
plt.xlabel('Formato do Post')

# Gráfico 2: Evolução no Tempo (Linha)
plt.subplot(1, 2, 2)
sns.lineplot(data=df, x='Data', y='Interacoes_Totais', hue='Tipo_Post', marker='o')
plt.title('Evolução das Interações ao Longo do Tempo')
plt.xticks(rotation=45)
plt.ylabel('Interações')

plt.tight_layout()
plt.savefig('insights_instagram.png')
print("🚀 SUCESSO! Abra a imagem 'insights_instagram.png' para ver os resultados.")
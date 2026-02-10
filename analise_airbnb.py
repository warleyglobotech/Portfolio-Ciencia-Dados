import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- CONFIGURAÇÃO ---
# O arquivo que você tem é o CSV normal (resumido), não o GZ
ARQUIVO = "listings.csv"

print(f"--> Lendo arquivo: {ARQUIVO}...")

try:
    # Lê o CSV direto (sem compressão)
    df = pd.read_csv(ARQUIVO)
    print(f"✅ SUCESSO! Carregamos {df.shape[0]} linhas.")

    # --- LIMPEZA E AJUSTES ---
    print("--> Organizando colunas...")

    # Renomear para português
    # No seu arquivo, a coluna de bairro se chama 'neighbourhood' (no outro era neighbourhood_cleansed)
    df = df.rename(columns={
        'neighbourhood': 'Bairro',
        'price': 'Preco',
        'room_type': 'Tipo'
    })

    # Tratamento do Preço
    # No seu arquivo, o preço JÁ É NÚMERO (não tem $), então não precisa substituir texto
    # Apenas removemos os vazios (NaN)
    df = df.dropna(subset=['Preco'])
    
    # Filtrar: Preços menores que 5000 (para tirar mansões/erros) e maiores que 0
    df = df[(df['Preco'] < 5000) & (df['Preco'] > 0)]

    # --- GRÁFICOS ---
    print("--> Gerando gráficos...")
    plt.figure(figsize=(12, 6))

    # Gráfico 1: Onde tem mais imóveis?
    plt.subplot(1, 2, 1)
    top_bairros = df['Bairro'].value_counts().head(10)
    sns.barplot(x=top_bairros.values, y=top_bairros.index, palette='Blues_d')
    plt.title('Top 10 Bairros (Quantidade)')
    plt.xlabel('Nº de Imóveis')

    # Gráfico 2: Onde é mais caro?
    plt.subplot(1, 2, 2)
    # Calcula preço médio dos top 10
    preco_bairro = df[df['Bairro'].isin(top_bairros.index)].groupby('Bairro')['Preco'].mean().sort_values(ascending=False)
    sns.barplot(x=preco_bairro.values, y=preco_bairro.index, palette='Greens_d')
    plt.title('Preço Médio (R$) nos Top Bairros')
    plt.xlabel('Preço (R$)')

    plt.tight_layout()
    plt.savefig('grafico_airbnb_rj.png')
    print("🎉 TUDO PRONTO! Abra a imagem 'grafico_airbnb_rj.png' na pasta.")

except FileNotFoundError:
    print(f"❌ ERRO: O arquivo '{ARQUIVO}' não está na pasta.")
    print("Verifique se o nome do arquivo baixado é exatamente 'listings.csv'.")
except Exception as e:
    print(f"❌ Erro inesperado: {e}")
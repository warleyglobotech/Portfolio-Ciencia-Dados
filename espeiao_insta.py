import instaloader
import pandas as pd
from datetime import datetime

# --- CONFIGURAÇÃO ---
PERFIL_ALVO = 'socialmlabs'  # <--- TROQUE PELO PERFIL QUE VOCÊ QUER (sem o @)
LIMITE_POSTS = 50         # Baixar apenas 50 para não ser bloqueado pelo Instagram

print(f"--> Iniciando a espionagem do perfil @{PERFIL_ALVO}...")
print("--> Isso pode levar alguns minutos. Aguarde...")

# Inicializa o Robô
L = instaloader.Instaloader()

# Dica: O Instaloader às vezes pede login para perfis muito grandes.
# Se der erro, tente um perfil menor ou rode novamente.

dados_lista = []

try:
    # Carrega o perfil
    perfil = instaloader.Profile.from_username(L.context, PERFIL_ALVO)

    # Loop pelos posts
    contador = 0
    for post in perfil.get_posts():
        if contador >= LIMITE_POSTS:
            break
        
        # Extrai os dados públicos
        dados_post = {
            'Data': post.date_local, # Data do post
            'Tipo': post.typename,   # GraphImage (Foto), GraphVideo (Vídeo), GraphSidecar (Carrossel)
            'Likes': post.likes,
            'Comentarios': post.comments,
            'Legenda': post.caption  # Texto do post
        }
        
        dados_lista.append(dados_post)
        contador += 1
        
        # Mostra progresso a cada 10 posts
        if contador % 10 == 0:
            print(f"   ... Baixados {contador} posts.")

    # --- SALVAR E ANALISAR ---
    if dados_lista:
        df = pd.DataFrame(dados_lista)
        
        # Salva em CSV para você usar depois se quiser
        nome_arquivo = f'dados_{PERFIL_ALVO}.csv'
        df.to_csv(nome_arquivo, index=False)
        print(f"✅ SUCESSO! Dados salvos em '{nome_arquivo}'.")

        # --- GERAÇÃO DE GRÁFICOS RÁPIDOS ---
        import matplotlib.pyplot as plt
        import seaborn as sns

        print("--> Gerando gráfico de análise...")
        
        # Criar coluna de Engajamento Total
        df['Engajamento'] = df['Likes'] + df['Comentarios']

        plt.figure(figsize=(12, 6))

        # Gráfico: Likes por Tipo de Mídia
        plt.subplot(1, 2, 1)
        sns.boxplot(x='Tipo', y='Likes', data=df, palette='viridis')
        plt.title(f'Distribuição de Likes por Formato (@{PERFIL_ALVO})')
        plt.yscale('log') # Escala logarítmica ajuda a ver melhor quando os números são gigantes

        # Gráfico: Evolução no Tempo
        plt.subplot(1, 2, 2)
        sns.lineplot(x='Data', y='Likes', data=df, marker='o', color='blue')
        plt.title('Evolução de Likes (Últimos 50 posts)')
        plt.xticks(rotation=45)

        plt.tight_layout()
        plt.savefig(f'analise_{PERFIL_ALVO}.png')
        print(f"📊 Gráfico salvo como 'analise_{PERFIL_ALVO}.png'. Abra para ver!")

    else:
        print("❌ Nenhum post encontrado. O perfil pode ser privado ou bloqueou o acesso.")

except Exception as e:
    print(f"❌ Ocorreu um erro: {e}")
    print("DICA: O Instagram bloqueia acessos anônimos frequentes.")
    print("Tente esperar alguns minutos ou mudar o perfil alvo.")
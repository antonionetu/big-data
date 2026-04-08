"""
Atividade Big Data — Velocidade de Internet Global
Análise do dataset: Internet Broadband and Mobile Speeds by Country
"""

# Dataset: https://www.kaggle.com/datasets/prasertk/internet-broadband-and-mobile-speeds-by-country

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats

# Configuração visual
plt.rcParams['figure.figsize'] = (12, 7)
plt.rcParams['font.size'] = 12
sns.set_style("whitegrid")

# ============================================================
# ETAPA 1 — Exploração Inicial
# ============================================================
print("=" * 60)
print("ETAPA 1 — EXPLORAÇÃO INICIAL DO DATASET")
print("=" * 60)

df = pd.read_csv("dados/broadband_speed.csv")

print("\n--- 5 primeiras linhas ---")
print(df.head().to_string())

print("\n--- Nomes das colunas ---")
for col in df.columns:
    print(f"  • {col}")

print("\n--- Tipos de dados ---")
print(df.dtypes.to_string())

print(f"\n--- Dimensões do dataset ---")
print(f"  Linhas: {df.shape[0]}")
print(f"  Colunas: {df.shape[1]}")

print("\n--- Valores nulos por coluna ---")
print(df.isnull().sum().to_string())

# ============================================================
# ETAPA 2 — Média e Mediana de Download por País
# ============================================================
print("\n" + "=" * 60)
print("ETAPA 2 — MÉDIA E MEDIANA DE DOWNLOAD")
print("=" * 60)

col_download = "Broadband Mbps"
col_upload = "Mobile Mbps"

# Tabela com velocidades por país (já é um valor por país)
tabela = df[["Country", col_download]].copy()
tabela.columns = ["País", "Download (Mbps)"]
tabela = tabela.sort_values("Download (Mbps)", ascending=False).reset_index(drop=True)

# Média e mediana globais
media_global = df[col_download].mean()
mediana_global = df[col_download].median()

print(f"\n--- Estatísticas Globais de Download ---")
print(f"  Média global:   {media_global:.2f} Mbps")
print(f"  Mediana global:  {mediana_global:.2f} Mbps")

print(f"\n--- Top 10 países com MAIOR velocidade de download ---")
top10 = tabela.head(10)
print(top10.to_string(index=False))

print(f"\n--- Top 10 países com MENOR velocidade de download ---")
bottom10 = tabela.tail(10)
print(bottom10.to_string(index=False))

# Adicionar média e mediana globais ao final da tabela e salvar
linha_media = pd.DataFrame({"País": ["MÉDIA GLOBAL"], "Download (Mbps)": [media_global]})
linha_mediana = pd.DataFrame({"País": ["MEDIANA GLOBAL"], "Download (Mbps)": [mediana_global]})
tabela_completa = pd.concat([tabela, linha_media, linha_mediana], ignore_index=True)
tabela_completa.to_csv("dados/media_mediana_download.csv", index=False, encoding="utf-8-sig")
print("\n[Salvo] dados/media_mediana_download.csv")

# ============================================================
# ETAPA 3 — Gráfico de Dispersão Download vs Upload (Mobile)
# ============================================================
print("\n" + "=" * 60)
print("ETAPA 3 — GRÁFICO DE DISPERSÃO")
print("=" * 60)

# Filtrar apenas países com dados de mobile
df_scatter = df.dropna(subset=[col_download, col_upload]).copy()

x = df_scatter[col_download].values
y = df_scatter[col_upload].values

# Regressão linear
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
linha_tendencia = slope * x + intercept
r_pearson = r_value

fig, ax = plt.subplots(figsize=(12, 8))
ax.scatter(x, y, alpha=0.6, edgecolors='black', linewidth=0.5, s=60, color='#2196F3')

# Ordenar para plotar a linha suave
ordem = np.argsort(x)
ax.plot(x[ordem], linha_tendencia[ordem], color='red', linewidth=2,
        label=f'Regressão Linear (r = {r_pearson:.3f})')

ax.set_xlabel("Velocidade de Download — Banda Larga (Mbps)", fontsize=13)
ax.set_ylabel("Velocidade de Upload — Mobile (Mbps)", fontsize=13)
ax.set_title("Dispersão: Velocidade de Download (Banda Larga) vs Upload (Mobile) por País",
             fontsize=14, fontweight='bold')
ax.legend(fontsize=12)
ax.text(0.05, 0.95, f"Correlação de Pearson: r = {r_pearson:.3f}\np-valor: {p_value:.2e}",
        transform=ax.transAxes, fontsize=11, verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

plt.tight_layout()
plt.savefig("graficos/scatter_download_upload/scatter_download_upload.png", dpi=300)
plt.close()
print(f"  Correlação de Pearson: r = {r_pearson:.3f}")
print("[Salvo] graficos/scatter_download_upload/scatter_download_upload.png")

# ============================================================
# ETAPA 4 — Histogramas de Distribuição
# ============================================================
print("\n" + "=" * 60)
print("ETAPA 4 — HISTOGRAMAS DE DISTRIBUIÇÃO")
print("=" * 60)

download = df[col_download].dropna()
upload = df[col_upload].dropna()

media_dl = download.mean()
mediana_dl = download.median()
media_ul = upload.mean()
mediana_ul = upload.median()

# 4a. Histograma de Download
fig, ax = plt.subplots(figsize=(12, 7))
ax.hist(download, bins=18, color='#2196F3', edgecolor='black', alpha=0.7, label='Download (Banda Larga)')
ax.axvline(media_dl, color='red', linestyle='--', linewidth=2, label=f'Média: {media_dl:.2f} Mbps')
ax.axvline(mediana_dl, color='green', linestyle='-', linewidth=2, label=f'Mediana: {mediana_dl:.2f} Mbps')
ax.set_xlabel("Velocidade de Download (Mbps)", fontsize=13)
ax.set_ylabel("Frequência", fontsize=13)
ax.set_title("Distribuição das Velocidades de Download (Banda Larga)", fontsize=14, fontweight='bold')
ax.legend(fontsize=11)
plt.tight_layout()
plt.savefig("graficos/histograma_download/histograma_download.png", dpi=300)
plt.close()
print("[Salvo] graficos/histograma_download/histograma_download.png")

# 4b. Histograma de Upload (Mobile)
fig, ax = plt.subplots(figsize=(12, 7))
ax.hist(upload, bins=18, color='#FF9800', edgecolor='black', alpha=0.7, label='Upload (Mobile)')
ax.axvline(media_ul, color='red', linestyle='--', linewidth=2, label=f'Média: {media_ul:.2f} Mbps')
ax.axvline(mediana_ul, color='green', linestyle='-', linewidth=2, label=f'Mediana: {mediana_ul:.2f} Mbps')
ax.set_xlabel("Velocidade Mobile (Mbps)", fontsize=13)
ax.set_ylabel("Frequência", fontsize=13)
ax.set_title("Distribuição das Velocidades Mobile", fontsize=14, fontweight='bold')
ax.legend(fontsize=11)
plt.tight_layout()
plt.savefig("graficos/histograma_upload/histograma_upload.png", dpi=300)
plt.close()
print("[Salvo] graficos/histograma_upload/histograma_upload.png")

# 4c. Histograma Comparativo
fig, ax = plt.subplots(figsize=(12, 7))
ax.hist(download, bins=18, color='#2196F3', edgecolor='black', alpha=0.5, label='Download (Banda Larga)')
ax.hist(upload, bins=18, color='#FF9800', edgecolor='black', alpha=0.5, label='Mobile')
ax.axvline(media_dl, color='blue', linestyle='--', linewidth=2, label=f'Média Download: {media_dl:.2f}')
ax.axvline(mediana_dl, color='blue', linestyle='-', linewidth=2, label=f'Mediana Download: {mediana_dl:.2f}')
ax.axvline(media_ul, color='darkorange', linestyle='--', linewidth=2, label=f'Média Mobile: {media_ul:.2f}')
ax.axvline(mediana_ul, color='darkorange', linestyle='-', linewidth=2, label=f'Mediana Mobile: {mediana_ul:.2f}')
ax.set_xlabel("Velocidade (Mbps)", fontsize=13)
ax.set_ylabel("Frequência", fontsize=13)
ax.set_title("Comparação: Distribuição Download (Banda Larga) vs Mobile", fontsize=14, fontweight='bold')
ax.legend(fontsize=10, loc='upper right')
plt.tight_layout()
plt.savefig("graficos/histograma_comparativo/histograma_comparativo.png", dpi=300)
plt.close()
print("[Salvo] graficos/histograma_comparativo/histograma_comparativo.png")

# ============================================================
# ETAPA 5 — Estatísticas Descritivas Complementares
# ============================================================
print("\n" + "=" * 60)
print("ETAPA 5 — ESTATÍSTICAS DESCRITIVAS COMPLETAS")
print("=" * 60)

for nome, serie in [("Download (Banda Larga)", download), ("Mobile", upload)]:
    print(f"\n--- {nome} ---")
    print(f"  Contagem:        {serie.count()}")
    print(f"  Média:           {serie.mean():.2f} Mbps")
    print(f"  Mediana:         {serie.median():.2f} Mbps")
    print(f"  Desvio Padrão:   {serie.std():.2f}")
    print(f"  Variância:       {serie.var():.2f}")
    print(f"  Mínimo:          {serie.min():.2f} Mbps")
    print(f"  1º Quartil (Q1): {serie.quantile(0.25):.2f} Mbps")
    print(f"  3º Quartil (Q3): {serie.quantile(0.75):.2f} Mbps")
    print(f"  Máximo:          {serie.max():.2f} Mbps")
    print(f"  Assimetria:      {serie.skew():.4f}")
    print(f"  Curtose:         {serie.kurtosis():.4f}")

print("\n" + "=" * 60)
print("ANÁLISE CONCLUÍDA — Todos os arquivos foram gerados!")
print("=" * 60)

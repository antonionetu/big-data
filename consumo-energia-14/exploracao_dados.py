"""
Atividade 14 — Consumo de Energia ao Longo do Tempo
Analise do dataset: World Energy Consumption
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats

plt.rcParams['figure.figsize'] = (12, 7)
plt.rcParams['font.size'] = 12
sns.set_style("whitegrid")

# ============================================================
# ETAPA 1 — Exploracao Inicial
# ============================================================
print("=" * 60)
print("ETAPA 1 — EXPLORACAO INICIAL DO DATASET")
print("=" * 60)

df = pd.read_csv("dados/dataset.csv")

print(f"\n--- Dimensoes do dataset ---")
print(f"  Linhas: {df.shape[0]}")
print(f"  Colunas: {df.shape[1]}")

print(f"\n--- 5 primeiras linhas (colunas-chave) ---")
cols_show = ['country', 'year', 'primary_energy_consumption',
             'coal_consumption', 'oil_consumption', 'gas_consumption',
             'nuclear_consumption', 'renewables_consumption']
print(df[cols_show].head().to_string())

print(f"\n--- Tipos de dados (amostra) ---")
for c in cols_show:
    print(f"  {c}: {df[c].dtype}")

print(f"\n--- Valores nulos (colunas principais) ---")
for c in cols_show:
    print(f"  {c}: {df[c].isnull().sum()}/{len(df)}")

print(f"\n--- Cobertura ---")
print(f"  Entidades unicas: {df['country'].nunique()}")
print(f"  Paises (com iso_code): {df[df['iso_code'].notna()]['country'].nunique()}")
print(f"  Periodo: {df['year'].min()} - {df['year'].max()}")

# ============================================================
# Preparar dados: apenas paises reais, com primary_energy
# ============================================================
paises = df[df['iso_code'].notna()].copy()

# Regioes para analise agregada
regioes_nomes = ['Africa', 'Asia', 'Europe', 'North America',
                 'South America', 'Oceania']
regioes = df[df['country'].isin(regioes_nomes)].copy()

# Colunas de consumo por fonte
fontes = {
    'Carvao': 'coal_consumption',
    'Petroleo': 'oil_consumption',
    'Gas Natural': 'gas_consumption',
    'Nuclear': 'nuclear_consumption',
    'Renovaveis': 'renewables_consumption',
    'Hidro': 'hydro_consumption',
}

# ============================================================
# ETAPA 2 — Questao A: Media de consumo por regiao e fonte
# ============================================================
print("\n" + "=" * 60)
print("ETAPA 2 — MEDIA DE CONSUMO POR REGIAO E FONTE DE ENERGIA")
print("=" * 60)

# Calcular media por regiao e fonte
resultados = []
for regiao in regioes_nomes:
    dados_regiao = regioes[regioes['country'] == regiao]
    for fonte_nome, fonte_col in fontes.items():
        media = dados_regiao[fonte_col].mean()
        resultados.append({
            'Regiao': regiao,
            'Fonte de Energia': fonte_nome,
            'Media de Consumo (TWh)': round(media, 2) if pd.notna(media) else None
        })

df_media = pd.DataFrame(resultados)
df_media = df_media.dropna(subset=['Media de Consumo (TWh)'])

# Tabela pivotada para visualizacao
tabela_pivot = df_media.pivot(index='Regiao', columns='Fonte de Energia',
                               values='Media de Consumo (TWh)')
print("\nMedia de consumo por regiao e fonte (TWh):")
print(tabela_pivot.to_string())

df_media.to_csv("dados/media_consumo.csv", index=False, encoding="utf-8-sig")
print("\n[Salvo] dados/media_consumo.csv")

# Grafico de barras agrupadas
fig, ax = plt.subplots(figsize=(14, 7))
tabela_pivot.plot(kind='bar', ax=ax, width=0.8)
ax.set_title("Media de Consumo de Energia por Regiao e Fonte", fontsize=14, fontweight='bold')
ax.set_xlabel("Regiao", fontsize=13)
ax.set_ylabel("Media de Consumo (TWh)", fontsize=13)
ax.legend(title="Fonte de Energia", fontsize=10, title_fontsize=11)
ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha='right')
plt.tight_layout()
plt.savefig("graficos/media_regiao_fonte/media_regiao_fonte.png", dpi=300)
plt.close()
print("[Salvo] graficos/media_regiao_fonte/media_regiao_fonte.png")

# ============================================================
# ETAPA 3 — Questao B: Grafico de dispersao (crescimento)
# ============================================================
print("\n" + "=" * 60)
print("ETAPA 3 — GRAFICO DE DISPERSAO: CONSUMO AO LONGO DO TEMPO")
print("=" * 60)

# Dados mundiais
mundo = df[df['country'] == 'World'].copy()
mundo = mundo.dropna(subset=['primary_energy_consumption'])

# Preparar dados por fonte para o scatter
fontes_mundo = {}
for fonte_nome, fonte_col in fontes.items():
    dados = mundo[['year', fonte_col]].dropna()
    if len(dados) > 0:
        fontes_mundo[fonte_nome] = dados

fig, ax = plt.subplots(figsize=(14, 8))
cores = ['#424242', '#FF8F00', '#1565C0', '#7B1FA2', '#2E7D32', '#0097A7']

# Primeiro: pontos do consumo total
ax.scatter(mundo['year'], mundo['primary_energy_consumption'],
           alpha=0.4, s=40, color='#E53935', marker='D', label='Total Primario')

# Fontes individuais
for i, (fonte_nome, dados) in enumerate(fontes_mundo.items()):
    col = list(fontes.values())[i]
    ax.scatter(dados['year'], dados[col], alpha=0.6, s=30,
               label=fonte_nome, color=cores[i])

# Linha de tendencia para consumo total
x_total = mundo['year'].values
y_total = mundo['primary_energy_consumption'].values
slope, intercept, r_val, p_val, _ = stats.linregress(x_total, y_total)
ax.plot(x_total, slope * x_total + intercept, color='red', linewidth=2,
        linestyle='--', label=f'Tendencia Total (r={r_val:.3f})')

ax.set_title("Crescimento do Consumo de Energia ao Longo dos Anos (Mundo)",
             fontsize=14, fontweight='bold')
ax.set_xlabel("Ano", fontsize=13)
ax.set_ylabel("Consumo de Energia (TWh)", fontsize=13)
ax.legend(fontsize=10, loc='upper left')
ax.text(0.02, 0.85, f"Correlacao (total vs ano): r = {r_val:.3f}",
        transform=ax.transAxes, fontsize=11,
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
plt.tight_layout()
plt.savefig("graficos/scatter_consumo_tempo/scatter_consumo_tempo.png", dpi=300)
plt.close()
print(f"  Correlacao consumo total vs ano: r = {r_val:.3f}")
print("[Salvo] graficos/scatter_consumo_tempo/scatter_consumo_tempo.png")

# ============================================================
# ETAPA 4 — Questao C: Variacoes sazonais / ciclicas
# ============================================================
print("\n" + "=" * 60)
print("ETAPA 4 — VARIACOES NO CONSUMO DE ENERGIA")
print("=" * 60)

# Dados anuais — analisar variacao percentual ano-a-ano
mundo_var = mundo[['year', 'primary_energy_consumption',
                   'energy_cons_change_pct']].dropna(subset=['energy_cons_change_pct'])

media_var = mundo_var['energy_cons_change_pct'].mean()
print(f"  Variacao media anual: {media_var:.2f}%")

# Identificar anos de queda
quedas = mundo_var[mundo_var['energy_cons_change_pct'] < 0].sort_values('energy_cons_change_pct')
print(f"  Anos com queda no consumo: {len(quedas)}")
print("\n  Maiores quedas:")
for _, row in quedas.head(5).iterrows():
    print(f"    {int(row['year'])}: {row['energy_cons_change_pct']:.2f}%")

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

# Grafico 1: Consumo total ao longo do tempo
ax1.plot(mundo['year'], mundo['primary_energy_consumption'],
         color='#1565C0', linewidth=2)
ax1.fill_between(mundo['year'], mundo['primary_energy_consumption'],
                 alpha=0.2, color='#1565C0')
ax1.set_title("Consumo Total de Energia Primaria — Mundo", fontsize=13, fontweight='bold')
ax1.set_ylabel("Consumo (TWh)", fontsize=12)

# Destacar periodos de queda
for _, row in quedas.iterrows():
    ax1.axvline(row['year'], color='red', alpha=0.15, linewidth=2)

# Grafico 2: Variacao percentual ano-a-ano
cores_bar = ['#EF5350' if v < 0 else '#42A5F5'
             for v in mundo_var['energy_cons_change_pct']]
ax2.bar(mundo_var['year'], mundo_var['energy_cons_change_pct'],
        color=cores_bar, width=0.8)
ax2.axhline(0, color='black', linewidth=0.5)
ax2.axhline(media_var, color='green', linewidth=1.5, linestyle='--',
            label=f'Media: {media_var:.2f}%')
ax2.set_title("Variacao Percentual Anual do Consumo de Energia — Mundo",
              fontsize=13, fontweight='bold')
ax2.set_xlabel("Ano", fontsize=12)
ax2.set_ylabel("Variacao (%)", fontsize=12)
ax2.legend(fontsize=11)

# Anotar eventos importantes
eventos = {
    1945: "Fim da\n2a Guerra",
    1973: "Crise do\nPetroleo",
    1979: "2a Crise\nPetroleo",
    2009: "Crise\nFinanceira",
    2020: "Pandemia\nCOVID-19"
}
for ano, texto in eventos.items():
    if ano in mundo_var['year'].values:
        val = mundo_var[mundo_var['year'] == ano]['energy_cons_change_pct'].values[0]
        ax2.annotate(texto, xy=(ano, val), xytext=(ano, val - 4),
                     fontsize=8, ha='center', fontweight='bold',
                     arrowprops=dict(arrowstyle='->', color='black', lw=0.8))

plt.tight_layout()
plt.savefig("graficos/variacoes_sazonais/variacoes_sazonais.png", dpi=300)
plt.close()
print("[Salvo] graficos/variacoes_sazonais/variacoes_sazonais.png")

# ============================================================
# ETAPA 5 — Estatisticas Descritivas Complementares
# ============================================================
print("\n" + "=" * 60)
print("ETAPA 5 — ESTATISTICAS DESCRITIVAS COMPLETAS")
print("=" * 60)

cols_stats = ['primary_energy_consumption', 'coal_consumption',
              'oil_consumption', 'gas_consumption',
              'nuclear_consumption', 'renewables_consumption']
nomes_stats = ['Consumo Total', 'Carvao', 'Petroleo',
               'Gas Natural', 'Nuclear', 'Renovaveis']

for nome, col in zip(nomes_stats, cols_stats):
    serie = paises[col].dropna()
    if len(serie) == 0:
        continue
    print(f"\n--- {nome} (todos os paises, todos os anos) ---")
    print(f"  Contagem:        {serie.count()}")
    print(f"  Media:           {serie.mean():.2f} TWh")
    print(f"  Mediana:         {serie.median():.2f} TWh")
    print(f"  Desvio Padrao:   {serie.std():.2f}")
    print(f"  Variancia:       {serie.var():.2f}")
    print(f"  Minimo:          {serie.min():.2f} TWh")
    print(f"  1o Quartil (Q1): {serie.quantile(0.25):.2f} TWh")
    print(f"  3o Quartil (Q3): {serie.quantile(0.75):.2f} TWh")
    print(f"  Maximo:          {serie.max():.2f} TWh")
    print(f"  Assimetria:      {serie.skew():.4f}")
    print(f"  Curtose:         {serie.kurtosis():.4f}")

print("\n" + "=" * 60)
print("ANALISE CONCLUIDA — Todos os arquivos foram gerados!")
print("=" * 60)

"""
Dashboard Interativo — Consumo de Energia ao Longo do Tempo
Gera um HTML com visualizacoes interativas usando Plotly.
"""

import pandas as pd
import numpy as np
from scipy import stats
import plotly
import plotly.graph_objects as go
import plotly.express as px
import json
import base64
import struct

# Carregar dados
df = pd.read_csv("../dados/dataset.csv")

col_total = "primary_energy_consumption"
fontes = {
    'Carvao': 'coal_consumption',
    'Petroleo': 'oil_consumption',
    'Gas Natural': 'gas_consumption',
    'Nuclear': 'nuclear_consumption',
    'Renovaveis': 'renewables_consumption',
    'Hidro': 'hydro_consumption',
}

# Dados mundiais
mundo = df[df['country'] == 'World'].dropna(subset=[col_total]).copy()

# Regioes
regioes_nomes = ['Africa', 'Asia', 'Europe', 'North America', 'South America', 'Oceania']
regioes = df[df['country'].isin(regioes_nomes)].copy()

# Paises reais
paises = df[df['iso_code'].notna()].copy()

# Estatisticas
slope, intercept, r_val, p_val, _ = stats.linregress(
    mundo['year'], mundo[col_total]
)
var_media = mundo['energy_cons_change_pct'].dropna().mean()

# ============================================================
# FIGURA 1 — Scatter: Consumo por fonte ao longo do tempo
# ============================================================
fig_scatter = go.Figure()
cores = ['#616161', '#FF8F00', '#1565C0', '#7B1FA2', '#2E7D32', '#00838F']

# Consumo total como linha
dados_total = mundo[['year', col_total]].dropna()
fig_scatter.add_trace(go.Scatter(
    x=dados_total['year'].tolist(),
    y=dados_total[col_total].tolist(),
    mode='lines',
    line=dict(color='#E53935', width=2.5),
    name='Total Primario',
    hovertemplate="<b>Total Primario</b><br>Ano: %{x}<br>Consumo: %{y:,.0f} TWh<extra></extra>"
))

# Fontes individuais como linhas
for i, (nome, col) in enumerate(fontes.items()):
    dados = mundo[['year', col]].dropna()
    fig_scatter.add_trace(go.Scatter(
        x=dados['year'].tolist(),
        y=dados[col].tolist(),
        mode='lines',
        line=dict(color=cores[i], width=2),
        name=nome,
        hovertemplate=f"<b>{nome}</b><br>Ano: %{{x}}<br>Consumo: %{{y:,.0f}} TWh<extra></extra>"
    ))

# Linha de tendencia do consumo total
x_t = dados_total['year'].tolist()
y_trend = [slope * x + intercept for x in x_t]
fig_scatter.add_trace(go.Scatter(
    x=x_t, y=y_trend,
    mode='lines', line=dict(color='red', width=2, dash='dash'),
    name=f'Tendencia Total (r={r_val:.3f})',
    hoverinfo='skip'
))

fig_scatter.update_layout(
    title=f"Crescimento do Consumo de Energia ao Longo dos Anos (Mundo)<br>"
          f"<sub>Correlacao consumo total vs ano: r = {r_val:.3f}</sub>",
    xaxis_title="Ano",
    yaxis_title="Consumo (TWh)",
    template="plotly_white",
    height=650
)

# ============================================================
# FIGURA 2 — Barras: Media por regiao e fonte
# ============================================================
fig_barras = go.Figure()
for i, (nome, col) in enumerate(fontes.items()):
    medias = []
    for reg in regioes_nomes:
        m = regioes[regioes['country'] == reg][col].mean()
        medias.append(round(m, 1) if pd.notna(m) else 0)
    fig_barras.add_trace(go.Bar(
        x=regioes_nomes,
        y=medias,
        name=nome,
        marker_color=cores[i],
        hovertemplate=f"<b>{nome}</b><br>%{{x}}<br>Media: %{{y:,.1f}} TWh<extra></extra>"
    ))

fig_barras.update_layout(
    title="Media de Consumo de Energia por Regiao e Fonte",
    xaxis_title="Regiao",
    yaxis_title="Media de Consumo (TWh)",
    barmode='group',
    template="plotly_white",
    height=650
)

# ============================================================
# FIGURA 3 — Variacao anual (barras + linha de consumo)
# ============================================================
mundo_var = mundo[['year', col_total, 'energy_cons_change_pct']].dropna(
    subset=['energy_cons_change_pct']
)

fig_var = go.Figure()
cores_bar = ['#EF5350' if v < 0 else '#42A5F5'
             for v in mundo_var['energy_cons_change_pct'].tolist()]

fig_var.add_trace(go.Bar(
    x=mundo_var['year'].tolist(),
    y=mundo_var['energy_cons_change_pct'].tolist(),
    marker_color=cores_bar,
    name='Variacao %',
    hovertemplate="Ano: %{x}<br>Variacao: %{y:.2f}%<extra></extra>"
))

fig_var.add_hline(y=0, line_color='black', line_width=0.5)
fig_var.add_hline(y=var_media, line_dash='dash', line_color='green',
                  annotation_text=f"Media: {var_media:.2f}%")

# Anotar crises
for ano, texto in {1973: "Crise Petroleo", 1979: "2a Crise", 2009: "Crise Financeira", 2020: "COVID-19"}.items():
    row = mundo_var[mundo_var['year'] == ano]
    if len(row) > 0:
        fig_var.add_annotation(x=ano, y=row['energy_cons_change_pct'].values[0],
                               text=texto, showarrow=True, arrowhead=2, font=dict(size=10))

fig_var.update_layout(
    title="Variacao Percentual Anual do Consumo de Energia — Mundo",
    xaxis_title="Ano",
    yaxis_title="Variacao (%)",
    template="plotly_white",
    height=600
)

# ============================================================
# FIGURA 4 — Top 20 paises consumidores (ano mais recente)
# ============================================================
recente = paises[paises['year'] == paises['year'].max()].dropna(subset=[col_total])
top20 = recente.nlargest(20, col_total).sort_values(col_total)

fig_top = go.Figure()
fig_top.add_trace(go.Bar(
    y=top20['country'].tolist(),
    x=top20[col_total].tolist(),
    orientation='h',
    marker=dict(color=top20[col_total].tolist(), colorscale='Viridis'),
    hovertemplate="<b>%{y}</b><br>Consumo: %{x:,.0f} TWh<extra></extra>"
))

fig_top.update_layout(
    title=f"Top 20 Paises — Consumo de Energia Primaria ({int(paises['year'].max())})",
    xaxis_title="Consumo (TWh)",
    template="plotly_white",
    height=700
)

# ============================================================
# FIGURA 5 — Evolucao da matriz energetica mundial (area empilhada)
# ============================================================
fig_area = go.Figure()
for i, (nome, col) in enumerate(fontes.items()):
    dados = mundo[['year', col]].dropna()
    fig_area.add_trace(go.Scatter(
        x=dados['year'].tolist(),
        y=dados[col].tolist(),
        mode='lines',
        stackgroup='one',
        name=nome,
        line=dict(color=cores[i]),
        hovertemplate=f"<b>{nome}</b><br>Ano: %{{x}}<br>Consumo: %{{y:,.0f}} TWh<extra></extra>"
    ))

fig_area.update_layout(
    title="Evolucao da Matriz Energetica Mundial",
    xaxis_title="Ano",
    yaxis_title="Consumo (TWh)",
    template="plotly_white",
    height=650
)

# ============================================================
# MONTAR HTML COM ABAS
# ============================================================
figures = {
    'scatter': fig_scatter,
    'barras': fig_barras,
    'variacao': fig_var,
    'ranking': fig_top,
    'matriz': fig_area,
}

def purge_bdata(obj):
    if isinstance(obj, dict):
        if 'bdata' in obj and 'dtype' in obj:
            dtype_map = {'f8': 'd', 'f4': 'f', 'i4': 'i', 'i2': 'h', 'u1': 'B', 'i1': 'b'}
            fmt = dtype_map.get(obj['dtype'], 'd')
            raw = base64.b64decode(obj['bdata'])
            size = struct.calcsize(fmt)
            return [struct.unpack(fmt, raw[i:i+size])[0] for i in range(0, len(raw), size)]
        return {k: purge_bdata(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [purge_bdata(i) for i in obj]
    return obj

figures_json = {}
for name, fig in figures.items():
    fig_dict = json.loads(fig.to_json())
    fig_dict = purge_bdata(fig_dict)
    figures_json[name] = json.dumps(fig_dict)

media_total = mundo[col_total].mean()
ultimo_consumo = mundo[mundo['year'] == mundo['year'].max()][col_total].values[0]

html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Interativo — Consumo de Energia Global</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #f5f5f5; }}
        .header {{
            background: linear-gradient(135deg, #1b5e20, #33691e);
            color: white; padding: 30px 40px; text-align: center;
        }}
        .header h1 {{ font-size: 28px; margin-bottom: 8px; }}
        .header p {{ font-size: 14px; opacity: 0.85; }}
        .tabs {{
            display: flex; background: #263238; padding: 0 20px;
            overflow-x: auto; gap: 4px;
        }}
        .tab {{
            padding: 14px 24px; color: #b0bec5; cursor: pointer;
            border: none; background: none; font-size: 14px;
            font-weight: 500; white-space: nowrap; transition: all 0.2s;
            border-bottom: 3px solid transparent;
        }}
        .tab:hover {{ color: white; background: rgba(255,255,255,0.05); }}
        .tab.active {{ color: white; border-bottom-color: #66bb6a; }}
        .content {{ display: none; padding: 20px; }}
        .content.active {{ display: block; }}
        .stats {{
            display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px; padding: 20px; max-width: 1200px; margin: 0 auto;
        }}
        .stat-card {{
            background: white; border-radius: 8px; padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;
        }}
        .stat-card .value {{ font-size: 28px; font-weight: bold; color: #1b5e20; }}
        .stat-card .label {{ font-size: 12px; color: #666; margin-top: 4px; }}
        .plot-container {{ width: 100%; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Dashboard Interativo — Consumo de Energia Global</h1>
        <p>Dataset: World Energy Consumption (219 paises, 1900-2022)</p>
    </div>

    <div class="stats">
        <div class="stat-card">
            <div class="value">219</div>
            <div class="label">Paises analisados</div>
        </div>
        <div class="stat-card">
            <div class="value">{ultimo_consumo:,.0f}</div>
            <div class="label">Consumo 2022 (TWh)</div>
        </div>
        <div class="stat-card">
            <div class="value">{r_val:.3f}</div>
            <div class="label">Correlacao (consumo vs ano)</div>
        </div>
        <div class="stat-card">
            <div class="value">+{var_media:.1f}%</div>
            <div class="label">Crescimento medio anual</div>
        </div>
        <div class="stat-card">
            <div class="value">6</div>
            <div class="label">Fontes de energia</div>
        </div>
    </div>

    <div class="tabs">
        <button class="tab active" onclick="showTab('scatter', this)">Dispersao</button>
        <button class="tab" onclick="showTab('barras', this)">Media por Regiao</button>
        <button class="tab" onclick="showTab('variacao', this)">Variacao Anual</button>
        <button class="tab" onclick="showTab('ranking', this)">Top 20 Paises</button>
        <button class="tab" onclick="showTab('matriz', this)">Matriz Energetica</button>
    </div>

    <div id="scatter" class="content active"><div id="plot-scatter" class="plot-container"></div></div>
    <div id="barras" class="content"><div id="plot-barras" class="plot-container"></div></div>
    <div id="variacao" class="content"><div id="plot-variacao" class="plot-container"></div></div>
    <div id="ranking" class="content"><div id="plot-ranking" class="plot-container"></div></div>
    <div id="matriz" class="content"><div id="plot-matriz" class="plot-container"></div></div>

    <script>
        var figData = {{
            scatter: {figures_json['scatter']},
            barras: {figures_json['barras']},
            variacao: {figures_json['variacao']},
            ranking: {figures_json['ranking']},
            matriz: {figures_json['matriz']}
        }};

        var rendered = {{}};

        function renderPlot(id) {{
            if (rendered[id]) return;
            var fig = figData[id];
            Plotly.newPlot('plot-' + id, fig.data, fig.layout, {{responsive: true}});
            rendered[id] = true;
        }}

        function showTab(id, btn) {{
            document.querySelectorAll('.content').forEach(c => c.classList.remove('active'));
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.getElementById(id).classList.add('active');
            btn.classList.add('active');
            setTimeout(function() {{ renderPlot(id); }}, 50);
        }}

        window.addEventListener('load', function() {{
            renderPlot('scatter');
        }});
    </script>
</body>
</html>"""

with open("dashboard.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Dashboard gerado com sucesso!")
print("[Salvo] interativo/dashboard.html")

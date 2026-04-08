"""
Dashboard Interativo — Velocidade de Internet Global
Gera um HTML com visualizacoes interativas usando Plotly.
"""

import pandas as pd
import numpy as np
from scipy import stats
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

# Carregar dados
df = pd.read_csv("../dados/broadband_speed.csv")

col_dl = "Broadband Mbps"
col_mob = "Mobile Mbps"

# Dados filtrados (com mobile)
df_full = df.dropna(subset=[col_dl, col_mob]).copy()

# Regressao linear para o scatter
slope, intercept, r_value, p_value, _, = stats.linregress(
    df_full[col_dl], df_full[col_mob]
)
x_line = np.array([df_full[col_dl].min(), df_full[col_dl].max()])
y_line = slope * x_line + intercept

# Estatisticas
media_dl = df[col_dl].mean()
mediana_dl = df[col_dl].median()
media_mob = df[col_mob].mean()
mediana_mob = df[col_mob].median()

# ============================================================
# FIGURA 1 — Scatter Interativo: Download vs Mobile
# ============================================================
fig_scatter = go.Figure()

fig_scatter.add_trace(go.Scatter(
    x=df_full[col_dl].tolist(),
    y=df_full[col_mob].tolist(),
    mode='markers',
    marker=dict(
        size=12,
        color=df_full[col_dl].tolist(),
        colorscale='Turbo',
        showscale=True,
        colorbar=dict(title="Download<br>(Mbps)"),
        line=dict(width=1, color='black'),
        opacity=0.85
    ),
    text=df_full['Country'].tolist(),
    customdata=list(zip(
        df_full['Broadband Speed Rank'].tolist(),
        df_full['Mobile Speed Rank'].tolist()
    )),
    hovertemplate=(
        "<b>%{text}</b><br>"
        "Download: %{x:.1f} Mbps (Rank #%{customdata[0]:.0f})<br>"
        "Mobile: %{y:.1f} Mbps (Rank #%{customdata[1]:.0f})<br>"
        "<extra></extra>"
    ),
    name='Paises'
))

fig_scatter.add_trace(go.Scatter(
    x=x_line.tolist(), y=y_line.tolist(),
    mode='lines',
    line=dict(color='red', width=2, dash='dash'),
    name=f'Regressao (r={r_value:.3f})',
    hoverinfo='skip'
))

fig_scatter.update_layout(
    title=dict(text=f"Dispersao: Download (Banda Larga) vs Mobile por Pais<br>"
                    f"<sub>Correlacao de Pearson: r = {r_value:.3f} | p-valor = {p_value:.2e}</sub>"),
    xaxis_title="Velocidade de Download — Banda Larga (Mbps)",
    yaxis_title="Velocidade Mobile (Mbps)",
    xaxis=dict(range=[0, df_full[col_dl].max() * 1.05]),
    yaxis=dict(range=[0, df_full[col_mob].max() * 1.05]),
    template="plotly_white",
    height=650
)

# ============================================================
# FIGURA 2 — Ranking Top 20 + Bottom 20
# ============================================================
df_sorted = df.sort_values(col_dl, ascending=True)
top20 = df_sorted.tail(20).copy()
bottom20 = df_sorted.head(20).copy()

top20['grupo'] = 'Top 20 — Mais rapidos'
bottom20['grupo'] = 'Bottom 20 — Mais lentos'
df_rank = pd.concat([bottom20, top20])

fig_ranking = go.Figure()

fig_ranking.add_trace(go.Bar(
    y=bottom20['Country'].tolist(),
    x=bottom20[col_dl].tolist(),
    orientation='h',
    marker=dict(color='#EF5350'),
    name='Mais lentos',
    hovertemplate="<b>%{y}</b><br>Download: %{x:.1f} Mbps<extra></extra>"
))

fig_ranking.add_trace(go.Bar(
    y=top20['Country'].tolist(),
    x=top20[col_dl].tolist(),
    orientation='h',
    marker=dict(color='#42A5F5'),
    name='Mais rapidos',
    hovertemplate="<b>%{y}</b><br>Download: %{x:.1f} Mbps<extra></extra>"
))

fig_ranking.add_vline(x=media_dl, line_dash="dash", line_color="green",
                      annotation_text=f"Media global: {media_dl:.1f}")
fig_ranking.add_vline(x=mediana_dl, line_dash="dot", line_color="orange",
                      annotation_text=f"Mediana: {mediana_dl:.1f}")

fig_ranking.update_layout(
    title="Ranking de Velocidade de Download — Top 20 vs Bottom 20",
    xaxis_title="Velocidade de Download (Mbps)",
    yaxis_title="",
    template="plotly_white",
    height=800,
    barmode='relative'
)

# ============================================================
# FIGURA 3 — Boxplot Comparativo
# ============================================================
fig_box = go.Figure()

fig_box.add_trace(go.Box(
    y=df[col_dl].dropna().tolist(),
    name="Download (Banda Larga)",
    marker_color='#2196F3',
    boxpoints='all',
    text=df.dropna(subset=[col_dl])['Country'].tolist(),
    hovertemplate="<b>%{text}</b><br>Download: %{y:.1f} Mbps<extra></extra>",
    pointpos=-1.5,
    jitter=0.3
))

fig_box.add_trace(go.Box(
    y=df[col_mob].dropna().tolist(),
    name="Mobile",
    marker_color='#FF9800',
    boxpoints='all',
    text=df.dropna(subset=[col_mob])['Country'].tolist(),
    hovertemplate="<b>%{text}</b><br>Mobile: %{y:.1f} Mbps<extra></extra>",
    pointpos=-1.5,
    jitter=0.3
))

fig_box.update_layout(
    title="Boxplot Comparativo — Download vs Mobile",
    yaxis_title="Velocidade (Mbps)",
    template="plotly_white",
    height=600
)

# ============================================================
# FIGURA 4 — Treemap por Faixa de Velocidade
# ============================================================
def faixa_velocidade(v):
    if v < 25:
        return "0-25 Mbps (Muito lento)"
    elif v < 50:
        return "25-50 Mbps (Lento)"
    elif v < 100:
        return "50-100 Mbps (Moderado)"
    else:
        return "100+ Mbps (Rapido)"

df_tree = df[['Country', col_dl]].copy()
df_tree['Faixa'] = df_tree[col_dl].apply(faixa_velocidade)
df_tree = df_tree.sort_values(col_dl, ascending=False)

fig_treemap = px.treemap(
    df_tree,
    path=['Faixa', 'Country'],
    values=col_dl,
    color=col_dl,
    color_continuous_scale='RdYlGn',
    title="Treemap — Paises por Faixa de Velocidade de Download",
    hover_data={col_dl: ':.1f'}
)

fig_treemap.update_layout(
    height=700,
    coloraxis_colorbar=dict(title="Download<br>(Mbps)")
)

fig_treemap.update_traces(
    hovertemplate="<b>%{label}</b><br>Download: %{value:.1f} Mbps<extra></extra>"
)

# ============================================================
# FIGURA 5 — Histograma Interativo Comparativo
# ============================================================
fig_hist = go.Figure()

fig_hist.add_trace(go.Histogram(
    x=df[col_dl].dropna().tolist(),
    nbinsx=18,
    name='Download (Banda Larga)',
    marker_color='rgba(33, 150, 243, 0.6)',
    hovertemplate="Faixa: %{x:.0f} Mbps<br>Paises: %{y}<extra></extra>"
))

fig_hist.add_trace(go.Histogram(
    x=df[col_mob].dropna().tolist(),
    nbinsx=18,
    name='Mobile',
    marker_color='rgba(255, 152, 0, 0.6)',
    hovertemplate="Faixa: %{x:.0f} Mbps<br>Paises: %{y}<extra></extra>"
))

fig_hist.add_vline(x=media_dl, line_dash="dash", line_color="blue",
                   annotation_text=f"Media DL: {media_dl:.1f}")
fig_hist.add_vline(x=mediana_dl, line_dash="dot", line_color="blue",
                   annotation_text=f"Mediana DL: {mediana_dl:.1f}")
fig_hist.add_vline(x=media_mob, line_dash="dash", line_color="darkorange",
                   annotation_text=f"Media Mob: {media_mob:.1f}")
fig_hist.add_vline(x=mediana_mob, line_dash="dot", line_color="darkorange",
                   annotation_text=f"Mediana Mob: {mediana_mob:.1f}")

fig_hist.update_layout(
    title="Histograma Comparativo — Download vs Mobile",
    xaxis_title="Velocidade (Mbps)",
    yaxis_title="Frequencia (Paises)",
    barmode='overlay',
    template="plotly_white",
    height=600
)

# ============================================================
# MONTAR HTML COM ABAS — renderizacao sob demanda via JSON
# ============================================================
import json

figures = {
    'scatter': fig_scatter,
    'ranking': fig_ranking,
    'boxplot': fig_box,
    'treemap': fig_treemap,
    'histograma': fig_hist,
}

# Converter para JSON sem formato binario (bdata)
def purge_bdata(obj):
    """Converte recursivamente campos bdata em listas normais."""
    if isinstance(obj, dict):
        if 'bdata' in obj and 'dtype' in obj:
            import base64, struct
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

html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Interativo — Velocidade de Internet Global</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #f5f5f5; }}
        .header {{
            background: linear-gradient(135deg, #1a237e, #0d47a1);
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
        .tab.active {{ color: white; border-bottom-color: #42a5f5; }}
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
        .stat-card .value {{ font-size: 28px; font-weight: bold; color: #1a237e; }}
        .stat-card .label {{ font-size: 12px; color: #666; margin-top: 4px; }}
        .plot-container {{ width: 100%; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Dashboard Interativo — Velocidade de Internet Global</h1>
        <p>Dataset: Internet Broadband and Mobile Speeds by Country (179 paises, Janeiro 2022)</p>
    </div>

    <div class="stats">
        <div class="stat-card">
            <div class="value">179</div>
            <div class="label">Paises analisados</div>
        </div>
        <div class="stat-card">
            <div class="value">{media_dl:.1f}</div>
            <div class="label">Media Download (Mbps)</div>
        </div>
        <div class="stat-card">
            <div class="value">{mediana_dl:.1f}</div>
            <div class="label">Mediana Download (Mbps)</div>
        </div>
        <div class="stat-card">
            <div class="value">{media_mob:.1f}</div>
            <div class="label">Media Mobile (Mbps)</div>
        </div>
        <div class="stat-card">
            <div class="value">{r_value:.3f}</div>
            <div class="label">Correlacao de Pearson</div>
        </div>
    </div>

    <div class="tabs">
        <button class="tab active" onclick="showTab('scatter', this)">Dispersao</button>
        <button class="tab" onclick="showTab('ranking', this)">Ranking</button>
        <button class="tab" onclick="showTab('boxplot', this)">Boxplot</button>
        <button class="tab" onclick="showTab('treemap', this)">Treemap</button>
        <button class="tab" onclick="showTab('histograma', this)">Histograma</button>
    </div>

    <div id="scatter" class="content active"><div id="plot-scatter" class="plot-container"></div></div>
    <div id="ranking" class="content"><div id="plot-ranking" class="plot-container"></div></div>
    <div id="boxplot" class="content"><div id="plot-boxplot" class="plot-container"></div></div>
    <div id="treemap" class="content"><div id="plot-treemap" class="plot-container"></div></div>
    <div id="histograma" class="content"><div id="plot-histograma" class="plot-container"></div></div>

    <script>
        var figData = {{
            scatter: {figures_json['scatter']},
            ranking: {figures_json['ranking']},
            boxplot: {figures_json['boxplot']},
            treemap: {figures_json['treemap']},
            histograma: {figures_json['histograma']}
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

        // Render first tab on page load
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
print("Abra o arquivo no navegador para interagir com os graficos.")

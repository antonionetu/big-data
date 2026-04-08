# Dashboard Interativo — Explicacao das Visualizacoes

Para abrir o dashboard:

```bash
cd consumo-energia-14/interativo
python3 dashboard_interativo.py
xdg-open dashboard.html
```

---

## Aba 1 — Dispersao (Consumo por Fonte ao Longo do Tempo)

Scatter plot com consumo de cada fonte de energia (carvao, petroleo, gas, nuclear, renovaveis, hidro) ao longo dos anos. Linha vermelha mostra a tendencia do consumo total (r = 0.994).

**Interatividade:** Hover mostra fonte, ano e consumo em TWh. Zoom e pan disponiveis.

---

## Aba 2 — Media por Regiao

Barras agrupadas mostrando a media historica de consumo por regiao (6 continentes) e por fonte de energia.

**Interatividade:** Hover mostra regiao, fonte e valor. Clique na legenda para isolar fontes.

---

## Aba 3 — Variacao Anual

Barras mostrando a variacao percentual ano-a-ano do consumo mundial. Azul = crescimento, vermelho = queda. Anotacoes marcam crises historicas.

**Interatividade:** Hover mostra ano e variacao exata. Zoom para focar em periodos especificos.

---

## Aba 4 — Top 20 Paises

Ranking horizontal dos 20 maiores consumidores de energia no ano mais recente (2022).

**Interatividade:** Hover mostra pais e consumo em TWh.

---

## Aba 5 — Matriz Energetica

Grafico de area empilhada mostrando a evolucao da composicao da matriz energetica mundial ao longo das decadas.

**Interatividade:** Hover mostra fonte e consumo por ano. Clique na legenda para mostrar/esconder fontes.

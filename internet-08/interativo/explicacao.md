# Dashboard Interativo — Explicacao das Visualizacoes

Para abrir o dashboard, execute o script e abra o HTML no navegador:

```bash
cd interativo
python3 dashboard_interativo.py
xdg-open dashboard.html   # Linux
```

---

## Aba 1 — Dispersao (Scatter Plot Interativo)

**O que e:** Grafico de dispersao com Download (banda larga) no eixo X e Mobile no eixo Y. Cada ponto e um pais.

**Interatividade:**
- Passe o mouse sobre qualquer ponto para ver o nome do pais, velocidades exatas e ranking mundial
- Os pontos sao coloridos por velocidade de download (escala Viridis)
- A linha vermelha tracejada mostra a regressao linear (r = 0.561)
- Use a roda do mouse para zoom, arraste para mover

**Por que e melhor que o estatico:** No grafico PNG nao da para saber qual ponto e qual pais. Aqui, basta passar o mouse.

---

## Aba 2 — Ranking (Barras Horizontais)

**O que e:** Os 20 paises mais rapidos (azul) e os 20 mais lentos (vermelho), em barras horizontais.

**Interatividade:**
- Hover mostra pais e velocidade exata
- Linhas verticais indicam a media e mediana globais
- Permite comparar visualmente a distancia entre os extremos

**Por que e melhor:** Mostra claramente a desigualdade — Monaco (192.68 Mbps) vs Afeganistao (1.62 Mbps), uma diferenca de 119x.

---

## Aba 3 — Boxplot Comparativo

**O que e:** Dois boxplots lado a lado: Download (banda larga) e Mobile. Mostra mediana, quartis, e todos os pontos individuais.

**Interatividade:**
- Cada ponto e clicavel — mostra o nome do pais e velocidade
- Identifica visualmente os outliers (paises muito acima ou abaixo do padrao)

**Por que e melhor:** O boxplot mostra a distribuicao de forma mais compacta que o histograma, e com pontos individuais voce identifica cada pais.

---

## Aba 4 — Treemap (Mapa de Arvore)

**O que e:** Agrupa paises em 4 faixas de velocidade:
- 0-25 Mbps (Muito lento)
- 25-50 Mbps (Lento)
- 50-100 Mbps (Moderado)
- 100+ Mbps (Rapido)

A area de cada retangulo e proporcional a velocidade de download.

**Interatividade:**
- Clique em uma faixa para expandir e ver os paises dentro dela
- Hover mostra pais e velocidade
- Clique fora ou no titulo para voltar

**Por que e melhor:** Mostra de forma visual e proporcional quantos paises estao em cada faixa — fica claro que a maioria esta nas faixas mais lentas.

---

## Aba 5 — Histograma Interativo

**O que e:** Mesmo histograma comparativo (Download vs Mobile), mas interativo.

**Interatividade:**
- Hover mostra a faixa de velocidade e quantos paises estao nela
- Clique na legenda para mostrar/esconder uma das distribuicoes
- Linhas verticais marcam media e mediana de cada tipo
- Zoom e pan disponiveis

**Por que e melhor:** Permite isolar cada distribuicao clicando na legenda, e o hover mostra contagens exatas.

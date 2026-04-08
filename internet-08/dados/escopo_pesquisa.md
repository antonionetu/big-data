# Escopo da Pesquisa — Internet Broadband and Mobile Speeds by Country

## Fonte dos Dados

- **Dataset:** Internet Broadband and Mobile Speeds by Country
- **Origem:** Kaggle (prasertk/internet-broadband-and-mobile-speeds-by-country)
- **Data de referencia:** Janeiro de 2022
- **Formato:** CSV com 179 linhas e 6 colunas

---

## Cobertura

- **179 paises** com dados de velocidade de banda larga (broadband)
- **139 paises** com dados de velocidade mobile
- **40 paises** sem dados de velocidade mobile

---

## Informacoes disponiveis por pais

Cada pais possui ate **4 metricas**:

| Coluna | Descricao | Cobertura |
|---|---|---|
| Country | Nome do pais | 179/179 (100%) |
| Broadband Speed Rank | Posicao no ranking mundial de banda larga | 179/179 (100%) |
| Broadband Mbps | Velocidade de download de banda larga em Mbps | 179/179 (100%) |
| Mobile Speed Rank | Posicao no ranking mundial mobile | 139/179 (77.7%) |
| Mobile Mbps | Velocidade mobile em Mbps | 139/179 (77.7%) |
| As of | Data de referencia da medicao | 179/179 (100%) |

---

## Amplitude dos dados

| Metrica | Minimo | Maximo | Amplitude |
|---|---|---|---|
| Download (Banda Larga) | 1.62 Mbps (Afeganistao) | 192.68 Mbps (Monaco) | 191.06 Mbps |
| Mobile | 0.53 Mbps (Yemen) | 135.62 Mbps (Emirados Arabes) | 135.09 Mbps |

---

## Paises sem dados mobile (40)

Estes paises possuem apenas dados de banda larga, sem informacoes de velocidade mobile:

| # | Pais | Download (Mbps) |
|---|---|---|
| 1 | Monaco | 192.68 |
| 2 | Liechtenstein | 118.19 |
| 3 | Andorra | 92.42 |
| 4 | Saint Lucia | 73.70 |
| 5 | Barbados | 68.83 |
| 6 | San Marino | 68.29 |
| 7 | Saint Vincent and the Grenadines | 58.26 |
| 8 | Dominica | 50.96 |
| 9 | Grenada | 50.66 |
| 10 | The Bahamas | 37.69 |
| 11 | Belize | 31.81 |
| 12 | Guyana | 31.01 |
| 13 | Saint Kitts and Nevis | 25.16 |
| 14 | Madagascar | 25.16 |
| 15 | Seychelles | 22.13 |
| 16 | Lesotho | 18.92 |
| 17 | Mali | 17.71 |
| 18 | Antigua and Barbuda | 17.36 |
| 19 | Togo | 16.46 |
| 20 | Cape Verde | 16.37 |
| 21 | Gabon | 13.41 |
| 22 | Congo | 11.84 |
| 23 | Suriname | 10.79 |
| 24 | Benin | 10.77 |
| 25 | Western Sahara | 10.51 |
| 26 | Micronesia | 9.75 |
| 27 | Rwanda | 9.52 |
| 28 | Liberia | 9.48 |
| 29 | Marshall Islands | 9.29 |
| 30 | Papua New Guinea | 9.25 |
| 31 | Sierra Leone | 8.57 |
| 32 | Bhutan | 8.52 |
| 33 | The Gambia | 7.84 |
| 34 | Mauritania | 6.10 |
| 35 | Malawi | 5.54 |
| 36 | Burundi | 5.44 |
| 37 | Swaziland | 4.94 |
| 38 | Djibouti | 4.71 |
| 39 | Niger | 3.85 |
| 40 | Guinea | 3.79 |

---

## Limitacoes do dataset

- **Ponto unico no tempo:** Todos os dados sao de janeiro de 2022 — nao ha serie historica para analisar evolucao.
- **Uma medicao por pais:** Cada pais tem um unico valor de download e mobile, sem desagregacao por regiao, provedor ou tipo de conexao.
- **22.3% sem dados mobile:** 40 paises (majoritariamente pequenos ou em desenvolvimento) nao possuem dados de velocidade mobile, o que limita analises comparativas entre banda larga e mobile.
- **Sem contexto socioeconomico:** O dataset nao inclui PIB, populacao, investimento em infraestrutura ou outros indicadores que permitiriam correlacoes mais profundas.

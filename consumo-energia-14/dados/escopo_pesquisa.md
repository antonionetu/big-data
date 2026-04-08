# Escopo da Pesquisa — World Energy Consumption

## Fonte dos Dados

- **Dataset:** World Energy Consumption
- **Origem:** Kaggle (pralabhpoudel/world-energy-consumption)
- **Periodo:** 1900 - 2022
- **Formato:** CSV com 22.012 linhas e 129 colunas

---

## Cobertura

- **306 entidades** no total (paises + agregados regionais)
- **219 paises** com codigo ISO valido
- **87 entidades agregadas** (regioes, continentes, blocos economicos como OECD, G7, etc.)
- **6 regioes continentais** usadas na analise: Africa, Asia, Europe, North America, South America, Oceania

---

## Informacoes disponiveis por pais/ano

O dataset contem **129 colunas** organizadas em categorias:

| Categoria | Colunas | Exemplo |
|---|---|---|
| Identificacao | 3 | country, year, iso_code |
| Demografico | 2 | population, gdp |
| Consumo total | 5 | primary_energy_consumption, energy_per_capita |
| Carvao | 12 | coal_consumption, coal_electricity, coal_share_energy |
| Petroleo | 12 | oil_consumption, oil_electricity, oil_share_energy |
| Gas Natural | 12 | gas_consumption, gas_electricity, gas_share_energy |
| Nuclear | 10 | nuclear_consumption, nuclear_electricity |
| Renovaveis | 10 | renewables_consumption, renewables_electricity |
| Hidro | 8 | hydro_consumption, hydro_electricity |
| Solar | 8 | solar_consumption, solar_electricity |
| Eolica | 8 | wind_consumption, wind_electricity |
| Biocombustivel | 8 | biofuel_consumption, biofuel_electricity |
| Fosseis (agregado) | 8 | fossil_fuel_consumption, fossil_share_energy |
| Baixo carbono | 8 | low_carbon_consumption, low_carbon_electricity |
| Outros | ~13 | electricity_generation, greenhouse_gas_emissions |

---

## Fontes de energia analisadas

| Fonte | Coluna principal | Paises com dados |
|---|---|---|
| Consumo total | primary_energy_consumption | 12.588 registros |
| Carvao | coal_consumption | 5.420 registros |
| Petroleo | oil_consumption | 5.713 registros |
| Gas Natural | gas_consumption | 5.215 registros |
| Nuclear | nuclear_consumption | 4.397 registros |
| Renovaveis | renewables_consumption | 5.479 registros |
| Hidro | hydro_consumption | 5.479 registros |

---

## Limitacoes do dataset

- **Dados anuais:** Nao ha granularidade mensal ou trimestral, limitando a analise de sazonalidade a variacoes ano-a-ano.
- **Muitos nulos:** Colunas especificas por fonte (nuclear, solar, eolica) tem mais de 75% de valores nulos — muitos paises nao possuem essas fontes.
- **Dados antigos incompletos:** Antes de 1965, poucos paises tem dados de consumo por fonte.
- **Entidades mistas:** O dataset mistura paises reais com agregados regionais (World, OECD, etc.), exigindo filtragem cuidadosa.
- **Unidade em TWh:** Todos os valores de consumo estao em terawatt-hora (TWh), facilitando comparacoes diretas.

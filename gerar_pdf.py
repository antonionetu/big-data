"""
Gera o PDF de documentacao das atividades de Big Data.
"""

from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, 'Atividade Big Data - Documentacao', align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Pagina {self.page_no()}/{{nb}}', align='C')

    def titulo(self, texto):
        self.set_font('Helvetica', 'B', 18)
        self.set_text_color(20, 60, 120)
        self.cell(0, 12, texto, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(20, 60, 120)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(6)

    def subtitulo(self, texto):
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(40, 80, 40)
        self.cell(0, 10, texto, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def sub2(self, texto):
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(60, 60, 60)
        self.cell(0, 8, texto, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def corpo(self, texto):
        self.set_font('Helvetica', '', 11)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 6, texto)
        self.ln(3)

    def item(self, texto):
        self.set_font('Helvetica', '', 11)
        self.set_text_color(30, 30, 30)
        self.cell(5)
        self.multi_cell(0, 6, f"- {texto}")
        self.ln(1)

    def tabela(self, cabecalho, dados, larguras=None):
        if larguras is None:
            w = 190 / len(cabecalho)
            larguras = [w] * len(cabecalho)

        # Cabecalho
        self.set_font('Helvetica', 'B', 10)
        self.set_fill_color(220, 230, 240)
        self.set_text_color(20, 20, 20)
        for i, h in enumerate(cabecalho):
            self.cell(larguras[i], 8, h, border=1, fill=True, align='C')
        self.ln()

        # Dados
        self.set_font('Helvetica', '', 10)
        self.set_text_color(30, 30, 30)
        fill = False
        for row in dados:
            if fill:
                self.set_fill_color(245, 245, 245)
            else:
                self.set_fill_color(255, 255, 255)
            for i, val in enumerate(row):
                align = 'L' if i == 0 else 'C'
                self.cell(larguras[i], 7, str(val), border=1, fill=True, align=align)
            self.ln()
            fill = not fill
        self.ln(4)

    def imagem(self, caminho, legenda="", w=170):
        if os.path.exists(caminho):
            x = (210 - w) / 2
            self.image(caminho, x=x, w=w)
            if legenda:
                self.set_font('Helvetica', 'I', 9)
                self.set_text_color(100, 100, 100)
                self.cell(0, 6, legenda, align='C', new_x="LMARGIN", new_y="NEXT")
            self.ln(5)


# ============================================================
# MONTAR PDF
# ============================================================
pdf = PDF()
pdf.alias_nb_pages()
pdf.set_auto_page_break(auto=True, margin=20)

# ============================================================
# CAPA
# ============================================================
pdf.add_page()
pdf.ln(40)
pdf.set_font('Helvetica', 'B', 28)
pdf.set_text_color(20, 60, 120)
pdf.cell(0, 15, 'Atividade Big Data', align='C', new_x="LMARGIN", new_y="NEXT")
pdf.ln(5)
pdf.set_font('Helvetica', '', 16)
pdf.set_text_color(60, 60, 60)
pdf.cell(0, 10, 'Documentacao dos Problemas 08 e 14', align='C', new_x="LMARGIN", new_y="NEXT")
pdf.ln(10)
pdf.set_draw_color(20, 60, 120)
pdf.line(60, pdf.get_y(), 150, pdf.get_y())
pdf.ln(15)
pdf.set_font('Helvetica', '', 13)
pdf.cell(0, 8, 'Alunos: Antonio Neto e Fabricio Roberto', align='C', new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 8, 'Disciplina: Big Data', align='C', new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 8, 'Data: Abril de 2026', align='C', new_x="LMARGIN", new_y="NEXT")
pdf.ln(10)
pdf.set_font('Helvetica', '', 11)
pdf.set_text_color(100, 100, 100)
pdf.cell(0, 8, 'Repositorio: github.com/antonionetu/big-data', align='C', new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 8, 'Tecnologias: Python, Pandas, Matplotlib, Seaborn, Plotly, Scipy', align='C', new_x="LMARGIN", new_y="NEXT")

# ============================================================
# PROBLEMA 08 — VELOCIDADE DE INTERNET
# ============================================================
pdf.add_page()
pdf.titulo('Problema 08 - Velocidade de Internet Global')

pdf.subtitulo('1. Objetivo')
pdf.corpo('Analisar dados de velocidade de internet (banda larga e mobile) por pais, calculando estatisticas descritivas, gerando visualizacoes e investigando correlacoes entre as variaveis.')

pdf.subtitulo('2. Dataset')
pdf.corpo('Internet Broadband and Mobile Speeds by Country (Kaggle). Dados de janeiro de 2022 cobrindo 179 paises com velocidades de banda larga e mobile em Mbps.')

pdf.tabela(
    ['Metrica', 'Valor'],
    [
        ['Paises', '179'],
        ['Paises com dados mobile', '139'],
        ['Paises sem dados mobile', '40'],
        ['Colunas', '6'],
        ['Periodo', 'Janeiro 2022'],
    ],
    [100, 90]
)

pdf.subtitulo('3. Exploracao e Tratamento dos Dados')
pdf.corpo('O dataset foi carregado com Pandas e explorado: 179 linhas, 6 colunas, 40 valores nulos nas colunas de velocidade mobile (22.3% dos paises). As colunas principais sao Country, Broadband Mbps e Mobile Mbps. Nao foi necessario tratamento adicional alem da exclusao de nulos para analises especificas.')

# Questao A
pdf.subtitulo('4. Questao A: Media e Mediana de Download')
pdf.corpo('Calculou-se a media e mediana das velocidades de download por pais. Como cada pais possui um unico valor, as estatisticas globais representam a distribuicao entre paises.')

pdf.tabela(
    ['Estatistica', 'Download (Mbps)', 'Mobile (Mbps)'],
    [
        ['Media', '47.21', '34.89'],
        ['Mediana', '33.76', '26.18'],
        ['Desvio Padrao', '43.67', '26.69'],
        ['Minimo', '1.62', '0.53'],
        ['Maximo', '192.68', '135.62'],
        ['Assimetria', '1.37', '1.41'],
        ['Curtose', '1.60', '1.76'],
    ],
    [65, 65, 60]
)

pdf.corpo('A diferenca entre media (47.21) e mediana (33.76) revela distribuicao assimetrica positiva: a maioria dos paises tem velocidades abaixo da media global.')

pdf.sub2('Top 10 - Maiores velocidades')
pdf.tabela(
    ['Pais', 'Download (Mbps)'],
    [
        ['Monaco', '192.68'], ['Singapore', '192.01'], ['Chile', '189.36'],
        ['Thailand', '184.03'], ['Hong Kong (SAR)', '173.42'],
        ['Denmark', '163.60'], ['Macau (SAR)', '156.73'],
        ['China', '155.79'], ['United States', '143.76'], ['Spain', '134.19'],
    ],
    [110, 80]
)

pdf.sub2('Bottom 10 - Menores velocidades')
pdf.tabela(
    ['Pais', 'Download (Mbps)'],
    [
        ['Afghanistan', '1.62'], ['Turkmenistan', '1.89'], ['Cuba', '1.90'],
        ['Ethiopia', '2.69'], ['Yemen', '2.74'],
        ['Syria', '2.87'], ['Sudan', '3.28'],
        ['Guinea', '3.79'], ['Niger', '3.85'], ['Zambia', '4.60'],
    ],
    [110, 80]
)

# Questao B
pdf.add_page()
pdf.subtitulo('5. Questao B: Grafico de Dispersao Download vs Upload')
pdf.corpo('Criou-se um scatter plot entre velocidade de banda larga (eixo X) e velocidade mobile (eixo Y) para os 139 paises com dados completos. A correlacao de Pearson (r = 0.561) indica relacao moderada positiva.')

pdf.imagem('internet-08/graficos/scatter_download_upload/scatter_download_upload.png',
           'Figura 1: Dispersao Download vs Mobile com linha de regressao')

pdf.corpo('Correlacao de Pearson: r = 0.561 (moderada positiva)\n'
          'p-valor: 7.11e-13 (estatisticamente significativo)\n\n'
          'Interpretacao: Paises com banda larga mais rapida tendem a ter mobile mais rapido, '
          'mas a relacao explica apenas 31% da variacao (r2 = 0.314). '
          'Fatores como investimento em infraestrutura, regulacao e geografia tambem influenciam.')

# Questao C
pdf.add_page()
pdf.subtitulo('6. Questao C: Histogramas de Distribuicao')
pdf.corpo('Geraram-se histogramas para analisar a distribuicao das velocidades de internet entre os paises.')

pdf.imagem('internet-08/graficos/histograma_download/histograma_download.png',
           'Figura 2: Histograma da velocidade de download', w=155)

pdf.corpo('A distribuicao e assimetrica positiva (assimetria = 1.37): a maioria dos paises concentra-se em velocidades baixas, enquanto poucos paises elevam a media.')

pdf.add_page()
pdf.imagem('internet-08/graficos/histograma_upload/histograma_upload.png',
           'Figura 3: Histograma da velocidade mobile', w=155)

pdf.imagem('internet-08/graficos/histograma_comparativo/histograma_comparativo.png',
           'Figura 4: Histograma comparativo Download vs Mobile', w=155)

pdf.corpo('O histograma comparativo mostra que as velocidades de banda larga tem maior amplitude (1.62-192.68 Mbps) do que as mobile (0.53-135.62 Mbps). Ambas compartilham o formato assimetrico.')

# Questao dissertativa
pdf.add_page()
pdf.subtitulo('7. Questao Dissertativa')
pdf.sub2('"Quais fatores podem influenciar as diferencas de velocidade')
pdf.sub2('de internet entre os paises? Como essas diferencas impactam')
pdf.sub2('a economia digital global?"')
pdf.ln(3)

pdf.corpo(
    'As disparidades nas velocidades de internet entre os paises sao significativas e refletem '
    'desigualdades estruturais profundas. Conforme evidenciado pela analise dos dados, os dez paises '
    'com maiores velocidades de banda larga - liderados por Monaco (192,68 Mbps) e Singapura '
    '(192,01 Mbps) - apresentam velocidades ate 100 vezes superiores aos dez ultimos do ranking, '
    'onde o Afeganistao registra apenas 1,62 Mbps. A media global de download e de 47,21 Mbps, '
    'porem a mediana de 33,76 Mbps revela uma distribuicao assimetrica positiva (assimetria de 1,37), '
    'indicando que a maioria dos paises possui velocidades abaixo da media.\n\n'
    'Entre os fatores que explicam essas diferencas, destaca-se primeiramente o nivel de investimento '
    'em infraestrutura de telecomunicacoes. Paises desenvolvidos investem consistentemente na expansao '
    'de redes de fibra optica e tecnologia 5G, enquanto nacoes em desenvolvimento ainda dependem de '
    'infraestrutura obsoleta. A geografia tambem desempenha um papel relevante: paises menores e '
    'urbanizados, como Singapura e Monaco, conseguem cobrir seu territorio com infraestrutura de '
    'alta velocidade a um custo relativamente baixo.\n\n'
    'O ambiente regulatorio e a competicao no mercado de telecomunicacoes constituem outro fator '
    'determinante. A correlacao moderada de Pearson (r = 0,561) entre velocidade de banda larga e '
    'velocidade mobile sugere que os investimentos em infraestrutura fixa e movel nem sempre caminham '
    'juntos. Paises como Bulgaria e Croacia apresentam velocidades mobile muito superiores as de '
    'banda larga, possivelmente por terem priorizado investimentos em redes 4G/5G.\n\n'
    'O impacto dessas desigualdades na economia digital global e profundo. Paises com internet lenta '
    'enfrentam barreiras ao comercio eletronico, a educacao a distancia, ao trabalho remoto e a adocao '
    'de servicos em nuvem. A alta variancia observada nos dados (desvio padrao de 43,67 Mbps para '
    'download) ilustra como a "divisao digital" perpetua desigualdades economicas existentes, limitando '
    'o acesso de bilhoes de pessoas as oportunidades da era digital.'
)

# ============================================================
# PROBLEMA 14 — CONSUMO DE ENERGIA
# ============================================================
pdf.add_page()
pdf.titulo('Problema 14 - Consumo de Energia ao Longo do Tempo')

pdf.subtitulo('1. Objetivo')
pdf.corpo('Analisar dados de consumo de energia global por regiao e fonte de energia, visualizar o crescimento ao longo dos anos, identificar variacoes ciclicas e discutir impactos em politicas ambientais e economicas.')

pdf.subtitulo('2. Dataset')
pdf.corpo('World Energy Consumption (Kaggle). Dados historicos de 1900 a 2022 cobrindo 219 paises e 129 variaveis incluindo consumo por fonte (carvao, petroleo, gas, nuclear, renovaveis, hidro).')

pdf.tabela(
    ['Metrica', 'Valor'],
    [
        ['Entidades totais', '306'],
        ['Paises (com ISO)', '219'],
        ['Periodo', '1900 - 2022'],
        ['Colunas', '129'],
        ['Fontes de energia', '6 principais'],
        ['Consumo mundial 2022', '167.788 TWh'],
    ],
    [100, 90]
)

# Questao A
pdf.subtitulo('3. Questao A: Media de Consumo por Regiao e Fonte')
pdf.corpo('Calculou-se a media historica de consumo de energia (em TWh) para 6 regioes do mundo, segmentada por fonte de energia.')

pdf.add_page()
pdf.imagem('consumo-energia-14/graficos/media_regiao_fonte/media_regiao_fonte.png',
           'Figura 5: Media de consumo por regiao e fonte de energia')

pdf.tabela(
    ['Regiao', 'Carvao', 'Petroleo', 'Gas', 'Nuclear', 'Renovaveis', 'Hidro'],
    [
        ['Africa', '832', '1.277', '576', '21', '219', '200'],
        ['Asia', '15.171', '12.837', '5.392', '856', '2.543', '1.954'],
        ['Europe', '7.120', '11.083', '7.692', '2.187', '2.424', '1.865'],
        ['N. America', '5.031', '11.756', '7.183', '1.665', '2.268', '1.721'],
        ['Oceania', '455', '484', '225', '0', '136', '101'],
        ['S. America', '204', '1.895', '744', '30', '1.309', '1.121'],
    ],
    [30, 25, 27, 25, 27, 28, 28]
)

pdf.corpo('A Asia domina o consumo de carvao (15.171 TWh), refletindo a industrializacao de China e India. '
          'Europa e America do Norte tem consumo mais diversificado. A America do Sul destaca-se pelo uso '
          'de hidro e renovaveis, impulsionado pelo Brasil.')

# Questao B
pdf.subtitulo('4. Questao B: Crescimento do Consumo ao Longo dos Anos')
pdf.corpo('O grafico de dispersao mostra a evolucao do consumo mundial por fonte de energia ao longo do tempo. '
          'A correlacao entre consumo total e ano e de r = 0.994 (quase perfeita).')

pdf.add_page()
pdf.imagem('consumo-energia-14/graficos/scatter_consumo_tempo/scatter_consumo_tempo.png',
           'Figura 6: Crescimento do consumo de energia ao longo dos anos')

pdf.corpo('O consumo mundial cresceu de ~25.000 TWh em 1965 para mais de 167.000 TWh em 2022. '
          'O petroleo e o carvao dominam historicamente, mas as renovaveis mostram crescimento acelerado '
          'nas ultimas decadas. O gas natural cresceu consistentemente desde os anos 1960.')

# Questao C
pdf.subtitulo('5. Questao C: Variacoes no Consumo de Energia')
pdf.corpo('Como o dataset possui granularidade anual (sem dados mensais), a analise foca nas variacoes '
          'ano-a-ano para identificar padroes ciclicos.')

pdf.imagem('consumo-energia-14/graficos/variacoes_sazonais/variacoes_sazonais.png',
           'Figura 7: Variacao percentual anual do consumo de energia', w=160)

pdf.tabela(
    ['Ano', 'Variacao', 'Evento'],
    [
        ['2020', '-3.56%', 'Pandemia COVID-19'],
        ['2009', '-1.61%', 'Crise financeira global'],
        ['1980', '-0.87%', '2a crise do petroleo'],
        ['1982', '-0.54%', 'Recessao global'],
        ['1981', '-0.41%', 'Efeitos crise 1979'],
    ],
    [40, 50, 100]
)

pdf.corpo('A variacao media anual e de +2.43%. Apenas 5 anos registraram queda, todos associados a '
          'crises economicas globais. O consumo de energia e extremamente resiliente - mesmo em crises, '
          'as quedas sao pequenas e seguidas de recuperacao rapida.')

# Estatisticas descritivas
pdf.add_page()
pdf.subtitulo('6. Estatisticas Descritivas')

pdf.tabela(
    ['Fonte', 'Media (TWh)', 'Mediana', 'Desvio', 'Assimetria', 'Curtose'],
    [
        ['Total', '581.57', '45.70', '2479.64', '9.66', '111.30'],
        ['Carvao', '390.92', '36.70', '1670.76', '10.02', '119.41'],
        ['Petroleo', '491.26', '140.24', '1234.73', '6.05', '41.01'],
        ['Gas', '310.74', '76.31', '860.21', '5.74', '36.35'],
        ['Nuclear', '86.95', '0.00', '271.28', '5.52', '35.08'],
        ['Renovaveis', '117.39', '20.73', '351.43', '9.22', '126.74'],
    ],
    [30, 30, 28, 28, 37, 37]
)

pdf.corpo('As distribuicoes sao extremamente assimetricas (assimetria 5-10) e leptocurticas '
          '(curtose 35-127), indicando que poucos paises (China, EUA, India) concentram a maior '
          'parte do consumo enquanto a grande maioria consome quantidades muito menores.')

# Questao dissertativa
pdf.subtitulo('7. Questao Dissertativa')
pdf.sub2('"Como a mudanca no consumo de energia pode impactar')
pdf.sub2('politicas ambientais e economicas?"')
pdf.ln(3)

pdf.corpo(
    'As transformacoes no padrao de consumo energetico global representam um dos principais vetores '
    'de mudanca tanto nas politicas ambientais quanto nas estrategias economicas das nacoes. A analise '
    'dos dados revela que o consumo mundial de energia primaria cresceu de forma quase linear ao longo '
    'das ultimas decadas (r = 0,994), passando de cerca de 25.000 TWh em 1965 para mais de 167.000 TWh '
    'em 2022.\n\n'
    'Essa trajetoria impacta diretamente as politicas ambientais. Os dados mostram que combustiveis '
    'fosseis ainda representam a maior parcela do consumo. A Asia apresenta um consumo medio de carvao '
    'de 15.171 TWh, valor tres vezes superior ao de qualquer outra regiao, o que esta associado as '
    'elevadas emissoes de gases de efeito estufa do continente. Essa concentracao pressiona governos '
    'a adotar metas de reducao de emissoes e mecanismos de precificacao de carbono.\n\n'
    'No ambito economico, a analise das variacoes anuais revela uma relacao intima entre consumo '
    'energetico e ciclos economicos. Os unicos cinco anos de queda coincidem com crises significativas: '
    'a pandemia de COVID-19 provocou a maior reducao historica (-3,56% em 2020), seguida pela crise '
    'financeira de 2009 (-1,61%) e pelas crises do petroleo de 1979-1982.\n\n'
    'A transicao energetica em curso tambem gera impactos economicos profundos. O crescimento das '
    'fontes renovaveis cria oportunidades em novos setores, mas ameaca economias dependentes de '
    'combustiveis fosseis. A America do Sul, com alta participacao de hidro (1.121 TWh) e renovaveis '
    '(1.309 TWh), demonstra que a diversificacao da matriz e possivel.\n\n'
    'Portanto, as mudancas no consumo de energia sao um fator determinante que molda acordos climaticos, '
    'define competitividade economica e influencia a qualidade de vida de bilhoes de pessoas.'
)

# ============================================================
# CONCLUSAO
# ============================================================
pdf.add_page()
pdf.titulo('Conclusao')

pdf.corpo(
    'As duas atividades desenvolvidas demonstram o poder da analise de dados para compreender '
    'fenomenos globais complexos. No Problema 08, a analise de velocidade de internet revelou '
    'uma desigualdade digital significativa entre paises, com distribuicao assimetrica e '
    'correlacao moderada entre infraestrutura fixa e movel. No Problema 14, o estudo do consumo '
    'de energia evidenciou um crescimento quase linear ao longo de decadas, com forte dependencia '
    'de combustiveis fosseis e variacoes associadas a crises economicas globais.\n\n'
    'Ambos os projetos utilizaram Python com as bibliotecas Pandas, Matplotlib, Seaborn, Scipy e '
    'Plotly, seguindo um pipeline de analise que inclui: exploracao inicial dos dados, calculo de '
    'estatisticas descritivas, geracao de visualizacoes estaticas e interativas, e interpretacao '
    'dos resultados com embasamento nos dados.\n\n'
    'Todo o codigo-fonte e os resultados estao disponiveis no repositorio:\n'
    'github.com/antonionetu/big-data'
)

pdf.subtitulo('Ferramentas Utilizadas')
pdf.tabela(
    ['Ferramenta', 'Uso'],
    [
        ['Python 3.12', 'Linguagem principal'],
        ['Pandas', 'Manipulacao e analise de dados'],
        ['Matplotlib/Seaborn', 'Graficos estaticos'],
        ['Plotly', 'Dashboards interativos'],
        ['Scipy', 'Regressao linear e correlacao de Pearson'],
        ['KaggleHub', 'Download dos datasets'],
    ],
    [70, 120]
)

# Salvar
pdf.output('documentacao_bigdata.pdf')
print('PDF gerado: documentacao_bigdata.pdf')

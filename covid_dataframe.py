import pandas as pd

arquivo = "/Users/alexandrethadeu/Documents/Python/Teste/dados/covid.csv"
covid_df = pd.read_csv(arquivo, sep=";", engine="python")

# Dados
tipos_dados = pd.DataFrame(covid_df.dtypes, columns=["Tipo de Dado"])
tipos_dados.columns.name = 'Variavel'
tipos_dados

# Shape
shape_obs = covid_df.shape[0]  # obs
shape_variavel = covid_df.shape[1]  # variaveis
print(
    f'A base de dados apresenta {shape_obs} observações e {shape_variavel} variaveis')

# Dez primeiras obs
covid_head = covid_df.head(10)
covid_head

# Casos e Obitos
total_obitos = covid_df['obitos'].sum()
total_casos = covid_df['casos_novos'].sum()
info = {
    'Casos': [total_casos],
    'Obitos': [total_obitos]
}
data = pd.DataFrame(info)

# Agrupando por municipios
group_municipio = covid_df.groupby('municipio')
total_obitos = group_municipio['obitos'].sum()
obitos_df = pd.DataFrame(total_obitos)
obitos_df.sort_values(['obitos'], ascending=False).head(10)

# Somando total de casos
total_casos = group_municipio['casos_novos'].sum()
casos_df = pd.DataFrame(total_casos)
casos_df.sort_values(['casos_novos'], ascending=False).head(10)

# Criado o df2 como covid_resume e adicionando letalidade
covid_resume = casos_df
covid_resume['obitos'] = obitos_df['obitos']
covid_resume['letalidade'] = covid_resume['obitos'] / \
    covid_resume['casos_novos']
covid_resume['letalidade'] = covid_resume['letalidade']
covid_resume.sort_values(['letalidade'], ascending=False).head(10)

# Agrupando um df para populacao
total_habitantes_df = pd.DataFrame(group_municipio['pop'].last())

# Adicionando no df2 casos_pc e obitos_pc
covid_resume['pop'] = total_habitantes_df['pop']
covid_resume['casos_pc'] = (
    covid_resume['casos_novos'] / covid_resume['pop']) * 100000
covid_resume['obitos_pc'] = (
    covid_resume['obitos'] / covid_resume['pop']) * 100000
covid_resume['casos_pc'] = covid_resume['casos_pc'].round()
covid_resume['obitos_pc'] = covid_resume['obitos_pc'].round()
covid_resume.sort_values(['obitos_pc'], ascending=False).head(10)

# Agrupando casos e obitos por mes e montando grafico em linha da evoulacao
group_meses = covid_df.groupby('mes')
casos_mes_df = pd.DataFrame(group_meses['casos_novos'].sum())
casos_mes_df.sort_values(['casos_novos'], ascending=True)
obitos_mes_df = pd.DataFrame(group_meses['obitos'].sum())
obitos_mes_df.sort_values(['obitos'], ascending=True)
obitos_mes_df['casos'] = casos_mes_df['casos_novos']
obitos_mes_df = obitos_mes_df.reindex(['Fevereiro', 'Março', 'Abril', 'Maio',
                                       'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro'])
obitos_mes_df
lines = obitos_mes_df.plot.line(subplots=True)

# Agrupando região para montar quantos municipios ha em cada regiao
covid_df2 = covid_df.drop_duplicates(['municipio'])
group_regiao = covid_df2.groupby('gde_regiao')
regiao_df = pd.DataFrame(group_regiao['municipio'].size())
regiao_df

# Adicionando densidade ao df2
area_df = pd.DataFrame(group_municipio['area'].last())
covid_resume['densidade'] = total_habitantes_df['pop'] / area_df['area']
covid_resume.sort_values(['densidade'], ascending=False).head(15)

# Gráfico em barras para mostar a letalidade por região
covid_resume.sort_values(['densidade', 'casos_pc'], ascending=False).head(15)
municipios_regiao = pd.DataFrame(group_municipio['gde_regiao'].last())
municipios_regiao
covid_resume['regiao'] = municipios_regiao['gde_regiao']
df_bar = covid_resume.groupby(['regiao'])['letalidade'].mean()
bar = df_bar.plot.bar()
bar

total_habitantes_60_df = pd.DataFrame(group_municipio['pop_60'].last())
covid_resume['pop_60'] = total_habitantes_60_df['pop_60']
covid_resume

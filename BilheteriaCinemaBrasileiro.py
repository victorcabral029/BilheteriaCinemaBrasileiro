#!/usr/bin/env python
# coding: utf-8

# ### O projeto a seguir propõe importar e fazer uma análise dos dados da Bilheteria do Cinema Brasileiro no ano de 2019, estes obtidos em https://oca.ancine.gov.br/cinema. Neste, algumas perguntas serão respondidas utilizando bibliotecas Python de Ciência de Dados, estas perguntas são :
# 
# #### * Números totais de público e arrecadação para Filmes Brasileiros e Estrangeiros
# #### * Maiores e menores Públicos e Arrecadação dos Filmes no ano
# #### * Números de Gêneros de Filmes, Distribuidoras e Municípios 
# #### * Números em Relação ao Mês de Estreia dos Filmes
# #### * Mapas do Brasil com os Valores identificados. Público, arrecadação, títulos exibidos, quantidade de cinemas e valor médio por exibição  

# ### Bibliotecas

# In[32]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
get_ipython().magic(u'matplotlib inline')
pd.set_option('mode.chained_assignment', None)


# ### Import das Planilhas

# In[53]:


xls = pd.ExcelFile('cinema.xlsx')
dfMunicipios = pd.read_excel(xls, 'Ranking_por_Municípios')
dfDadosGerais = pd.read_excel(xls,'Dados_Gerais')
dfFilmes = pd.read_excel(xls, 'Ranking_Filmes_Exibidos')
dfUf = pd.read_excel(xls, 'Ranking_por_UF')
dfGrupoExibidor = pd.read_excel(xls, 'Ranking_por_Grupo_Exibidor')
dfComplexo = pd.read_excel(xls,'Ranking_por_Complexos')


# ## Publico Filmes Brasileiros x Público Filmes Estrangeiros

# In[54]:


dfDadosGerais.reset_index()


# In[55]:


df = dfDadosGerais[dfDadosGerais['Tipo']=='Público 2019']
df.plot(kind='bar', cmap='inferno', figsize=(10,6))
plt.legend(loc=2, prop={'size': 15})


# ### Maiores Públicos de FIlmes Brasileiros

# In[56]:


dfFilmesBr = dfFilmes[dfFilmes['Nacionalidade']=="Filmes Brasileiros"]


# In[57]:


dfFilmesBr[['Título da Obra','Público']].sort_values(by=['Público'],ascending=False).head(10)


# ### Menores Públicos de Filmes Brasileiros

# In[58]:


dfFilmesBr[['Título da Obra','Público']].sort_values(by=['Público']).head(10)


# ### Maiores Públicos de Filmes Estrangeiros

# In[59]:


dfFilmesEs = dfFilmes[dfFilmes['Nacionalidade']=="Filmes Estrangeiros"]
dfFilmesEs[['Título da Obra','Público']].sort_values(by=['Público'],ascending=False).head(10)


# ### Menores Públicos de Filmes Estrangeiros

# In[60]:


dfFilmesEs[['Título da Obra','Público']].sort_values(by=['Público']).head(10)


# ## Renda Filmes Brasileiros x Renda Filmes Estrangeiros

# In[61]:


df = dfDadosGerais[dfDadosGerais['Tipo']=='Renda (R$) 2019']
df.plot(kind='bar', cmap='inferno', figsize=(10,6))
plt.legend(loc=2, prop={'size': 15})


# ### Maiores rendas em Filmes Brasileiros

# In[62]:


dfFilmesBr[['Título da Obra','Renda (R$)']].sort_values(by=['Renda (R$)'],ascending=False).head(10)


# ### Maiores Rendas em Filmes Estrangeiros

# In[63]:


dfFilmesEs[['Título da Obra','Público']].sort_values(by=['Público'],ascending=False).head(10)


# ### Gêneros de Filmes Brasileiros

# In[75]:


dfGeneroBr = dfFilmesBr.groupby(['Gênero'])[['Público','Renda (R$)']].sum()
dfGeneroBr


# ### Gêneros de Filmes Estrangeiros

# In[77]:


dfGeneroEs = dfFilmesEs.groupby(['Gênero'])[['Público','Renda (R$)']].sum()
dfGeneroEs


# ### Distribuidoras de Filmes Brasileiros

# In[15]:


dfDistBr = dfFilmesBr.groupby(['Distribuidoras'])[['Público','Renda (R$)']].sum()
dfDistBr.sort_values(by="Público",ascending=False)


# ### Distribuidoras de Filmes Estrangeiros

# In[16]:


dfDistEs = dfFilmesEs.groupby(['Distribuidoras'])[['Público','Renda (R$)']].sum()
dfDistEs.sort_values(by="Público",ascending=False).head(20)


# ### Municípios com Maior Público

# In[17]:


dfMunicipios = dfMunicipios.dropna()
dfMunicipios.sort_values(by="Público",ascending=False).head(15)


# ### Municípios com Menor Público

# In[18]:


dfMunicipios.sort_values(by="Público").head(15)


# ### Público e Renda por Mês de Estreia dos Filmes

# In[37]:


dfMes = dfFilmes[['Data de Lançamento','Público','Renda (R$)']]
sMes = dfMes['Data de Lançamento'].astype(str)
sMes = sMes.str.slice(start=5,stop=7)
dfMes['Mes'] = sMes


# In[38]:


soma = dfMes.groupby('Mes').sum()
soma.reset_index()


# In[39]:


cmap = sns.color_palette("OrRd",12)
sns.set(font_scale=1.3)
sns.set_style('whitegrid')


# In[40]:


plt.figure(figsize=(10,5))
sns.barplot(x=soma.index,y=soma['Público'],palette=cmap)
plt.title('Público por Mês de Estreia')
plt.xlabel('Mês do ano')
plt.ylabel('Público (Em Milhões)')


# In[41]:


plt.figure(figsize=(10,5))
sns.barplot(x=soma.index,y=soma['Renda (R$)'], palette=sns.color_palette('OrRd',12))
plt.title('Renda de ingressos por Mês de Estreia')
plt.xlabel('Mês do ano')
plt.ylabel('Renda em Mlihões de Reais')


# In[42]:


import geopandas as gpd
ufs = gpd.read_file('mapa.gpkg', layer="lim_unidade_federacao_a")
dfMapa = dfMunicipios
dfMapa = dfMapa.drop(columns='Município').dropna()
ufs.rename({'sigla':'UF'}, axis=1, inplace = True)


# In[43]:


dfEstados = dfMapa.groupby('UF').sum()
total = ufs.merge(dfEstados, on='UF')


# ### Público por Estado

# In[44]:


total.plot(column='Público',
          cmap = 'OrRd',
          figsize = (16,10),
          legend = True,
          edgecolor = 'black',
          legend_kwds = {'label':'Público por Estado'})


# ### Renda de Bilheteria por Estado

# In[45]:


total.plot(column='Renda (R$)',
          cmap = 'OrRd',
          figsize = (16,10),
          legend = True,
          edgecolor = 'black',
          legend_kwds = {'label':'Renda (Em Reais) de Bilheteria por Estado'})


# ### Número de Títulos Exibidos por Estado

# In[46]:


total.plot(column='Títulos Exibidos',
          cmap = 'OrRd',
          figsize = (16,10),
          legend = True,
          edgecolor = 'black',
          legend_kwds = {'label':'Número de Títulos Exibidos por Estado'})


# ### Quantidade de Cinema por Estados

# In[47]:


dfNumCinemas = dfComplexo.groupby('UF').count()
total2 = ufs.merge(dfNumCinemas, on='UF')


# In[48]:


total2.plot(column='Município',
          cmap = 'OrRd',
          figsize = (16,10),
          legend = True,
          edgecolor = 'black',
          legend_kwds = {'label':'Número de Complexos de Cinema'})


# ### Média de preço por pessoa em uma exibição

# In[49]:


arr = dfUf['Renda (R$)'].values/ dfUf['Público'].values
dfUf['perCapita'] = arr


# In[50]:


dfUf.dropna(inplace=True)


# In[51]:


f, axes = plt.subplots(1,2, figsize=(18,6))

total3 = ufs.merge(dfUf, on='UF')
total3.plot(column='perCapita',
          cmap = 'OrRd',
          legend = True,
          edgecolor = 'black',
          legend_kwds = {'label':'Valor médio de arrecadação por pessoa, em uma exibição','orientation': "horizontal"},
          ax=axes[0])

sns.distplot(arr, ax=axes[1], color='red')
plt.xlabel('Valor médio de arrecadação por pessoa, em uma exibição')



# In[ ]:





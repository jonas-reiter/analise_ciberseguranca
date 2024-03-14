import pandas as pd
import streamlit as st

# Importar dados

df = pd.read_csv('https://raw.githubusercontent.com/jonas-reiter/analise_ciberseguranca/main/Base%20de%20Dados%20-%20Ataques%20Cibern%C3%A9ticos.csv', sep=';')
# Listar Anos unicos
anos_unicos = pd.unique(df['Ano'])
anos_unicos.sort()
# Listar meses unicos
meses_unicos = pd.unique(df['Mes'])

# criar um titulo para o Streamlit
st.title('Ataques Cibernéticos no Brasil')
cols = st.columns(3)
with cols[0]:
    ano_escolhido = st.slider('Ano', min_value=2010, max_value=2019, value=(2010, 2019))
with cols[1]:
    mes_escolhido = st.selectbox('Mês', meses_unicos, index=None)
with cols[2]:
    st.text(f'Categoria')
    colunas_internas = st.columns(3)
    categorias = {}
    with colunas_internas[0]:
        categorias['Baixo'] = st.checkbox('Baixo', True)
    with colunas_internas[1]:
        categorias['Medio'] = st.checkbox('Medio', True)
    with colunas_internas[2]:
        categorias['Alto'] = st.checkbox('Alto', True)


def classificar(valor):
    if valor < 100000:
        return 'Baixo'
    elif valor < 200000:
        return 'Medio'
    return 'Alto'


df['Categoria'] = df['Total'].apply(classificar)


categorias_filtrar = []
for chave, valor in categorias.items():
    if valor:
        categorias_filtrar.append(chave)
df_tabela = df[df['Categoria'].isin(categorias_filtrar)]

query = f'Ano >= {ano_escolhido[0]} & Ano <= {ano_escolhido[1]}'
df_tabela = df_tabela.query(query)
if mes_escolhido is not None:
    df_tabela = df_tabela.query(f'Mes == "{mes_escolhido}"')
df_tabela = df_tabela.query(query)

# criando tabela
st.dataframe(df_tabela, hide_index=1, use_container_width=True,
             column_config={
                 'Ano': st.column_config.NumberColumn(
                     format='%d'),
             }
             )
df_agrupado_ano = pd.DataFrame(df.groupby(['Ano']).sum('Total'))

tipos_ataque = list(df.columns[3:-1])
tipos_ataque_dict = {}

colunas = st.columns(len(tipos_ataque))
for indice, tipo in enumerate(tipos_ataque):
    with colunas[indice]:
        tipos_ataque_dict[tipo] = st.toggle(tipo, True)

colunas_dropar = ['Total']
for chave, valor in tipos_ataque_dict.items():
    if not valor:
        colunas_dropar.append(chave)

df_agrupado_ano.drop(columns=colunas_dropar, inplace=True)
df_agrupado_ano = df_agrupado_ano.query(query)
total = pd.DataFrame(df_agrupado_ano.sum())
total.columns = ['total']
st.area_chart(df_agrupado_ano, use_container_width=True)
total.sort_values(by='total', ascending=False, axis='rows', inplace=True)
# total.reset_index(inplace=True)
st.dataframe(total)
st.bar_chart(total, use_container_width=True)

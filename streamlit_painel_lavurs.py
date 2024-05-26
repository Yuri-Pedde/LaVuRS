import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import geopandas as gpd
import unicodedata
from streamlit_extras.app_logo import add_logo 
from streamlit_elements import elements, mui, html
from shapely.geometry import MultiPolygon
import altair as alt

pd.options.display.max_columns=None
st.set_page_config(
    page_title="LaVuRS",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state='collapsed'
)

container1 = st.container()
with container1:
    col1, col2, col3 = st.columns([2,9,2])
    with col1:
        st.write('<div style="margin-top: 15px;">', unsafe_allow_html=True)
        st.write('</div>', unsafe_allow_html=True)
        st.write('<div style="display: flex; justify-content: left;">', unsafe_allow_html=True)
        st.image(r"Feevale_symbol_and_logo_(horizontal).svg.png", width=200)
        st.write('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<h1 style="text-align: center;color:#000000;font-size:32px;margin-top:0px;margin-bottom:0px;">{"PAINEL DE DESASTRES DA BACIA HIDROGRÁFICA DO RIO DOS SINOS"}</h1>', unsafe_allow_html=True)    
        st.markdown(f'<h1 style="text-align: center;color:#000000;font-size:18px;margin-top:0px;margin-bottom:0px;">{"LABORATÓRIO DE VULNERABILIDADES, RISCOS E SOCIEDADE | OFICINA DE DEFESA CIVIL DO VALE DO PARANHANA"}</h1>', unsafe_allow_html=True)
        st.markdown(f'<h1 style="text-align: center;color:#000000;font-size:13px;margin-top:0px;margin-bottom:0px;">{f"PAINEL ATUALIZADO EM TEMPO REAL"}</h1>', unsafe_allow_html=True)
        
    with col3:    
        st.write('<div style="display: flex; justify-content: right;">', unsafe_allow_html=True)
        st.image(r'LOGO_LAVURS-removebg-preview.png', width=250)
        st.write('</div>', unsafe_allow_html=True)
    st.write('<hr style="border: 0; height: 4px; background-color: black; margin: 0 auto;">', unsafe_allow_html=True)
st.markdown(
    """
    <style>
    /* Define a largura mínima da sidebar */
    .css-1d391kg {
        min-width: 150px;
        max-width: 150px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown("""<style>
        #root > div:nth-child(1) > div.withScreencast > div > div > div > section.st-emotion-cache-1gv3huu.eczjsme16 > div.st-emotion-cache-6qob1r.eczjsme8
        {
        background: linear-gradient(to bottom, #66b366 0%, #66b366 10%, #80cc80 20%, #99e599 40%, #b3e5c0 60%, white 100%);
        }
        </style>""", unsafe_allow_html=True)
        
st.markdown("""<style>
            #root > div:nth-child(1) > div.withScreencast > div > div > div > section.st-emotion-cache-vk3wp9.eczjsme11 > div.st-emotion-cache-6qob1r.eczjsme3 > div.st-emotion-cache-79elbk.eczjsme10 > ul > li:nth-child(1) > div
            {
                background: linear-gradient(to bottom, #66b366 0%, #66b366 10%, #80cc80 20%, #99e599 40%, #b3e5c0 60%, white 100%);
            }
            #root > div:nth-child(1) > div.withScreencast > div > div > div > section.st-emotion-cache-vk3wp9.eczjsme11 > div.st-emotion-cache-6qob1r.eczjsme3 > div.st-emotion-cache-79elbk.eczjsme10 > ul > li:nth-child(2) > div
            {
                background: linear-gradient(to bottom, #66b366 0%, #66b366 10%, #80cc80 20%, #99e599 40%, #b3e5c0 60%, white 100%);
            }
            #root > div:nth-child(1) > div.withScreencast > div > div > div > section.st-emotion-cache-vk3wp9.eczjsme11 > div.st-emotion-cache-6qob1r.eczjsme3 > div.st-emotion-cache-79elbk.eczjsme10 > ul > li:nth-child(2) > div > a > span
            {
                color: black;
                 
            }
            </style>""", unsafe_allow_html=True)
st.sidebar.title("Navegação")
# CSS para estilizar os itens da sidebar
page = st.sidebar.radio("", ["Painel LaVuRS", "Sobre o Painel"])

if page=="Painel LaVuRS":
    @st.cache_data #nao precisa fazer o loading o tempo todo
    def load_geodata(url):
        gdf = gpd.read_file(url)
        return gdf
    
    def load_df(url):
        df_x = pd.read_excel(url)
        return df_x
        
    @st.cache_data
    def load_df2(url):
        df_x = pd.read_excel(url, sheet_name="Página1")
        return df_x
    def remover_acentos(text):
        return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
    df_original = load_df('https://docs.google.com/spreadsheets/d/e/2PACX-1vQTq8R52z3oc9uW3FUsCjym25giwCvrPfcmLwWyc8ugt-c4g5uR-ZKUG3EOBdIP62sLnWSP68dnVkUw/pub?output=xlsx')
    df_original['Fonte'] = df_original['Fonte'].replace('', 'Sem fonte')
    df_original['Ano'] = df_original['Ano'].astype(int).astype(float)
    df_original['Década'] = (df_original['Ano'] // 10) * 10
    df_original['Década'] = df_original['Década'].astype(int).astype(str)
    df_original['Ano'] = df_original['Ano'].astype(int)
    df_original['Década'] = df_original['Década'].astype(int)
    df_dict = load_df2('https://docs.google.com/spreadsheets/d/e/2PACX-1vQTq8R52z3oc9uW3FUsCjym25giwCvrPfcmLwWyc8ugt-c4g5uR-ZKUG3EOBdIP62sLnWSP68dnVkUw/pub?output=xlsx')
    df_dict['Municipio'] = df_dict['Municipio'].apply(lambda x: remover_acentos(x))
    df_dict['Municipio'] = df_dict['Municipio'].apply(lambda x: x.strip().upper())
    municipio_to_regiao = dict(zip(df_dict.Municipio, df_dict.Regiao_BHRS))
    # Função para obter a região a partir dos municípios
    def get_regiao(municipios):
        # Separar os municípios e obter as regiões correspondentes
        regioes = set()
        for mun in municipios.split('; '):
            mun = mun.strip()
            if mun in municipio_to_regiao:
                regioes.add(municipio_to_regiao[mun])
            else:
                regioes.add("OUTRAS BACIAS")
        return '; '.join(regioes)

    df_original["Municipio"] = df_original["Municipio"].apply(lambda x: remover_acentos(x))
    df_original["Municipio"] = df_original["Municipio"].apply(lambda x: x.strip().upper())
    df_original["Regiao_BHRS"] = df_original["Municipio"].apply(get_regiao)

    eventos_unicos = df_original['Evento'].str.split('; ').explode().str.upper().unique()
    
    df_original['Municipio'] = df_original['Municipio'].str.upper().apply(lambda x: remover_acentos(x))
    municipios_unicos = df_original['Municipio'].str.split('; ').explode().str.upper().unique()
    municipios_unicos_strip_dupli = pd.DataFrame(list(municipios_unicos))[0].str.strip().drop_duplicates()
    municipios_unicos_strip_dupli_df = pd.DataFrame(municipios_unicos_strip_dupli)
    municipios_unicos_strip_dupli_df[0] = municipios_unicos_strip_dupli_df[0].astype(str).apply(lambda x: remover_acentos(x))
    municipios_unicos_strip_dupli_df = municipios_unicos_strip_dupli_df.rename(columns={0:'Municipio'})
    municipios_unicos_strip_dupli_df['Municipio'] = municipios_unicos_strip_dupli_df['Municipio'].apply(lambda x: x.upper().strip())
    municipios_unicos_strip_dupli_df = municipios_unicos_strip_dupli_df.set_index('Municipio')
    municipios_unicos_strip_dupli_df = municipios_unicos_strip_dupli_df.drop(['BHRS','VALE DOS SINOS'])
    municipios_unicos_strip_dupli_df2 = municipios_unicos_strip_dupli_df.reset_index()
    
    lista_municipios_bacia = ['Araricá', 'Cachoeirinha', 'Campo Bom', 'Canela', 'Canoas', 'Capela de Santana', 'Caraá', 'Dois Irmãos', 
                              'Estância Velha', 'Esteio', 'Glorinha', 'Gramado','Gravataí', 'Igrejinha', 'Ivoti', 'Nova Hartz', 'Nova Santa Rita', 
                              'Novo Hamburgo', 'Osório', 'Parobé', 'Portão', 'Riozinho', 'Rolante', 'Santa Maria do Herval', 'Santo Antônio da Patrulha', 
                              'São Francisco de Paula', 'São Leopoldo', 'São Sebastião do Caí', 'Sapiranga', 'Sapucaia do Sul', 'Taquara', 'Três Coroas']
    
    df_lista_municipios_bacia = pd.DataFrame(lista_municipios_bacia)
    df_lista_municipios_bacia[0] = df_lista_municipios_bacia[0].astype(str).apply(lambda x: remover_acentos(x))
    df_lista_municipios_bacia = df_lista_municipios_bacia.rename(columns={0:'Municipio'})
    df_lista_municipios_bacia['Municipio'] = df_lista_municipios_bacia['Municipio'].apply(lambda x: x.upper().strip())
    
    municipios_unicos_filtrofinal = pd.merge(municipios_unicos_strip_dupli_df2,df_lista_municipios_bacia, on='Municipio', how='inner')
    
    container_filtros = st.container()
    with container_filtros:
        #st.write('<div style="margin-top: 15px;">', unsafe_allow_html=True)
        #st.write('</div>', unsafe_allow_html=True)
        coluna1,coluna1_5, coluna2, coluna2_5, coluna3, coluna3_5, coluna4, coluna4_5, coluna5 = st.columns([1,0.1,1,0.1,1,0.1,1,0.1,1])
        
        st.markdown(f"""
        <style>
        #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-bm2z3a.ea3mdgi8 > div.block-container.st-emotion-cache-1jicfl2.ea3mdgi5 > div > div > div > div:nth-child(6) > div > div > div.st-emotion-cache-ocqkz7.e1f1d6gn5
        {{
            background: linear-gradient(to bottom, #66b366 0%, #66b366 2%, #80cc80 4%, #99e599 6%, #b3e5c0 15%, white 20%);
            box-shadow: 0px 0px 5px 5px rgba(0, 0, 0, 0.25);
            padding: 20px;
            border-radius: 15px;
            border: 3px solid green;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 14vh;
        }}
        </style>
        """, unsafe_allow_html=True)
        
        with coluna1:
            
            lista_decadas_todas_filtro = list(df_original['Década'].unique())
            lista_decadas_todas_filtro.insert(0,'Todas as décadas')
            decada = st.selectbox("SELECIONE A DÉCADA", lista_decadas_todas_filtro, index=0, format_func=lambda x: x)
            st.markdown(
                f"""
                <style>
                #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-bm2z3a.ea3mdgi8 > div.block-container.st-emotion-cache-1jicfl2.ea3mdgi5 > div > div > div > div:nth-child(6) > div > div > div > div:nth-child(1) > div > div > div > div:nth-child(1) > div
                {{                
                    box-shadow: 0px 0px 5px 5px rgba(0, 0, 0, 0.25);
                    border: 2px solid green;
                    border-radius: 15px;
                    padding: 10px;
                }}
                </style>
                """,
                unsafe_allow_html=True
            )
            st.markdown(
                """
                <style>
                #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-bm2z3a.ea3mdgi8 > div.block-container.st-emotion-cache-1jicfl2.ea3mdgi5 > div > div > div > div:nth-child(6) > div > div > div.st-emotion-cache-ocqkz7.e1f1d6gn5 > div:nth-child(1) > div > div > div > div:nth-child(1) > div > div > div
                {
                    background-color: #e0ffe0; /* Verde bem clarinho */
                    border: 1px solid lightgreen; /* Borda verde */
                    border-radius: 8px;
                    padding: 0px;
                    max-width: calc(100%);
                }
                </style>
                """,
                unsafe_allow_html=True
            )
            st.markdown(
                f"""
                <style>
                #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-bm2z3a.ea3mdgi8 > div.block-container.st-emotion-cache-1jicfl2.ea3mdgi5 > div > div > div > div:nth-child(6) > div > div > div.st-emotion-cache-ocqkz7.e1f1d6gn5 > div:nth-child(1) > div > div > div > div:nth-child(1) > div > label 
                {{
                    text-align: center;
                    margin: 0 auto; /* Centraliza horizontalmente */
                    display: table;
                }}
                </style>
                """,
                unsafe_allow_html=True
            )
            if decada != "Todas as décadas":
                anos = sorted(df_original[df_original['Década'] == decada]['Ano'].unique())
                #df_decada_filtrada_ou_nao = df_original[df_original['Década'] == decada]
            else:
                anos = sorted(df_original['Ano'].unique())
                #df_decada_filtrada_ou_nao = df_original.copy()
            anos.insert(0, "Todos os anos")       
        with coluna2:
                   
            ano = st.selectbox("SELECIONE O ANO", anos, index=0, format_func=lambda x: x)
            st.markdown(
                f"""
                <style>
                #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-bm2z3a.ea3mdgi8 > div.block-container.st-emotion-cache-1jicfl2.ea3mdgi5 > div > div > div > div:nth-child(6) > div > div > div.st-emotion-cache-ocqkz7.e1f1d6gn5 > div:nth-child(3) > div > div > div > div:nth-child(1) > div 
                {{
                    box-shadow: 0px 0px 5px 5px rgba(0, 0, 0, 0.25);
                    border: 2px solid green;
                    border-radius: 15px;
                    padding: 10px;
                }}
                </style>
                """,
                unsafe_allow_html=True
                
            )        
            st.markdown(
                f"""
                <style>
                #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-bm2z3a.ea3mdgi8 > div.block-container.st-emotion-cache-1jicfl2.ea3mdgi5 > div > div > div > div:nth-child(6) > div > div > div.st-emotion-cache-ocqkz7.e1f1d6gn5 > div:nth-child(3) > div > div > div > div:nth-child(1) > div > div > div {{
                    background-color: #e0ffe0; /* Verde bem clarinho */
                    border: 1px solid lightgreen; /* Borda verde */
                    border-radius: 8px;
                    padding: 0px;
                    max-width: calc(100%);
                }}
                </style>
                """,
                unsafe_allow_html=True
            )
            st.markdown(
                f"""
                <style>
                #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-bm2z3a.ea3mdgi8 > div.block-container.st-emotion-cache-1jicfl2.ea3mdgi5 > div > div > div > div:nth-child(6) > div > div > div.st-emotion-cache-ocqkz7.e1f1d6gn5 > div:nth-child(3) > div > div > div > div:nth-child(1) > div > label 
                {{
                    text-align: center;
                    margin: 0 auto; /* Centraliza horizontalmente */
                    display: table;
                }}
                </style>
                """,
                unsafe_allow_html=True
            )
    
            df_original['Regiao_BHRS'] = df_original['Regiao_BHRS'].apply(lambda x: x.replace(" E ", "; ") if " E " in x else x)
            #st.dataframe(df_original['Regiao_BHRS'])
            df_regioes_lavurs_inicio = df_original.assign(Regiao_BHRS=df_original['Regiao_BHRS'].str.split('; ')).explode('Regiao_BHRS')
            #st.write(len(df_regioes_lavurs_inicio))
            df_regioes_lavurs_inicio_alto = df_regioes_lavurs_inicio[df_regioes_lavurs_inicio['Regiao_BHRS']=='ALTO SINOS']
            df_regioes_lavurs_inicio_baixo = df_regioes_lavurs_inicio[df_regioes_lavurs_inicio['Regiao_BHRS']=='BAIXO SINOS']
            df_regioes_lavurs_inicio_medio = df_regioes_lavurs_inicio[df_regioes_lavurs_inicio['Regiao_BHRS']=='MEDIO SINOS']
            df_regioes_lavurs_inicio = pd.concat([df_regioes_lavurs_inicio_alto, df_regioes_lavurs_inicio_medio, df_regioes_lavurs_inicio_baixo])
            if ano == "Todos os anos" and decada != "Todas as décadas":
                regioes = sorted(df_regioes_lavurs_inicio[df_regioes_lavurs_inicio['Década'] == decada]['Regiao_BHRS'].unique())
            elif ano != "Todos os anos" and decada != "Todas as décadas":
                regioes = sorted(df_regioes_lavurs_inicio[(df_regioes_lavurs_inicio['Década'] == decada)&(df_regioes_lavurs_inicio['Ano'] == ano)]['Regiao_BHRS'].unique())
            elif ano != "Todos os anos" and decada == "Todas as décadas":
                regioes = sorted(df_regioes_lavurs_inicio[df_regioes_lavurs_inicio['Ano'] == ano]['Regiao_BHRS'].unique())
            else:
                regioes = sorted(df_regioes_lavurs_inicio['Regiao_BHRS'].unique())
            regioes.insert(0, 'Todas as regiões')      
    
        with coluna3:
    
            regiao = st.selectbox("SELECIONE A REGIÃO DA BHRS", regioes, index=0, format_func=lambda x: x)
            st.markdown(
                f"""
                <style>
                #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-bm2z3a.ea3mdgi8 > div.block-container.st-emotion-cache-1jicfl2.ea3mdgi5 > div > div > div > div:nth-child(6) > div > div > div.st-emotion-cache-ocqkz7.e1f1d6gn5 > div:nth-child(5) > div > div > div > div:nth-child(1) > div
                {{                
                    box-shadow: 0px 0px 5px 5px rgba(0, 0, 0, 0.25);
                    border: 2px solid green;
                    border-radius: 15px;
                    padding: 10px;
                }}
                </style>
                """,
                unsafe_allow_html=True
            )
            st.markdown(
                """
                <style>
                #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-bm2z3a.ea3mdgi8 > div.block-container.st-emotion-cache-1jicfl2.ea3mdgi5 > div > div > div > div:nth-child(6) > div > div > div.st-emotion-cache-ocqkz7.e1f1d6gn5 > div:nth-child(5) > div > div > div > div:nth-child(1) > div > div > div
                {
                    background-color: #e0ffe0; /* Verde bem clarinho */
                    border: 1px solid lightgreen; /* Borda verde */
                    border-radius: 8px;
                    padding: 0px;
                    max-width: calc(100%);
                }
                </style>
                """,
                unsafe_allow_html=True
            )
            st.markdown(
                f"""
                <style>
                #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-bm2z3a.ea3mdgi8 > div.block-container.st-emotion-cache-1jicfl2.ea3mdgi5 > div > div > div > div:nth-child(6) > div > div > div.st-emotion-cache-ocqkz7.e1f1d6gn5 > div:nth-child(5) > div > div > div > div:nth-child(1) > div > label 
                {{
                    text-align: center;
                    margin: 0 auto; /* Centraliza horizontalmente */
                    display: table;
                }}
                </style>
                """,
                unsafe_allow_html=True
            )
            
            df_municipios_lavurs_inicio = df_original.assign(Municipio=df_original['Municipio'].str.split('; ')).explode('Municipio')
            df_regiao_muni_dict = load_df2('https://docs.google.com/spreadsheets/d/e/2PACX-1vQTq8R52z3oc9uW3FUsCjym25giwCvrPfcmLwWyc8ugt-c4g5uR-ZKUG3EOBdIP62sLnWSP68dnVkUw/pub?output=xlsx')
            df_regiao_muni_dict['Municipio'] = df_regiao_muni_dict['Municipio'].apply(lambda x: remover_acentos(x))
            df_regiao_muni_dict['Municipio'] = df_regiao_muni_dict['Municipio'].apply(lambda x: x.strip().upper())
            df_municipios_lavurs_inicio['Municipio'] = df_municipios_lavurs_inicio['Municipio'].apply(lambda x: remover_acentos(x))
            df_municipios_lavurs_inicio['Municipio'] = df_municipios_lavurs_inicio['Municipio'].apply(lambda x: x.strip().upper())
            # Verificação da correspondência
            municipios_nao_encontrados = df_municipios_lavurs_inicio[~df_municipios_lavurs_inicio['Municipio'].isin(df_regiao_muni_dict['Municipio'])]
            for mun in municipios_nao_encontrados['Municipio'].unique():
                df_municipios_lavurs_inicio = df_municipios_lavurs_inicio[df_municipios_lavurs_inicio['Municipio'] != mun]
            df_regiao_muni_dict = df_regiao_muni_dict.set_index('Municipio')
            dicionario_regiao_muni = df_regiao_muni_dict.to_dict()['Regiao_BHRS']
            df_municipios_lavurs_inicio['Regiao_BHRS'] = df_municipios_lavurs_inicio['Municipio'].map(dicionario_regiao_muni)
            df_regioes_lavurs_inicio_mapeado = df_municipios_lavurs_inicio.dropna(how='any').reset_index(drop=True)
            if decada != "Todas as décadas":
                df_regioes_lavurs_inicio_mapeado = df_regioes_lavurs_inicio_mapeado[df_regioes_lavurs_inicio_mapeado['Década'] == decada]
            if ano != "Todos os anos":
                df_regioes_lavurs_inicio_mapeado = df_regioes_lavurs_inicio_mapeado[df_regioes_lavurs_inicio_mapeado['Ano'] == ano]
            if regiao != "Todas as regiões":
                df_regioes_lavurs_inicio_mapeado = df_regioes_lavurs_inicio_mapeado[df_regioes_lavurs_inicio_mapeado['Regiao_BHRS']==regiao]
            municipios = sorted(df_regioes_lavurs_inicio_mapeado['Municipio'].str.split('; ').explode().unique())
            municipios.insert(0, 'Todos os municípios')
                
        with coluna4:
                   
            municipio_filtro = st.selectbox("SELECIONE O MUNICÍPIO DA BHRS", municipios, index=0, format_func=lambda x: x)
            st.markdown(
                f"""
                <style>
                #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-bm2z3a.ea3mdgi8 > div.block-container.st-emotion-cache-1jicfl2.ea3mdgi5 > div > div > div > div:nth-child(6) > div > div > div.st-emotion-cache-ocqkz7.e1f1d6gn5 > div:nth-child(7) > div > div > div > div:nth-child(1) > div
                {{                
                    box-shadow: 0px 0px 5px 5px rgba(0, 0, 0, 0.25);
                    border: 2px solid green;
                    border-radius: 15px;
                    padding: 10px;
                }}
                </style>
                """,
                unsafe_allow_html=True
            )
            st.markdown(
                """
                <style>
                #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-bm2z3a.ea3mdgi8 > div.block-container.st-emotion-cache-1jicfl2.ea3mdgi5 > div > div > div > div:nth-child(6) > div > div > div.st-emotion-cache-ocqkz7.e1f1d6gn5 > div:nth-child(7) > div > div > div > div:nth-child(1) > div > div > div
                {
                    background-color: #e0ffe0; /* Verde bem clarinho */
                    border: 1px solid lightgreen; /* Borda verde */
                    border-radius: 8px;
                    padding: 0px;
                    max-width: calc(100%);
                }
                </style>
                """,
                unsafe_allow_html=True
            )
            st.markdown(
                f"""
                <style>
                #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-bm2z3a.ea3mdgi8 > div.block-container.st-emotion-cache-1jicfl2.ea3mdgi5 > div > div > div > div:nth-child(6) > div > div > div.st-emotion-cache-ocqkz7.e1f1d6gn5 > div:nth-child(7) > div > div > div > div:nth-child(1) > div > label 
                {{
                    text-align: center;
                    margin: 0 auto; /* Centraliza horizontalmente */
                    display: table;
                }}
                </style>
                """,
                unsafe_allow_html=True
            )
            
            df_eventos_lavurs = df_regioes_lavurs_inicio_mapeado.assign(Evento=df_regioes_lavurs_inicio_mapeado['Evento'].str.split('; ')).explode('Evento')
            #df_eventos_lavurs_dropado = df_eventos_lavurs.drop_duplicates(['Data_Evento'])
            if decada != "Todas as décadas":
                df_eventos_lavurs = df_eventos_lavurs[df_eventos_lavurs['Década'] == decada]
            if ano != "Todos os anos":
                df_eventos_lavurs = df_eventos_lavurs[df_eventos_lavurs['Ano'] == ano]
            if regiao != "Todas as regiões":
                df_eventos_lavurs = df_eventos_lavurs[df_eventos_lavurs['Regiao_BHRS']==regiao]
            if municipio_filtro != "Todos os municípios":
                df_eventos_lavurs = df_eventos_lavurs[df_eventos_lavurs['Municipio']==municipio_filtro]
            eventos = sorted(df_eventos_lavurs['Evento'].str.split('; ').explode().unique())
            eventos.insert(0, 'Todos os tipos de evento')
        with coluna5:
            #lista_evento_todas_filtro = list(eventos_unicos)
            #lista_evento_todas_filtro.insert(0,'Todos os tipos de evento')       
            evento_tipo_filtro = st.selectbox("SELECIONE A TIPOLOGIA DO EVENTO", eventos, index=0, format_func=lambda x: x)
            st.markdown(
                f"""
                <style>
                #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-bm2z3a.ea3mdgi8 > div.block-container.st-emotion-cache-1jicfl2.ea3mdgi5 > div > div > div > div:nth-child(6) > div > div > div.st-emotion-cache-ocqkz7.e1f1d6gn5 > div:nth-child(9) > div > div > div > div:nth-child(1) > div
                {{                
                    box-shadow: 0px 0px 5px 5px rgba(0, 0, 0, 0.25);
                    border: 2px solid green;
                    border-radius: 15px;
                    padding: 10px;
                }}
                </style>
                """,
                unsafe_allow_html=True
            )
            st.markdown(
                """
                <style>
                #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-bm2z3a.ea3mdgi8 > div.block-container.st-emotion-cache-1jicfl2.ea3mdgi5 > div > div > div > div:nth-child(6) > div > div > div.st-emotion-cache-ocqkz7.e1f1d6gn5 > div:nth-child(9) > div > div > div > div:nth-child(1) > div > div > div
                {
                    background-color: #e0ffe0; /* Verde bem clarinho */
                    border: 1px solid lightgreen; /* Borda verde */
                    border-radius: 8px;
                    padding: 0px;
                    max-width: calc(100%);
                }
                </style>
                """,
                unsafe_allow_html=True
            )
            st.markdown(
                f"""
                <style>
                #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-bm2z3a.ea3mdgi8 > div.block-container.st-emotion-cache-1jicfl2.ea3mdgi5 > div > div > div > div:nth-child(6) > div > div > div.st-emotion-cache-ocqkz7.e1f1d6gn5 > div:nth-child(9) > div > div > div > div:nth-child(1) > div > label 
                {{
                    text-align: center;
                    margin: 0 auto; /* Centraliza horizontalmente */
                    display: table;
                }}
                </style>
                """,
                unsafe_allow_html=True
            )

    df_filtrado = df_eventos_lavurs.copy()
    for coluna in df_filtrado.columns:
        df_filtrado[coluna] = df_filtrado[coluna].astype(str).str.strip()
    
    if decada != "Todas as décadas":
        df_filtrado = df_filtrado[df_filtrado['Década'] == str(decada)]
    
    if ano != "Todos os anos":
        df_filtrado = df_filtrado[df_filtrado['Ano'] == str(ano)]
    
    if regiao != "Todas as regiões":
        df_filtrado = df_filtrado[df_filtrado['Regiao_BHRS']==regiao]
    
    if municipio_filtro != "Todos os municípios":
        df_filtrado = df_filtrado[df_filtrado['Municipio']==municipio_filtro]
    
    if evento_tipo_filtro != "Todos os tipos de evento":
        df_filtrado = df_filtrado[df_filtrado['Evento']==evento_tipo_filtro]
    
    
    df_fonte_explodido = df_filtrado.assign(Fonte=df_filtrado['Fonte'].str.split('; ')).explode('Fonte')
    dicionario_fonte = {
                        'Panorama': 'Jornal Panorama',
                        'G1': 'Site',
                        'DECRETO':'Decreto',
                        'Site de Prefeitura': 'Site',
                        'ZH': 'Jornal ZH'
                        }
    df_fonte_explodido['Fonte'] = df_fonte_explodido['Fonte'].replace(dicionario_fonte)
    df_fonte_explodido['Quantidade_Reportagens'] = pd.to_numeric(df_fonte_explodido['Quantidade_Reportagens'], errors='coerce')
    total_reportagens = df_fonte_explodido.drop_duplicates(['Data_Evento'])['Quantidade_Reportagens'].sum()
    total_fontes_jornalisticas = len(df_fonte_explodido['Fonte'].unique())
    total_de_eventos_registrados = len(df_filtrado['Data_Evento'].unique())
    total_eventos_unicos_tipo = len(df_filtrado['Evento'].unique())
    municipios_total_atingidos = len(df_filtrado['Municipio'].unique())
    
    container_cards = st.container()
    col6,col6_5, col7,col7_5,col8,col9_5,col9,col9_5,col10 = st.columns([1,0.1,1,0.1,1,0.1,1,0.1,1])
    with container_cards:
        
        with col6:
            st.markdown(
                        """
                        <div style='border: 2px solid green; border-radius: 20px; padding: 10px; box-shadow: 0px 0px 5px 5px rgba(0, 0, 0, 0.25); text-align: center; background-color: #c8e6c9;'>
                            <h10 style='font-size: 13px;'>REPORTAGENS COLETADAS</h10>
                            <p style='font-size: 26px; margin: 0; font-weight: bold;'>{}</p>
                        </div>
                        """.format(total_reportagens),
                        unsafe_allow_html=True
            )
        with col7:
            st.markdown(
                        """
                        <div style='border: 2px solid green; border-radius: 20px; padding: 10px; box-shadow: 0px 0px 5px 5px rgba(0, 0, 0, 0.25); text-align: center; background-color: #c8e6c9;'>
                            <h10 style='font-size: 13px;'>NÚMERO DE FONTES</h10>
                            <p style='font-size: 26px; margin: 0; font-weight: bold;'>{}</p>
                        </div>
                        """.format(total_fontes_jornalisticas),
                        unsafe_allow_html=True
            )
    
        with col8:
            st.markdown(
                        """
                        <div style='border: 2px solid green; border-radius: 20px; padding: 10px; box-shadow: 0px 0px 5px 5px rgba(0, 0, 0, 0.25); text-align: center; background-color: #c8e6c9;'>
                            <h10 style='font-size: 13px;'>EVENTOS REGISTRADOS</h10>
                            <p style='font-size: 26px; margin: 0; font-weight: bold;'>{}</p>
                        </div>
                        """.format(total_de_eventos_registrados),
                        unsafe_allow_html=True
            )
         
        with col9:
            st.markdown(
                        """
                        <div style='border: 2px solid green; border-radius: 20px; padding: 10px; box-shadow: 0px 0px 5px 5px rgba(0, 0, 0, 0.25); text-align: center; background-color: #c8e6c9;'>
                            <h10 style='font-size: 13px;'>TIPOS DE EVENTO REGISTRADOS</h10>
                            <p style='font-size: 26px; margin: 0; font-weight: bold;'>{}</p>
                        </div>
                        """.format(total_eventos_unicos_tipo),
                        unsafe_allow_html=True
            )
    
        with col10:
            st.markdown(
                        """
                        <div style='border: 2px solid green; border-radius: 20px; padding: 10px; box-shadow: 0px 0px 5px 5px rgba(0, 0, 0, 0.25); text-align: center; background-color: #c8e6c9;'>
                            <h10 style='font-size: 13px;'>MUNICÍPIOS COM EVENTO</h10>
                            <p style='font-size: 26px; margin: 0; font-weight: bold;'>{}</p>
                        </div>
                        """.format(municipios_total_atingidos),
                        unsafe_allow_html=True
            )
    
    
    container2 = st.container()
    with container2:
        st.write('<div style="margin-top: 10px;">', unsafe_allow_html=True)
        st.write('</div>', unsafe_allow_html=True)
        col4, col5 = st.columns([1.22, 1])
        with col4:
            df_municipios_lavurs_advindo_origem = df_filtrado.copy()
            df_municipios_lavurs_advindo_origem = df_municipios_lavurs_advindo_origem.drop_duplicates(['Data_Evento','Municipio'])
            if df_municipios_lavurs_advindo_origem.shape[0] > 0:
                df_municipios_lavurs = pd.crosstab(df_municipios_lavurs_advindo_origem['Municipio'], columns='count').reset_index()
            #df_municipios_lavurs = df_municipios_lavurs.assign(Municipio=df_municipios_lavurs['Municipio'].str.split('; ')).explode('Municipio')
                df_municipios_lavurs.reset_index(drop=True, inplace=True)
    
                df_municipios_lavurs['Municipio'] = df_municipios_lavurs['Municipio'].astype(str).apply(lambda x: remover_acentos(x))
            #df_municipios_lavurs_final_setado = df_municipios_lavurs.set_index('Municipio')
            #df_municipios_lavurs_final_setado = df_municipios_lavurs_final_setado.reset_index()
                df_municipios_lavurs_final_setado = pd.merge(df_municipios_lavurs, df_lista_municipios_bacia, on='Municipio', how='inner')
    
                municipios = load_geodata('https://raw.githubusercontent.com/andrejarenkow/geodata/main/municipios_rs_CRS/RS_Municipios_2021.json')
                municipios["IBGE6"] = municipios["CD_MUN"].str.slice(0,6)
                municipios['NOME_MUNICIPIO'] = municipios['NM_MUN']
                municipios['NOME_MUNICIPIO'] = municipios['NOME_MUNICIPIO'].astype(str).apply(lambda x: remover_acentos(x.strip()))
                municipios['NOME_MUNICIPIO'] = municipios['NOME_MUNICIPIO'].apply(lambda x: x.upper().strip())
                municipios = municipios.rename(columns={'NOME_MUNICIPIO':'Municipio'})
                dados_mapa_final = pd.merge(municipios, df_municipios_lavurs_final_setado, on='Municipio', how='left')
                dados_mapa_final['count'] = dados_mapa_final['count'].fillna(0)
            else:
                df_municipios_lavurs_advindo_origem['count'] = 1
                df_municipios_lavurs = df_municipios_lavurs_advindo_origem[['Municipio','count']]
            #df_municipios_lavurs = df_municipios_lavurs.assign(Municipio=df_municipios_lavurs['Municipio'].str.split('; ')).explode('Municipio')
                df_municipios_lavurs.reset_index(drop=True, inplace=True)
    
                df_municipios_lavurs['Municipio'] = df_municipios_lavurs['Municipio'].astype(str).apply(lambda x: remover_acentos(x))
            #df_municipios_lavurs_final_setado = df_municipios_lavurs.set_index('Municipio')
            #df_municipios_lavurs_final_setado = df_municipios_lavurs_final_setado.reset_index()
                df_municipios_lavurs_final_setado = pd.merge(df_municipios_lavurs, df_lista_municipios_bacia, on='Municipio', how='inner')
    
                municipios = load_geodata('https://raw.githubusercontent.com/andrejarenkow/geodata/main/municipios_rs_CRS/RS_Municipios_2021.json')
                municipios["IBGE6"] = municipios["CD_MUN"].str.slice(0,6)
                municipios['NOME_MUNICIPIO'] = municipios['NM_MUN']
                municipios['NOME_MUNICIPIO'] = municipios['NOME_MUNICIPIO'].astype(str).apply(lambda x: remover_acentos(x.strip()))
                municipios['NOME_MUNICIPIO'] = municipios['NOME_MUNICIPIO'].apply(lambda x: x.upper().strip())
                municipios = municipios.rename(columns={'NOME_MUNICIPIO':'Municipio'})
                dados_mapa_final = pd.merge(municipios, df_municipios_lavurs_final_setado, on='Municipio', how='left')
                try:
                    dados_mapa_final['count'] = dados_mapa_final['count'].fillna(0)
                except:
                    pass
            dados_mapa_final['IBGE6'] = dados_mapa_final['IBGE6'].astype(str)
            #dados_mapa_final['geometry2'] = dados_mapa_final['geometry'].apply(lambda x: x.__geo_interface__)
            #dados_mapa_final = dados_mapa_final.set_index('IBGE6')
            dados_mapa_final = dados_mapa_final.reset_index(drop=True)
            dados_mapa_final = dados_mapa_final.rename(columns={'count':'Nº de Eventos'})
    
            latitude_maxima = dados_mapa_final[dados_mapa_final['Nº de Eventos']!=0].geometry.centroid.y.max()
            longitude_maxima = dados_mapa_final[dados_mapa_final['Nº de Eventos']!=0].geometry.centroid.x.max()
            latitude_minima = dados_mapa_final[dados_mapa_final['Nº de Eventos']!=0].geometry.centroid.y.min()
            longitude_minima = dados_mapa_final[dados_mapa_final['Nº de Eventos']!=0].geometry.centroid.x.min()
            lati = (latitude_minima+latitude_maxima)/2
            long = (longitude_minima+longitude_maxima)/2
    
            df_bacia_hidrografica_rio_sinos = pd.merge(municipios,df_lista_municipios_bacia,on='Municipio',how='inner')
    
            # Definindo os valores e cores intermediárias
            max_events = dados_mapa_final['Nº de Eventos'].max()
            colorscale_custom = [
            [0, 'rgba(255,255,255,0.7)'],  # Branco para 0
            [0.2, 'rgba(100,150,0,0.7)'],  # Verde claro
            [0.6, 'rgba(180,100,0,0.7)'],  # Verde escuro
            [1, 'rgba(255,0,0,0.7)']]  # Vermelho
                
            if max_events <5:
                colorscale_custom = [
                    [0, 'rgba(255,255,255,0.7)'],  # Branco para 0
                    [0.5, 'rgba(50,255,0,0.7)'],
                    [1, 'rgba(100,220,0,0.7)'], # Verde claro (ou a cor que você preferir para um único evento)
                ]
            if max_events <10 and max_events>=5:
            # Se há apenas um evento, definimos uma escala de cores que contemple somente essa situação
                colorscale_custom = [
                    [0, 'rgba(255,255,255,0.7)'],  # Branco para 0
                    [0.5, 'rgba(100,220,0,0.7)'], # Verde claro (ou a cor que você preferir para um único evento)
                      [1, 'rgba(180,100,0,0.7)'],  # Verde escuro  
                    ]
            token = 'pk.eyJ1IjoiYW5kcmUtamFyZW5rb3ciLCJhIjoiY2xkdzZ2eDdxMDRmMzN1bnV6MnlpNnNweSJ9.4_9fi6bcTxgy5mGaTmE4Pw'
            px.set_mapbox_access_token(token)
            # Criando a paleta de cores personalizada
            map_fig = px.choropleth_mapbox(dados_mapa_final, geojson=dados_mapa_final.geometry,
                                           locations=dados_mapa_final.index, color='Nº de Eventos',
                                           color_continuous_scale=colorscale_custom,
                                           center ={'lat':lati, 'lon':long},
                                           zoom=7.6,
                                           mapbox_style="stamen-watercolor",
                                           hover_name='Municipio',
                                           width=800,
                                           height=680,
                                           template='plotly_dark',)
                                           
            map_fig.update_traces(marker_line_width=0.5)
    
            map_fig.update_layout(title={
                            'text': '<b><i>Mapa de Calor: Quantidade de Eventos Extremos por Município da BHRS</i></b>',
                            'y':1,
                            'x':0.5,
                            'xanchor': 'center',
                            'yanchor': 'top',
                            'font': {'family': 'Arial', 'size': 20}
                        }, margin=dict(l=100, # margem esquerda
                                       r=0, # margem direita
                                       t=50, # margem superior
                                       b=0  # margem inferior
                                    ))
    
            bacia_hidrografica = df_bacia_hidrografica_rio_sinos['geometry'].unary_union
    
            if isinstance(bacia_hidrografica, MultiPolygon):
                exterior = bacia_hidrografica.exterior
                lon_list = list(exterior.xy[0])
                lat_list = list(exterior.xy[1])
            else:
                lon_list = list(bacia_hidrografica.exterior.xy[0])
                lat_list = list(bacia_hidrografica.exterior.xy[1])
            
    
            map_fig.add_trace(go.Scattermapbox(
                mode="lines",
                lon=lon_list + [lon_list[0]],  # Adicionando o primeiro ponto no final para fechar o polígono
                lat=lat_list + [lat_list[0]],  # Adicionando o primeiro ponto no final para fechar o polígono
                marker={'color': 'black'},  # Cor da linha do contorno
                line=dict(width=3),  # Espessura da linha externa da bacia hidrográfica
                opacity=1,
                name='',
                hoverinfo='none'
            ))
            map_fig.update_coloraxes(colorbar=dict(
                                     orientation='h',
                                     thickness=28.5,
                                     title="Nº de Eventos",
                                     yanchor='bottom',  # Ancorar na parte inferior da barra de cores
                                     y=-0.3, # Posicionar abaixo da barra de cores
                                     x=0.52,
                                     tickfont={'color':'black',},
                                     len=1/1.2,
                                     lenmode='fraction',
                                     title_side='bottom',
                                     title_font_color='#000000',
                                     ticks='inside',  # Coloque os ticks dentro da barra de cores
                                     ticklen=5,  # Comprimento dos ticks
                                     tickwidth=0.5,  # Espessura dos ticks
                                     tickcolor='black',  # Cor dos ticks
            ))       
            map_fig
            st.markdown(
            """
            <style>
                #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-bm2z3a.ea3mdgi8 > div.block-container.st-emotion-cache-1jicfl2.ea3mdgi5 > div > div > div > div:nth-child(8) > div > div > div.st-emotion-cache-ocqkz7.e1f1d6gn5 > div.st-emotion-cache-xchpfm.e1f1d6gn3
                {
                box-shadow: 0px 0px 5px 5px rgba(0, 0, 0, 0.25);
                border: 2px solid green;
                border-radius: 15px;
                overflow: hidden;
                padding: 15px;
                max-width: 100%;
            }
            </style>
            """,
            unsafe_allow_html=True
            )
    
        with col5:
            df_heatmap_filtrado = df_filtrado.copy()
            df_heatmap_filtrado = df_heatmap_filtrado.drop_duplicates(['Data_Evento','Regiao_BHRS','Evento'])
            # Criar dummies para Região
            df_heatmap_filtrado['Regiao_BHRS'] = df_heatmap_filtrado['Regiao_BHRS'].apply(lambda x: x.replace(" E ", "; ") if " E " in x else x)
            dummies_regiao = df_heatmap_filtrado['Regiao_BHRS'].str.get_dummies('; ').reindex(columns=['ALTO SINOS', 'MEDIO SINOS', 'BAIXO SINOS'], fill_value=0)
            
            # Criar dummies para Evento
            #eventos_unicos = df_original['Evento'].str.split('; ').explode().str.upper().unique()
            dummies_eventos = df_heatmap_filtrado['Evento'].str.get_dummies('; ').reindex(columns=eventos_unicos, fill_value=0)
    
            # Juntar os dummies de região e eventos com o dataframe original
            df = pd.concat([df_heatmap_filtrado, dummies_regiao, dummies_eventos], axis=1)
    
            # Agrupar os dados por tipo de evento e somar para obter a contagem por região
            heatmap_data = df.groupby('Evento')[['ALTO SINOS','MEDIO SINOS', 'BAIXO SINOS']].sum().reset_index()
    
            heatmap_data_expanded = heatmap_data.assign(Evento=heatmap_data['Evento'].str.split('; ')).explode('Evento')
            # Resetar o índice
            heatmap_data_expanded.reset_index(drop=True, inplace=True)
    
            # Agrupar os dados novamente e somar para obter a contagem por região
            heatmap_data_final = heatmap_data_expanded.groupby(['Evento'])[['ALTO SINOS', 'MEDIO SINOS', 'BAIXO SINOS',]].sum().reset_index()
    
            # Se necessário, você pode ordenar os eventos
            heatmap_data_final = heatmap_data_final.sort_values(by='Evento')
    
            total_alto_sinos = int(heatmap_data_final['ALTO SINOS'].sum())
            total_medio_sinos = int(heatmap_data_final['MEDIO SINOS'].sum())
            total_baixo_sinos = int(heatmap_data_final['BAIXO SINOS'].sum())
    
            heatmap_data_final_setado = heatmap_data_final.set_index('Evento')
            lista_total_regioes = []
            lista_total_regioes.append([total_alto_sinos,total_medio_sinos,total_baixo_sinos])
            heatmap_data_final_setado = pd.concat([heatmap_data_final_setado,pd.DataFrame(lista_total_regioes).rename(columns={0:'ALTO SINOS',1:'MEDIO SINOS',2:'BAIXO SINOS'})])
            heatmap_data_final_setado = heatmap_data_final_setado.rename(index={0: 'TOTAL DE EVENTOS'})
            
            fig, ax = plt.subplots(figsize=(13.1, 13.6))

            
            heatmap_data = heatmap_data_final_setado#.drop('TOTAL DE EVENTOS')
    
            cmap = sns.cubehelix_palette(start=2, rot=0, dark=0, light=.95, reverse=False, as_cmap=True)
            sns.heatmap(data=heatmap_data, cmap=cmap, annot=True, fmt='d', linewidths=0.9, annot_kws={"size": 17}, cbar_kws={"orientation": "horizontal", "label": "N° de Eventos", "pad": 0.08})
            
            plt.axhline(y=-0.5, color='black', linestyle='-', linewidth=1)
    
            # Adicionando o total de eventos como uma anotação no gráfico
            total_eventos = heatmap_data_final_setado.loc['TOTAL DE EVENTOS']
    
            cbar = ax.collections[0].colorbar
            cbar.ax.tick_params(labelsize=14)
            valor_maximo_heatmap = heatmap_data.values.max()
            #cbar.set_ticks(np.arange(0,valor_maximo_heatmap  + 1, 5))
            cbar.ax.xaxis.label.set_size(16)
            plt.xticks(fontsize=12)
            plt.yticks(fontsize=12) 
    
            plt.title('TABELA HEATMAP: CONTAGEM DE EVENTOS POR REGIÃO E TIPOLOGIA', fontsize=21, pad=20,fontweight='bold', fontstyle='italic', fontname='Arial')
            ax.set_xlabel('')
            ax.set_ylabel('')
            plt.tight_layout()
    
            # Mostrar o gráfico no Streamlit
            st.pyplot(fig)
            st.markdown(
            """
            <style>
            #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-bm2z3a.ea3mdgi8 > div.block-container.st-emotion-cache-1jicfl2.ea3mdgi5 > div > div > div > div:nth-child(8) > div > div > div.st-emotion-cache-ocqkz7.e1f1d6gn5 > div.st-emotion-cache-1488958.e1f1d6gn3
            {            
                box-shadow: 0px 0px 5px 5px rgba(0, 0, 0, 0.25);
                border: 2px solid green;
                border-radius: 15px;
                overflow: hidden;
                padding: 15px;
                max-width: 100%;
            }
            </style>
            """,
            unsafe_allow_html=True
            )
    
            
    container3 = st.container()
    with container3:
        df_eventos_lavurs_dropado = df_eventos_lavurs.copy()
        if regiao!='Todas as regiões' and municipio_filtro!="Todos os municípios" and evento_tipo_filtro!="Todos os tipos de evento":
            df_eventos_lavurs_dropado_filtrado = df_eventos_lavurs_dropado[(df_eventos_lavurs_dropado['Regiao_BHRS']==regiao)&(df_eventos_lavurs_dropado['Municipio']==municipio_filtro)&(df_eventos_lavurs_dropado['Evento']==evento_tipo_filtro)]
        elif regiao=='Todas as regiões' and municipio_filtro!="Todos os municípios" and evento_tipo_filtro!="Todos os tipos de evento":
            df_eventos_lavurs_dropado_filtrado = df_eventos_lavurs_dropado[(df_eventos_lavurs_dropado['Municipio']==municipio_filtro)&(df_eventos_lavurs_dropado['Evento']==evento_tipo_filtro)]
        elif regiao=='Todas as regiões' and municipio_filtro=="Todos os municípios" and evento_tipo_filtro!="Todos os tipos de evento":
            df_eventos_lavurs_dropado_filtrado = df_eventos_lavurs_dropado[(df_eventos_lavurs_dropado['Evento']==evento_tipo_filtro)]
        elif regiao!='Todas as regiões' and municipio_filtro=="Todos os municípios" and evento_tipo_filtro=="Todos os tipos de evento":
            df_eventos_lavurs_dropado_filtrado = df_eventos_lavurs_dropado[df_eventos_lavurs_dropado['Regiao_BHRS']==regiao]
        elif regiao!='Todas as regiões' and municipio_filtro!="Todos os municípios" and evento_tipo_filtro=="Todos os tipos de evento":
            df_eventos_lavurs_dropado_filtrado = df_eventos_lavurs_dropado[(df_eventos_lavurs_dropado['Regiao_BHRS']==regiao)&(df_eventos_lavurs_dropado['Municipio']==municipio_filtro)]
        else:
            df_eventos_lavurs_dropado_filtrado = df_eventos_lavurs_dropado.copy()
    
        contagem_por_ano = df_eventos_lavurs_dropado_filtrado.drop_duplicates(['Data_Evento','Ano'])['Ano'].value_counts().sort_index().reset_index()    
        contagem_por_ano = contagem_por_ano.rename(columns={'count':'Nº de Eventos'})
        media = contagem_por_ano['Nº de Eventos'].mean()
        media = round(media,0)
        i=contagem_por_ano['Ano'].astype(int).min()-1
        maximo_ano = contagem_por_ano['Ano'].astype(int).max()
        contagem_por_ano['Ano'] = contagem_por_ano['Ano'].astype(str)
        while i<=maximo_ano:
            i_str = str(i)
            if i_str not in contagem_por_ano['Ano'].unique():
                lista=[i_str]
                lista_2 = [0.0]
                lista_df_anos_0 = pd.DataFrame(lista).rename(columns={0:'Ano'})
                lista_df_anos_2 = pd.DataFrame(lista_2).rename(columns={0:'Nº de Eventos'})
                lista_merged = pd.concat([lista_df_anos_0,lista_df_anos_2], axis=1)
                contagem_por_ano = pd.concat([contagem_por_ano,lista_merged])            
            i=i+1    
        
        contagem_por_ano['Média de Eventos da Série Histórica'] = media
        contagem_por_ano['Nº de Eventos'] = round(contagem_por_ano['Nº de Eventos'].astype(float),0)
        title_properties = alt.TitleParams(
                                            text='Série Histórica: Quantidade de Eventos por Ano',
                                            fontWeight='bold',
                                            fontStyle='italic',
                                            font='Arial',
                                            fontSize=18,
                                            color='black',
                                            baseline='middle',
                                            orient='top',
                                            anchor='middle'
                                          )        
        # Função para desenhar o gráfico de linhas com Altair
        
        if decada != "Todas as décadas":
            chart = alt.Chart(contagem_por_ano).mark_point().encode(
                x=alt.X('Ano', scale=alt.Scale(nice=False)),  # Definindo o número de ticks como 10
                y='Nº de Eventos',
                color=alt.condition(
                    (alt.datum.Ano >= str(decada)) & (alt.datum.Ano <= str(int(decada)+9)), 
                    alt.value('#FF0000'),  # Se for da década desejada, use vermelho
                    alt.value('#008000')   # Senão, use verde
                ),
                tooltip=['Ano', 'Nº de Eventos', 'Média de Eventos da Série Histórica']
            ).properties(
                height=300,
                width=1500
            )
    
            # Adicionando linha para a média
            chart_with_markers = chart + alt.Chart(contagem_por_ano).mark_line(interpolate='cardinal').transform_filter(
                (alt.datum.Ano >= str(decada)) & (alt.datum.Ano <= str(int(decada)+9))
            ).encode(
                x=alt.X('Ano', scale=alt.Scale(nice=False)), # Definindo o número de ticks como 10
                y='Nº de Eventos',
                color=alt.value('#FF0000')  # Cor da linha vermelha
            )
    
            # Adicionando outra linha para a média
            chart_with_markers += alt.Chart(contagem_por_ano).mark_line(interpolate='cardinal').transform_filter(
                alt.datum.Ano <= str(decada)
            ).encode(
                x=alt.X('Ano', scale=alt.Scale(nice=False)), 
                y='Nº de Eventos',
                color=alt.value('#008000')  # Linha antes da década em verde
            )
    
            # Adicionando outra linha para a média
            chart_with_markers += alt.Chart(contagem_por_ano).mark_line(interpolate='cardinal').transform_filter(
                alt.datum.Ano >= str(int(decada)+9)
            ).encode(
                x=alt.X('Ano', scale=alt.Scale(nice=False)),  # Definindo o número de ticks como 10
                y='Nº de Eventos',
                color=alt.value('#008000')  # Linha após a década em verde
            )
    
            # Adicionando linha da média
            chart_with_markers += alt.Chart(contagem_por_ano).mark_line().encode(
                x=alt.X('Ano', scale=alt.Scale(nice=False)),  # Definindo o número de ticks como 10
                y=alt.Y('Média de Eventos da Série Histórica', title='Número de Eventos'),
                color=alt.value('#000000')  # Linha da média em preto
            )
    
            # Adicionando outra linha
            chart_with_markers += alt.Chart(contagem_por_ano).mark_line().encode(
                x=alt.X('Ano', scale=alt.Scale(nice=False)),  # Definindo o número de ticks como 10
                y=alt.Y('Média de Eventos da Série Histórica', title='Número de Eventos'),  # Adicionando rótulo ao eixo Y
                color=alt.value('#000000')  # Cor da linha em preto
            )
        
        else:
            chart = alt.Chart(contagem_por_ano).mark_point().encode(
            x=alt.X('Ano', scale=alt.Scale(nice=False)),
            y='Nº de Eventos',
            color=alt.value('#008000'),
            tooltip=['Ano', 'Nº de Eventos', 'Média de Eventos da Série Histórica']
            )
                                            
            # Adicionando os marcadores para a linha principal
            chart_with_markers = chart + alt.Chart(contagem_por_ano).mark_line(interpolate='cardinal').encode(
                x=alt.X('Ano', scale=alt.Scale(nice=False)),
                y='Nº de Eventos',
                color=alt.value('#008000')  # Cor da linha vermelha
            )
            # Adicionando outra linha para a média
            chart_with_markers += alt.Chart(contagem_por_ano).mark_line().encode(
                x=alt.X('Ano', scale=alt.Scale(nice=False)),
                y=alt.Y('Média de Eventos da Série Histórica', title='Número de Eventos'),
                color=alt.value('#000000')  # Linha da média em preto
            )
            # Adicionando outra linha
            chart_with_markers += alt.Chart(contagem_por_ano).mark_line().encode(
            x=alt.X('Ano', scale=alt.Scale(nice=False)),
            y=alt.Y('Média de Eventos da Série Histórica', title='Número de Eventos'),  # Adicionando rótulo ao eixo Y em negrito
            color=alt.value('#000000'))    
    
        title_properties = alt.TitleParams(
            text='Série Histórica: Quantidade de Eventos por Ano',
            fontWeight='bold',
            fontStyle='italic',
            font='Arial',
            fontSize=18,
            color='black',
            baseline='middle',
            orient='top',
            anchor='middle'
        )

        # Configuração dos eixos
        layout_chart = chart_with_markers.configure_axisLeft(
            titleFontWeight='bold',
            titleFontSize=18,
            titleColor='black',
        ).configure_axisX(
            titleFontWeight='bold',
            titleFontSize=18,
            titleColor='black',
            labelFontSize=12,
        ).properties(height=450,width=1680)
        # Gráfico com título
        chart_with_title = layout_chart.properties(title=title_properties)
        st.altair_chart(chart_with_title)
        # Mostrando o gráfico no Streamlit
        st.markdown(
        """
        <style>
        #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-bm2z3a.ea3mdgi8 > div.block-container.st-emotion-cache-1jicfl2.ea3mdgi5 > div > div > div > div:nth-child(9) > div > div > div:nth-child(1) > div > div
        {    
            box-shadow: 0px 0px 5px 5px rgba(0, 0, 0, 0.25);
            border: 2px solid green;
            border-radius: 15px;
            padding: 15px;
            max-width: 100%-40px;
    
        }
        </style>
        """,
        unsafe_allow_html=True
        )
        
        container4 = st.container()
        col11,col12 = st.columns([1,1.2])    
        with container4:
            with col11:
                df_decadas = pd.DataFrame()
                df_decadas = df_eventos_lavurs_dropado_filtrado.drop_duplicates(['Data_Evento','Ano'])['Ano'].value_counts().sort_index().reset_index()    
                df_decadas = df_decadas.rename(columns={'count':'Nº de Eventos'})
                df_decadas['Ano'] = df_decadas['Ano'].astype(int).astype(float)
                df_decadas['Década'] = (df_decadas['Ano'] // 10) * 10
                df_decadas['Década'] = df_decadas['Década'].astype(int).astype(str)
                contagem_por_decada = df_decadas.groupby('Década')['Nº de Eventos'].sum().reset_index()
    
                sns.set_style("white")
                
                # Criando o gráfico de barras
                fig_2 = plt.figure(figsize=(12, 6.5))
    
                # Plotando o gráfico de barras
                ax =sns.barplot(data=contagem_por_decada, x="Década", y="Nº de Eventos", color="#009000")
                sns.despine()
                # Personalizando os valores do eixo X
                plt.xticks(fontsize=12, fontweight='bold')  # Define o tamanho e o peso da fonte dos rótulos do eixo X
            
                plt.yticks([])
    
                # Adicionando título e rótulos dos eixos
                plt.title('SÉRIE HISTÓRICA: NÚMERO DE EVENTOS POR DÉCADA', fontsize=20, fontstyle='italic', fontweight='bold', fontname='Arial')
                plt.xlabel('Década', fontsize=16)
                plt.ylabel('Número de Eventos', fontsize=16)
                for i, p in enumerate(ax.patches):
                # Obtendo a década correspondente ao índice da barra
                    decada_x = contagem_por_decada.loc[i, 'Década']
                    if decada == decada_x:
                        p.set_color('red')  # Se for a década selecionada, cor da barra vermelha
                    else:
                        p.set_color('green')  # Se não for a década selecionada, cor da barra em cinza claro
    
                    ax.annotate(format(p.get_height(), '.0f'), 
                                (p.get_x() + p.get_width() / 2., p.get_height()), 
                                ha='center', va='center', 
                                xytext=(0, 5), 
                                textcoords='offset points',
                                fontsize=12,
                                fontweight='bold',
                                color='black'  # Cor do texto é preto
                                )
    
                st.pyplot(plt.gcf())
                st.markdown(
                """
                <style>
                #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-bm2z3a.ea3mdgi8 > div.block-container.st-emotion-cache-1jicfl2.ea3mdgi5 > div > div > div > div:nth-child(9) > div > div > div:nth-child(3) > div.st-emotion-cache-n4b52j.e1f1d6gn3 > div
                {
                    box-shadow: 0px 0px 5px 5px rgba(0, 0, 0, 0.25);
                    border: 2px solid green;
                    border-radius: 15px;
                    overflow: hidden;
                    padding: 15px;
                    max-width: 100%;
                }
    
                </style>
                """,
                unsafe_allow_html=True
                )
    
            with col12:
                df_fonte_explodido = df_filtrado.assign(Fonte=df_filtrado['Fonte'].str.split('; ')).explode('Fonte')
                df_fonte_explodido['Quantidade_Reportagens'] = df_fonte_explodido['Quantidade_Reportagens'].astype(int)
                dicionario_fonte = {
                    'Panorama': 'Jornal Panorama',
                    'G1': 'Site',
                    'DECRETO':'Decreto',
                    'Site de Prefeitura': 'Site',
                    'ZH': 'Jornal ZH',
                    'nan':'Sem Fonte',
                    np.nan:'Sem Fonte',
                    'JORNAL VS':'Jornal VS',
                }
                df_fonte_explodido['Fonte'] = df_fonte_explodido['Fonte'].replace(dicionario_fonte)
                df_fontesexplodido_lavurs_dropado_filtrado = df_fonte_explodido.copy()
                df_fontes = df_fontesexplodido_lavurs_dropado_filtrado.drop_duplicates('Data_Evento')  
                contagem_por_fonte = df_fontes.groupby('Fonte')['Quantidade_Reportagens'].sum().reset_index()
                #contagem_por_fonte = contagem_por_fonte.rename(columns={'Quantidade_Reportagens':'N° de Reportagens'})
                contagem_por_fonte = contagem_por_fonte.sort_values(by='Quantidade_Reportagens', ascending=False)
                
                # Criando o gráfico de barras
                barsh = plt.figure(figsize=(12, 6.5))
    
                # Plotando o gráfico de barras
                sns.set_style("whitegrid")
    
                # Plotando o gráfico de barras com Seaborn
                axbarsh = sns.barplot(x="Quantidade_Reportagens", y="Fonte", data=contagem_por_fonte, color="#009000", orient='h')
                sns.despine()
                for index, row in contagem_por_fonte.iterrows():
                    axbarsh.annotate(format(row["Quantidade_Reportagens"], '.0f'), 
                                    xy=(row["Quantidade_Reportagens"], row['Fonte']), 
                                    xytext=(5, 0),  # Deslocamento do texto
                                    textcoords="offset points",
                                    ha='left', va='center',  # Alinhamento horizontal e vertical
                                    fontsize=10, fontweight='bold', color='black')
    
                # Personalizando os valores do eixo X
                plt.yticks(fontsize=10, fontweight='bold')
                # Removendo o eixo y
                plt.xticks([])
    
                # Adicionando título e rótulos dos eixos
                plt.title('NÚMERO DE REPORTAGENS POR FONTE', fontsize=18, fontstyle='italic', fontweight='bold', fontname='Arial')
                plt.xlabel('Número de Reportagens', fontsize=14)
                plt.ylabel('Fonte', fontsize=14) 
    
                # Exibindo o gráfico
                st.pyplot(plt.gcf())
    
                # Criando a string HTML com o gráfico e a sombra
                st.markdown(
                """
                <style>
                #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-bm2z3a.ea3mdgi8 > div.block-container.st-emotion-cache-1jicfl2.ea3mdgi5 > div > div > div > div:nth-child(9) > div > div > div:nth-child(3) > div.st-emotion-cache-1wce3lb.e1f1d6gn3
                {                
                    box-shadow: 0px 0px 5px 5px rgba(0, 0, 0, 0.25);
                    border: 2px solid green;
                    border-radius: 15px;
                    overflow: hidden;
                    padding: 15px;
                    max-width: 100%;
                }
    
                </style>
                """,
                unsafe_allow_html=True
                )
        
        container5 = st.container()
        col13, col14 = st.columns([1,1])
        with container5:
                   
            with col13:
                df_filtrado_dropado_anomes = df_filtrado.copy()
                df_filtrado_dropado_anomes['Quantidade_Municipios'] = df_filtrado_dropado_anomes['Quantidade_Municipios'].astype(int)
                df_filtrado_dropado_anomes['Quantidade_Reportagens'] = df_filtrado_dropado_anomes['Quantidade_Reportagens'].astype(int)
                df_filtrado_dropado_anomes_muni = df_filtrado_dropado_anomes.groupby(['Ano','Mes'])['Municipio'].nunique().reset_index()
                df_filtrado_dropado_anomes_Reportagens = df_filtrado_dropado_anomes.drop_duplicates('Data_Evento')
                df_filtrado_dropado_anomes_Reportagens_crosstab = df_filtrado_dropado_anomes_Reportagens[['Ano','Mes',"Quantidade_Reportagens"]].groupby(['Ano','Mes'])['Quantidade_Reportagens'].sum().reset_index()
                df_filtrado_dropado_anomes_Reportagens_crosstab = df_filtrado_dropado_anomes_Reportagens_crosstab[['Ano', 'Mes','Quantidade_Reportagens']]
                df_filtrado_ano_mes_eventos = df_filtrado_dropado_anomes.drop_duplicates('Data_Evento')
                df_filtrado_ano_mes_eventos_crosstab = pd.crosstab(index=[df_filtrado_ano_mes_eventos['Ano'],df_filtrado_ano_mes_eventos['Mes']],columns='count').reset_index()
                df_filtrado_ano_mes_merged = pd.merge(df_filtrado_ano_mes_eventos_crosstab,df_filtrado_dropado_anomes_Reportagens_crosstab,on=['Ano','Mes'], how='outer')
                df_filtrado_ano_mes_merged = df_filtrado_ano_mes_merged.rename(columns={'count':'N° de Eventos', 'Quantidade_Reportagens':'N° de Reportagens'})
                df_filtrado_ano_mes_merged_final = pd.merge(df_filtrado_ano_mes_merged,df_filtrado_dropado_anomes_muni,on=['Ano', 'Mes'] , how='outer')
                df_filtrado_ano_mes_merged_final = df_filtrado_ano_mes_merged_final.rename(columns={'Municipio':'Quantidade_Municipios','Mes':'Mês'})
                df_filtrado_ano_mes_merged_final[r'% de Municípios Atingidos'] = round((df_filtrado_ano_mes_merged_final['Quantidade_Municipios']*100)/(31),2)
                tabela_ano_mes = df_filtrado_ano_mes_merged_final[['Ano', 'Mês', 'N° de Eventos', 'N° de Reportagens', r'% de Municípios Atingidos']]
                tabela_ano_mes = tabela_ano_mes.sort_values(by=['N° de Eventos','N° de Reportagens'], ascending=False)
                # Reiniciando o índice do DataFrame
                tabela_ano_mes = tabela_ano_mes.reset_index(drop=True)
                # Adicionando a coluna de ranking
                tabela_ano_mes['Ranking'] = tabela_ano_mes.index + 1
                # Definindo a coluna de ranking como o novo índice
                tabela_ano_mes.set_index('Ranking', inplace=True)
                #tabela_ano_mes = tabela_ano_mes.sort_values(by=r'% de Municípios Atingidos', ascending=False)
                tabela_anomes_stilished = tabela_ano_mes.style.background_gradient(cmap=cmap, subset=['N° de Eventos', 'N° de Reportagens'])
    
                st.dataframe(tabela_anomes_stilished, use_container_width =True,
                            column_config={r'% de Municípios Atingidos': st.column_config.ProgressColumn(
                                            r'% de Municípios Atingidos na BHRS',
                                            help="Porcentagem de Municípios Atingidos na BHRS em relação ao total de Municípios da BHRS",
                                            format="%f",
                                            min_value=0,
                                            max_value=100,),
                                            'N° Eventos': st.column_config.NumberColumn(
                                            'N° Eventos',
                                            format="%d"),
                                            "N° Reportagens": st.column_config.NumberColumn(
                                            "N° de Reportagens",
                                            format="%d")}
                                            )
                st.markdown(
                """
                <style>
                #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-bm2z3a.ea3mdgi8 > div.block-container.st-emotion-cache-1jicfl2.ea3mdgi5 > div > div > div > div:nth-child(9) > div > div > div:nth-child(4) > div:nth-child(1)
                {                
                    box-shadow: 0px 0px 5px 5px rgba(0, 0, 0, 0.25);
                    border: 2px solid green;
                    border-radius: 15px;
                    overflow: hidden;
                    padding: 15px;
                    max-width: 100%;
                }
    
                </style>
                """,
                unsafe_allow_html=True
                )
            with col14:
                df_filtrado_dropado_municipio_origem = df_filtrado.copy()
                df_filtrado_dropado_municipio_origem['Quantidade_Reportagens'] = df_filtrado_dropado_municipio_origem['Quantidade_Reportagens'].astype(int)
                df_filtrado_dropado_municipio_Reportagens = df_filtrado_dropado_municipio_origem.drop_duplicates(['Data_Evento','Municipio'])
                df_filtrado_dropado_municipio_Reportagens2 = df_filtrado_dropado_municipio_Reportagens[['Municipio',"Quantidade_Reportagens"]].groupby(['Municipio'])['Quantidade_Reportagens'].sum().reset_index()
                df_filtrado_municipio_eventos = df_filtrado_dropado_municipio_origem.drop_duplicates(['Data_Evento','Municipio'])
                df_filtrado_municipio_eventos_crosstab = pd.crosstab(index=df_filtrado_municipio_eventos['Municipio'],columns='count').reset_index()
                df_filtrado_municipio_merged = pd.merge(df_filtrado_municipio_eventos_crosstab, df_filtrado_dropado_municipio_Reportagens2, on='Municipio', how='outer')
                df_filtrado_municipio_merged_final = df_filtrado_municipio_merged.rename(columns={'count':'N° de Eventos', 'Quantidade_Reportagens':'N° de Reportagens'})
    
                tabela_municipio = df_filtrado_municipio_merged_final.sort_values(by='N° de Eventos', ascending=False)
                # Reiniciando o índice do DataFrame
                tabela_municipio = tabela_municipio.reset_index(drop=True)
                # Adicionando a coluna de ranking
                tabela_municipio['Ranking'] = tabela_municipio.index + 1
                # Definindo a coluna de ranking como o novo índice
                tabela_municipio.set_index('Ranking', inplace=True)
                tabela_municipio_stilished = tabela_municipio.style.background_gradient(cmap=cmap, subset=['N° de Eventos', 'N° de Reportagens'])
                st.dataframe(tabela_municipio_stilished, use_container_width =True,
                            column_config={'N° Eventos': st.column_config.NumberColumn(
                                            'N° Eventos',
                                            format="%d"),
                                            "N° Reportagens": st.column_config.NumberColumn(
                                            "N° de Reportagens",
                                            format="%d")}
                                            )
                st.markdown(
                """
                <style>
                #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-bm2z3a.ea3mdgi8 > div.block-container.st-emotion-cache-1jicfl2.ea3mdgi5 > div > div > div > div:nth-child(9) > div > div > div:nth-child(4) > div:nth-child(2) 
                {                
                    box-shadow: 0px 0px 5px 5px rgba(0, 0, 0, 0.25);
                    border: 2px solid green;
                    border-radius: 15px;
                    overflow: hidden;
                    padding: 15px;
                    max-width: 100%;
                }
                </style>
                """,
                unsafe_allow_html=True
                )
        col15, col16 = st.columns([2,1])
        container6 = st.container()
        with container6:
            with col15:
                df_meses = pd.DataFrame()
                df_meses = df_filtrado.drop_duplicates(['Data_Evento','Mes'])['Mes'].value_counts().sort_index().reset_index()    
                df_meses = df_meses.rename(columns={'count':'Nº de Eventos'})
                contagem_por_mes = df_meses.groupby('Mes')['Nº de Eventos'].sum().reset_index()
                meses_mapping = {
                    "JANEIRO": 1, "FEVEREIRO": 2, "MARÇO": 3, "ABRIL": 4,
                    "MAIO": 5, "JUNHO": 6, "JULHO": 7, "AGOSTO": 8,
                    "SETEMBRO": 9, "OUTUBRO": 10, "NOVEMBRO": 11, "DEZEMBRO": 12
                }
                
                # Adicionar uma coluna auxiliar para ordenar
                contagem_por_mes["Mes_num"] = contagem_por_mes["Mes"].map(meses_mapping)
                
                # Ordenar o DataFrame pelos valores numéricos dos meses
                contagem_por_mes_sorted = contagem_por_mes.sort_values("Mes_num").drop(columns="Mes_num")
                
                # Resetar o índice (opcional)
                contagem_por_mes_sorted = contagem_por_mes_sorted.reset_index(drop=True)
                contagem_por_mes_sorted['Mes'] = contagem_por_mes_sorted['Mes'].replace('NÃO IDENTIFICADO','N/I')
                sns.set_style("white")
                    
                # Criando o gráfico de barras
                fig_meses = plt.figure(figsize=(24, 7.5))
        
                # Plotando o gráfico de barras
                ax_meses =sns.barplot(data=contagem_por_mes_sorted, x="Mes", y="Nº de Eventos", color="#009000", width=0.5)
                sns.despine()
                # Personalizando os valores do eixo X
                plt.xticks(fontsize=12, fontweight='bold')  # Define o tamanho e o peso da fonte dos rótulos do eixo X
                
                plt.yticks([])
        
                # Adicionando título e rótulos dos eixos
                plt.title('SÉRIE HISTÓRICA: NÚMERO DE EVENTOS POR MÊS', fontsize=20, fontstyle='italic', fontweight='bold', fontname='Arial')
                plt.xlabel('Mês', fontsize=16)
                plt.ylabel('Número de Eventos', fontsize=16)
                for i, p in enumerate(ax_meses.patches):    
                    ax_meses.annotate(format(p.get_height(), '.0f'), 
                                (p.get_x() + p.get_width() / 2., p.get_height()), 
                                ha='center', va='center', 
                                xytext=(0, 5), 
                                textcoords='offset points',
                                fontsize=14,
                                fontweight='bold',
                                color='black')  # Cor do texto é preto
                                    
        
                st.pyplot(plt.gcf())
    
                st.markdown(
                """
                <style>
                #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-bm2z3a.ea3mdgi8 > div.block-container.st-emotion-cache-1jicfl2.ea3mdgi5 > div > div > div > div:nth-child(9) > div > div > div:nth-child(5) > div.st-emotion-cache-115gedg.e1f1d6gn3
                {                
                    box-shadow: 0px 0px 5px 5px rgba(0, 0, 0, 0.25);
                    border: 2px solid green;
                    border-radius: 15px;
                    overflow: hidden;
                    padding: 15px;
                    max-width: 100%;
                }
                </style>
                """,unsafe_allow_html=True)
        with col16:
            df_pizza = df_filtrado.copy()
            df_pizza['Quantidade_Reportagens'] = df_pizza['Quantidade_Reportagens'].astype(int)
            df_pizza2 = df_pizza.drop_duplicates(['Data_Evento','Regiao_BHRS'])
            df_pizza2 = df_pizza2[['Regiao_BHRS',"Quantidade_Reportagens"]].groupby(['Regiao_BHRS'])['Quantidade_Reportagens'].sum().reset_index()
            colors = ["#77dd77", "#ff6961", "#000000"]

            fig_pizza, ax_pizza = plt.subplots()    
                # Configurando o gráfico de rosca
            wedges, texts, autotexts = ax_pizza.pie(df_pizza2["Quantidade_Reportagens"], labels=df_pizza2["Regiao_BHRS"], colors=colors, startangle=90, 
                                                        counterclock=False, wedgeprops=dict(width=0.3), autopct='%1.1f%%')
            for autotext, color in zip(autotexts, colors):
                autotext.set_color('white')  # Definindo a cor do texto para branco
                autotext.set_backgroundcolor(color)
                autotext.set_alpha(0.85)  # Definindo a opacidade
                autotext.set_fontweight('bold')
                # Adicionando título
            plt.title("PORCENTAGEM DE REPORTAGENS POR REGIÃO DA BHRS",fontstyle='italic', fontweight='bold')
                
                # Exibindo o gráfico no Streamlit
            st.pyplot(fig_pizza)
            st.markdown(
                """
                <style>
                #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-bm2z3a.ea3mdgi8 > div.block-container.st-emotion-cache-1jicfl2.ea3mdgi5 > div > div > div > div:nth-child(9) > div > div > div:nth-child(5) > div.st-emotion-cache-1r6slb0.e1f1d6gn3
                {                
                    box-shadow: 0px 0px 5px 5px rgba(0, 0, 0, 0.25);
                    border: 2px solid green;
                    border-radius: 15px;
                    overflow: hidden;
                    padding: 15px;
                    max-width: 100%;
                }
                </style>
                """,unsafe_allow_html=True)
elif page=="Sobre o Painel":
    st.write('Em contrução')


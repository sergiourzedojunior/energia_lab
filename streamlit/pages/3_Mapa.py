import streamlit as st
import pandas as pd
import folium
from branca.colormap import linear
import streamlit_folium as st_folium  # Importação correta

# Load data paths
path = "D:\\OneDrive\\energia_lab\\data\\"
path1 = "D:\\OneDrive\\energia_lab\\streamlit\\data_steamlit\\" 


# Configuração da página Streamlit
st.set_page_config(layout="wide", page_title="Eficiência Energética Labdados")

# Interface principal do app
st.markdown("# Mapa de Eficiência Energética! ⚡")

# Carregar e limpar dados
@st.cache_data
def load_unidos_data():
    df = pd.read_csv(path+'df_unidos.csv')
    state_mapping = {
        "Espírito Santo": "ES", "São Paulo": "SP", "Paraná": "PR",
        "Bahia": "BA", "Rio Grande do Norte": "RN", "Pernambuco": "PE",
        "Mato Grosso": "MT", "Rio Grande do Sul": "RS"
    }
    df['Estado'] = df['Estado'].str.upper().replace({k.upper(): v for k, v in state_mapping.items()})
    df = df[df['Estado'].isin(state_mapping.values())]
    return df

df = load_unidos_data()

# Centroides dos estados brasileiros
state_centroids = {
    "ES": (-19.19, -40.34), "SP": (-23.55, -46.64), "PR": (-24.89, -51.55),
    "BA": (-12.96, -38.51), "RN": (-5.22, -36.52), "PE": (-8.28, -35.07),
    "MT": (-12.64, -55.42), "RS": (-30.01, -51.22)
}

# Agrupar por estado e calcular a soma dos scores
estado_scores = df.groupby('Estado')['Score'].sum().reset_index()

# Calcular score máximo e mínimo para escala de cores
max_score = estado_scores['Score'].max()
min_score = estado_scores['Score'].min()

# Ajustar o valor mínimo para a escala de cores
adjusted_min_score = min_score + (max_score - min_score) * .01

colormap = linear.Greens_09.scale(adjusted_min_score, max_score)

# Adicionar coordenadas dos centroides
estado_scores['Latitude'] = estado_scores['Estado'].map(lambda x: state_centroids[x][0])
estado_scores['Longitude'] = estado_scores['Estado'].map(lambda x: state_centroids[x][1])

# Criar mapa
mapa = folium.Map(location=[-14.2350, -51.9253], zoom_start=4)
for idx, row in estado_scores.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=20,  # Aumentar o tamanho do círculo
        popup=f"Estado: {row['Estado']}<br>Score: {row['Score']:.2f}",
        color=colormap(row['Score']),
        fill=True,
        fill_color=colormap(row['Score'])
    ).add_to(mapa)
    
    
# Adicionar legenda ao mapa
colormap.caption = 'Distribuição de Scores por Estado'
colormap.add_to(mapa)

# Integração do mapa no Streamlit usando streamlit_folium
st.markdown("## Mapa Interativo dos Scores por Estado")
st_folium.folium_static(mapa)  # Uso correto do módulo importado

st.markdown("---")  # Linha horizontal em markdown

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Cache do dataset 
@st.cache_data
def carregar_dados():
    return sns.load_dataset("penguins")

# Contador basico de visitas (mostrar SESSION_STATE)
if "visitas" not in st.session_state:
    st.session_state["visitas"] = 1
else:
    st.session_state["visitas"] += 1

# TITULO E INTRO
st.title("Streamlit App - Dataset de Pinguins")
st.header("Explorando os dados do dataset Penguins")
st.info(f"Você acessou essa página {st.session_state['visitas']} vezes.")

# LADO ESQUERDO - controles
st.sidebar.title("filtros")
mostrar_dados = st.sidebar.checkbox("Exibir tabela")

# carregar dados
dados = carregar_dados()

# filtro de especie
filtro_especie = st.sidebar.multiselect(
    "especie:", options=dados["species"].dropna().unique().tolist(),
    default=dados["species"].dropna().unique().tolist()
)

# filtro de sexo
sexo = st.sidebar.radio("sexo", ["Todos", "Male", "Female"], index=0)
if sexo != "Todos":
    dados = dados[dados["sex"] == sexo]

# filtro por massa
min_mass = int(dados["body_mass_g"].min())
max_mass = int(dados["body_mass_g"].max())
faixa_peso = st.sidebar.slider("peso do bicho (gramas)", min_mass, max_mass, (min_mass, max_mass))
dados = dados[dados["body_mass_g"].between(*faixa_peso)]

# filtro especie final
dados = dados[dados["species"].isin(filtro_especie)]

# mostra tabela
if mostrar_dados:
    st.subheader("dados brutos")
    st.dataframe(dados)

# grafico de histograma
st.subheader("Distribuição do Peso")
fig1, ax1 = plt.subplots()
sns.histplot(dados["body_mass_g"], kde=True, ax=ax1)
st.pyplot(fig1)

# boxplot por especie
st.subheader("Tamanho do bico por especie")
fig2, ax2 = plt.subplots()
sns.boxplot(data=dados, x="species", y="bill_length_mm", ax=ax2)
st.pyplot(fig2)

# escolha de colunas p scatter
st.subheader("correlações")
eixo_x = st.selectbox("coluna x", ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"])
eixo_y = st.selectbox("coluna y", ["body_mass_g", "flipper_length_mm", "bill_depth_mm", "bill_length_mm"])
fig3, ax3 = plt.subplots()
sns.scatterplot(data=dados, x=eixo_x, y=eixo_y, hue="species", ax=ax3)
st.pyplot(fig3)

# estatisticas
with st.expander("Estatísticas?"):
    st.write(dados.describe())

# resetar contador de visitas
if st.button("zerar contador"):
    st.session_state["visitas"] = 1
    st.success("Resetado com sucesso")
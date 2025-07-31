import streamlit as st
import random

st.set_page_config(layout="wide")
st.title("Simulador de Combate - Kill Team 3")

# --- Inicialización del estado ---
if "vidas" not in st.session_state:
    st.session_state.vidas = {"atacante": 12, "defensor": 12}
if "dados_atacante" not in st.session_state:
    st.session_state.dados_atacante = []
if "dados_defensor" not in st.session_state:
    st.session_state.dados_defensor = []
if "interacciones" not in st.session_state:
    st.session_state.interacciones = []

# --- Inputs para Atacante y Defensor ---
col1, col2 = st.columns(2)
with col1:
    st.markdown("### Atacante")
    exito_norm_atac = st.number_input("Éxitos normales", 0, 6, 2, key="exitos_norm_atac")
    critico_atac = st.number_input("Críticos", 0, 6, 1, key="critico_atac")
    dmg_norm_atac = st.number_input("Daño normal", 1, 10, 3)
    dmg_crit_atac = st.number_input("Daño crítico", 1, 12, 5)
    vida_atac = st.number_input("Vida", 1, 30, max(st.session_state.vidas["atacante"], 1), key="vida_atac")
    st.session_state.vidas["atacante"] = vida_atac

with col2:
    st.markdown("### Defensor")
    exito_norm_def = st.number_input("Éxitos normales", 0, 6, 2, key="exitos_norm_def")
    critico_def = st.number_input("Críticos", 0, 6, 1, key="critico_def")
    dmg_norm_def = st.number_input("Daño normal", 1, 10, 2)
    dmg_crit_def = st.number_input("Daño crítico", 1, 12, 4)
    vida_def = st.number_input("Vida", 1, 30, max(st.session_state.vidas["defensor"], 1), key="vida_def")
    st.session_state.vidas["defensor"] = vida_def

# --- Generar dados según input ---
def generar_dados(num_normales, num_criticos):
    return ["✔️"] * num_normales + ["💥"] * num_criticos

# --- Mostrar dados e interacciones ---
def mostrar_dados(dados_atac, dados_def, jugador):
    st.markdown("#### Resultado de los dados")
    col_atac, col_def = st.columns(2)

    def render_dados(label, dados, enemigo, enemigo_key):
        cols = st.columns(len(dados) + 1)
        cols[0].markdown(f"**{label}**\n\n❤️ {st.session_state.vidas[label.lower()]}")
        for i, d in enumerate(dados):
            disabled = (label, i) in st.session_state.interacciones
            if cols[i + 1].button(d, key=f"{label}_{i}", disabled=disabled):
                st.session_state.interacciones.append((label, i))
                # Interactuar con dado enemigo
                for j, ed in enumerate(enemigo):
                    if (enemigo_key, j) not in st.session_state.interacciones:
                        st.session_state.interacciones.append((enemigo_key, j))
                        break

    render_dados("Atacante", dados_atac, dados_def, "Defensor")
    render_dados("Defensor", dados_def, dados_atac, "Atacante")

# --- Botón para lanzar dados ---
if st.button("Lanzar dados"):
    st.session_state.dados_atacante = generar_dados(exito_norm_atac, critico_atac)
    st.session_state.dados_defensor = generar_dados(exito_norm_def, critico_def)
    st.session_state.interacciones = []

# --- Mostrar dados si existen ---
if st.session_state.dados_atacante and st.session_state.dados_defensor:
    mostrar_dados(
        st.session_state.dados_atacante,
        st.session_state.dados_defensor,
        "atacante"
    )

# --- Botón para reiniciar todo ---
if st.button("Reiniciar"):
    st.session_state.dados_atacante = []
    st.session_state.dados_defensor = []
    st.session_state.interacciones = []
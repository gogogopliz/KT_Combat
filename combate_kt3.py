
import streamlit as st
from uuid import uuid4

st.set_page_config(layout="wide")

# Inicialización
if "vidas" not in st.session_state:
    st.session_state.vidas = {"atacante": 10, "defensor": 10}
if "dados_atacante" not in st.session_state:
    st.session_state.dados_atacante = []
if "dados_defensor" not in st.session_state:
    st.session_state.dados_defensor = []
if "acciones_atacante" not in st.session_state:
    st.session_state.acciones_atacante = {}
if "acciones_defensor" not in st.session_state:
    st.session_state.acciones_defensor = {}

# Funciones
def generar_dados(tipo, cantidad):
    return [{"id": str(uuid4()), "tipo": tipo, "accion": "Atacar"} for _ in range(cantidad)]

def mostrar_dados(nombre, dados, acciones, enemigo):
    col1, col2 = st.columns([1, 5])
    with col1:
        st.markdown(f"**{nombre.capitalize()}**")
    with col2:
        cols = st.columns(len(dados))
        for i, dado in enumerate(dados):
            emoji = "🎯" if dado["tipo"] == "crítico" else "🎲"
            if cols[i].button(f"{emoji}", key=f"{nombre}_{dado['id']}"):
                acciones[dado["id"]] = "Bloquear" if acciones.get(dado["id"], "Atacar") == "Atacar" else "Atacar"

        # Mostrar debajo las acciones
        st.markdown("")
        cols_acc = st.columns(len(dados))
        for i, dado in enumerate(dados):
            accion = acciones.get(dado["id"], "Atacar")
            color = "🛡️" if accion == "Bloquear" else "⚔️"
            cols_acc[i].markdown(f"<div style='text-align: center;'>{color}</div>", unsafe_allow_html=True)

# UI
st.markdown("## Simulador de combate cuerpo a cuerpo (Kill Team 3)")

col1, col2 = st.columns(2)
with col1:
    vida_ata = st.number_input("Vida atacante", 1, 30, value=st.session_state.vidas["atacante"], key="vida_ata")
with col2:
    vida_def = st.number_input("Vida defensor", 1, 30, value=st.session_state.vidas["defensor"], key="vida_def")

st.session_state.vidas["atacante"] = vida_ata
st.session_state.vidas["defensor"] = vida_def

col1, col2 = st.columns(2)
with col1:
    n_norm_ata = st.number_input("Éxitos normales atacante", 0, 6, 2, key="norm_ata")
    n_crit_ata = st.number_input("Éxitos críticos atacante", 0, 6, 1, key="crit_ata")
    if st.button("Generar dados atacante"):
        st.session_state.dados_atacante = generar_dados("normal", n_norm_ata) + generar_dados("crítico", n_crit_ata)
        st.session_state.acciones_atacante = {d["id"]: "Atacar" for d in st.session_state.dados_atacante}

with col2:
    n_norm_def = st.number_input("Éxitos normales defensor", 0, 6, 2, key="norm_def")
    n_crit_def = st.number_input("Éxitos críticos defensor", 0, 6, 1, key="crit_def")
    if st.button("Generar dados defensor"):
        st.session_state.dados_defensor = generar_dados("normal", n_norm_def) + generar_dados("crítico", n_crit_def)
        st.session_state.acciones_defensor = {d["id"]: "Atacar" for d in st.session_state.dados_defensor}

st.markdown("---")
mostrar_dados("atacante", st.session_state.dados_atacante, st.session_state.acciones_atacante, "defensor")
mostrar_dados("defensor", st.session_state.dados_defensor, st.session_state.acciones_defensor, "atacante")

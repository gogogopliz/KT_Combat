
import streamlit as st
from PIL import Image
import base64

st.set_page_config(page_title="Combate KT3", layout="wide")

# Inicializar estado
if "vida_atacante" not in st.session_state:
    st.session_state.vida_atacante = 12
if "vida_defensor" not in st.session_state:
    st.session_state.vida_defensor = 12

st.title("Simulador de Combate - Kill Team 3")

col1, col2 = st.columns(2)

with col1:
    st.header("Atacante")
    vida_atacante = st.number_input("Vida inicial", min_value=1, max_value=50, value=st.session_state.vida_atacante, key="vida_atacante_input")
    daño_normal_ata = st.number_input("Daño normal", min_value=1, max_value=10, value=3)
    daño_critico_ata = st.number_input("Daño crítico", min_value=1, max_value=20, value=5)
    éxitos_normales_ata = st.number_input("Éxitos normales", min_value=0, max_value=6, value=2)
    éxitos_críticos_ata = st.number_input("Éxitos críticos", min_value=0, max_value=6, value=1)

with col2:
    st.header("Defensor")
    vida_defensor = st.number_input("Vida inicial", min_value=1, max_value=50, value=st.session_state.vida_defensor, key="vida_defensor_input")
    daño_normal_def = st.number_input("Daño normal", min_value=1, max_value=10, value=2)
    daño_critico_def = st.number_input("Daño crítico", min_value=1, max_value=20, value=4)
    éxitos_normales_def = st.number_input("Éxitos normales", min_value=0, max_value=6, value=2)
    éxitos_críticos_def = st.number_input("Éxitos críticos", min_value=0, max_value=6, value=1)

st.divider()

# Contadores de vida
st.session_state.vida_atacante = vida_atacante
st.session_state.vida_defensor = vida_defensor

# Funciones
def reset_dados():
    st.session_state.dados_ata = [{"tipo": "normal"}] * int(éxitos_normales_ata) + [{"tipo": "critico"}] * int(éxitos_críticos_ata)
    st.session_state.dados_def = [{"tipo": "normal"}] * int(éxitos_normales_def) + [{"tipo": "critico"}] * int(éxitos_críticos_def)
    for d in st.session_state.dados_ata:
        d["usado"] = False
    for d in st.session_state.dados_def:
        d["usado"] = False
    st.session_state.muerto = None

def usar_dado(agresor, idx):
    if agresor == "ata":
        dado = st.session_state.dados_ata[idx]
        objetivo = "def"
        daño = daño_critico_ata if dado["tipo"] == "critico" else daño_normal_ata
    else:
        dado = st.session_state.dados_def[idx]
        objetivo = "ata"
        daño = daño_critico_def if dado["tipo"] == "critico" else daño_normal_def

    if dado["usado"]:
        return

    acción = st.radio(f"¿Qué hacer con este dado {agresor}-{idx+1}?", ["Atacar", "Bloquear"], key=f"accion_{agresor}_{idx}")

    if acción == "Bloquear":
        opuestos = st.session_state.dados_def if agresor == "ata" else st.session_state.dados_ata
        for od in opuestos:
            if not od.get("usado", False):
                od["usado"] = True
                break
    else:
        if objetivo == "def":
            st.session_state.vida_defensor -= daño
            if st.session_state.vida_defensor <= 0:
                st.session_state.muerto = "Defensor"
        else:
            st.session_state.vida_atacante -= daño
            if st.session_state.vida_atacante <= 0:
                st.session_state.muerto = "Atacante"

    dado["usado"] = True

# Inicializar dados
if "dados_ata" not in st.session_state or st.button("Resetear dados"):
    reset_dados()

st.markdown("### Combate")

# Mostrar dados
def mostrar_dados(jugador, nombre, vida, daño_normal, daño_critico):
    st.markdown(f"**{nombre} - Vida: {vida}**")
    cols = st.columns(len(st.session_state[f"dados_{jugador}"]))
    for i, d in enumerate(st.session_state[f"dados_{jugador}"]):
        simbolo = "🟡" if d["tipo"] == "critico" else "⚪️"
        if d["usado"]:
            simbolo = "⬜️"
        with cols[i]:
            if not d.get("usado", False) and st.button(simbolo, key=f"{jugador}_{i}"):
                usar_dado(jugador, i)
    if st.session_state.muerto == nombre:
        st.markdown("**¡Muerto!**")

mostrar_dados("ata", "Atacante", st.session_state.vida_atacante, daño_normal_ata, daño_critico_ata)
mostrar_dados("def", "Defensor", st.session_state.vida_defensor, daño_normal_def, daño_critico_def)

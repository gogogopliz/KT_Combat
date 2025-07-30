
import streamlit as st
from PIL import Image
import base64

# Configuración inicial
st.set_page_config(page_title="Simulador Interactivo Kill Team 3", layout="centered")

st.markdown("## 🎲 Simulador Interactivo de Combate - Kill Team 3")
st.markdown("Haz clic en los dados para **atacar** o **bloquear**, y observa el efecto en la vida del oponente.")

# Funciones de utilidad
def load_image(path):
    return Image.open(path)

def render_die(index, crit=False, used=False, owner='attacker', dead=False):
    color = "yellow" if crit else "white"
    alpha = 0.3 if used or dead else 1.0
    label = f"{'¡Muerto!' if dead else ''}"
    style = f"display:inline-block; margin:2px; padding:4px; border-radius:4px; background-color:{color}; opacity:{alpha}; width:40px; height:40px; text-align:center; line-height:30px; font-weight:bold; border:1px solid black;"
    return st.markdown(f"<div style='{style}'>{label}</div>", unsafe_allow_html=True)

# Estado inicial
if "state" not in st.session_state:
    st.session_state.state = {
        "attacker": {"normal": 0, "crit": 0, "dmg_normal": 3, "dmg_crit": 5, "life": 12},
        "defender": {"normal": 0, "crit": 0, "dmg_normal": 3, "dmg_crit": 5, "life": 12},
        "attacker_dice": [],
        "defender_dice": [],
        "used_dice": {"attacker": [], "defender": []},
        "blocked_dice": {"attacker": [], "defender": []},
        "dead": {"attacker": False, "defender": False}
    }

def reset_combat():
    st.session_state.state["attacker_dice"] = []
    st.session_state.state["defender_dice"] = []
    st.session_state.state["used_dice"] = {"attacker": [], "defender": []}
    st.session_state.state["blocked_dice"] = {"attacker": [], "defender": []}
    st.session_state.state["dead"] = {"attacker": False, "defender": False}

# Configuración de ambos combatientes
col1, col2 = st.columns(2)
with col1:
    st.markdown("### ⚔️ Atacante")
    st.session_state.state["attacker"]["normal"] = st.number_input("Normales", 0, 10, 2, key="att_norm")
    st.session_state.state["attacker"]["crit"] = st.number_input("Críticos", 0, 10, 1, key="att_crit")
    st.session_state.state["attacker"]["dmg_normal"] = st.number_input("Daño Normal", 1, 10, 3, key="att_dmg_n")
    st.session_state.state["attacker"]["dmg_crit"] = st.number_input("Daño Crítico", 1, 20, 5, key="att_dmg_c")
    st.session_state.state["attacker"]["life"] = st.number_input("Vida", 1, 30, 12, key="att_life")
with col2:
    st.markdown("### 🛡️ Defensor")
    st.session_state.state["defender"]["normal"] = st.number_input("Normales", 0, 10, 2, key="def_norm")
    st.session_state.state["defender"]["crit"] = st.number_input("Críticos", 0, 10, 1, key="def_crit")
    st.session_state.state["defender"]["dmg_normal"] = st.number_input("Daño Normal", 1, 10, 3, key="def_dmg_n")
    st.session_state.state["defender"]["dmg_crit"] = st.number_input("Daño Crítico", 1, 20, 5, key="def_dmg_c")
    st.session_state.state["defender"]["life"] = st.number_input("Vida", 1, 30, 12, key="def_life")

# Generar dados si no están creados
if not st.session_state.state["attacker_dice"]:
    st.session_state.state["attacker_dice"] = ["crit"] * st.session_state.state["attacker"]["crit"] + ["normal"] * st.session_state.state["attacker"]["normal"]
    st.session_state.state["defender_dice"] = ["crit"] * st.session_state.state["defender"]["crit"] + ["normal"] * st.session_state.state["defender"]["normal"]

# Mostrar vidas actuales y dados
st.markdown("### Resultados")
layout = st.columns([1, 8])
layout[0].markdown(f"**❤️ Atacante:** {st.session_state.state['attacker']['life']}")
for i, die in enumerate(st.session_state.state["attacker_dice"]):
    render_die(i, crit=(die == "crit"), used=(i in st.session_state.state["used_dice"]["attacker"] or st.session_state.state["dead"]["attacker"]), owner='attacker', dead=st.session_state.state["dead"]["attacker"])

layout2 = st.columns([1, 8])
layout2[0].markdown(f"**❤️ Defensor:** {st.session_state.state['defender']['life']}")
for i, die in enumerate(st.session_state.state["defender_dice"]):
    render_die(i, crit=(die == "crit"), used=(i in st.session_state.state["used_dice"]["defender"] or st.session_state.state["dead"]["defender"]), owner='defender', dead=st.session_state.state["dead"]["defender"])

# Botón de reinicio
if st.button("🔄 Resetear"):
    reset_combat()
    st.experimental_rerun()

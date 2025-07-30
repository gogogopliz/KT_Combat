
import streamlit as st
import uuid

st.set_page_config(page_title="Simulador Interactivo Cuerpo a Cuerpo", layout="wide")

st.title("⚔️ Simulador Interactivo de Combate Cuerpo a Cuerpo - Kill Team 3")

st.markdown("Haz clic en los dados para decidir si atacan o bloquean. El combate termina si uno muere.")

# Función para crear un dado visual
def render_die(die_type, used=False, translucent=False, label=None):
    color = "yellow" if die_type == "crit" else "white"
    opacity = 0.4 if translucent else 1.0
    emoji = "💥" if die_type == "crit" else "⚪"
    return f'<span style="font-size:30px; opacity:{opacity}; color:{color}; margin:4px;">{emoji}<br>{label or ""}</span>'

# Inicialización de estados
if "attacker_dice" not in st.session_state:
    st.session_state.attacker_dice = []
    st.session_state.defender_dice = []
    st.session_state.attacker_hp = 10
    st.session_state.defender_hp = 10
    st.session_state.used_dice = set()
    st.session_state.blocked_dice = set()
    st.session_state.attacker_dmg = {"normal": 3, "crit": 5}
    st.session_state.defender_dmg = {"normal": 2, "crit": 4}
    st.session_state.killed = {"attacker": False, "defender": False}

# Reseteo
if st.button("🔄 Resetear combate"):
    st.session_state.attacker_dice = []
    st.session_state.defender_dice = []
    st.session_state.attacker_hp = 10
    st.session_state.defender_hp = 10
    st.session_state.used_dice = set()
    st.session_state.blocked_dice = set()
    st.session_state.killed = {"attacker": False, "defender": False}

col1, col2 = st.columns(2)
with col1:
    st.header("Atacante")
    st.session_state.attacker_hp = st.number_input("Vida del Atacante", 1, 50, st.session_state.attacker_hp)
    st.session_state.attacker_dmg["normal"] = st.number_input("Daño Normal Atacante", 1, 10, st.session_state.attacker_dmg["normal"])
    st.session_state.attacker_dmg["crit"] = st.number_input("Daño Crítico Atacante", 1, 10, st.session_state.attacker_dmg["crit"])
    num_a_normal = st.number_input("Éxitos Normales Atacante", 0, 10, 3)
    num_a_crit = st.number_input("Éxitos Críticos Atacante", 0, 10, 1)
    if st.button("Cargar dados atacante"):
        st.session_state.attacker_dice = [("normal", str(uuid.uuid4())) for _ in range(num_a_normal)] +                                          [("crit", str(uuid.uuid4())) for _ in range(num_a_crit)]

with col2:
    st.header("Defensor")
    st.session_state.defender_hp = st.number_input("Vida del Defensor", 1, 50, st.session_state.defender_hp)
    st.session_state.defender_dmg["normal"] = st.number_input("Daño Normal Defensor", 1, 10, st.session_state.defender_dmg["normal"])
    st.session_state.defender_dmg["crit"] = st.number_input("Daño Crítico Defensor", 1, 10, st.session_state.defender_dmg["crit"])
    num_d_normal = st.number_input("Éxitos Normales Defensor", 0, 10, 2)
    num_d_crit = st.number_input("Éxitos Críticos Defensor", 0, 10, 1)
    if st.button("Cargar dados defensor"):
        st.session_state.defender_dice = [("normal", str(uuid.uuid4())) for _ in range(num_d_normal)] +                                          [("crit", str(uuid.uuid4())) for _ in range(num_d_crit)]

# Función de interacción con dado
def handle_click(die_id, actor, die_type):
    if die_id in st.session_state.used_dice or st.session_state.killed["attacker"] or st.session_state.killed["defender"]:
        return

    action = st.radio(f"¿Qué hace el dado {die_id[:4]} ({actor})?", ["Atacar", "Bloquear"], horizontal=True, key=die_id)
    target = "defender" if actor == "attacker" else "attacker"
    target_dice = st.session_state.defender_dice if actor == "attacker" else st.session_state.attacker_dice
    target_dmg = st.session_state.attacker_dmg if actor == "defender" else st.session_state.defender_dmg

    if action == "Atacar":
        dmg = st.session_state.attacker_dmg[die_type] if actor == "attacker" else st.session_state.defender_dmg[die_type]
        st.session_state[target + "_hp"] -= dmg
        st.write(f"{actor.capitalize()} inflige {dmg} de daño a {target}. Vida restante: {st.session_state[target + '_hp']}")
    else:
        for i, (t_die_type, t_die_id) in enumerate(target_dice):
            if t_die_id not in st.session_state.blocked_dice and                (t_die_type == die_type or die_type == "crit"):
                st.session_state.blocked_dice.add(t_die_id)
                st.write(f"{actor.capitalize()} bloquea un dado de {target}.")
                break

    st.session_state.used_dice.add(die_id)

    # Muerte
    for p in ["attacker", "defender"]:
        if st.session_state[p + "_hp"] <= 0:
            st.session_state.killed[p] = True

# Mostrar vida
st.markdown(f"### ❤️ Vida Atacante: {st.session_state.attacker_hp}")
dice_row = ""
for die_type, die_id in st.session_state.attacker_dice:
    label = "¡Muerto!" if st.session_state.killed["attacker"] else ""
    dice_row += render_die(die_type, die_id in st.session_state.used_dice,
                           st.session_state.killed["attacker"] or die_id in st.session_state.blocked_dice, label)
st.markdown(dice_row, unsafe_allow_html=True)

# Mostrar vida
st.markdown(f"### ❤️ Vida Defensor: {st.session_state.defender_hp}")
dice_row = ""
for die_type, die_id in st.session_state.defender_dice:
    label = "¡Muerto!" if st.session_state.killed["defender"] else ""
    dice_row += render_die(die_type, die_id in st.session_state.used_dice,
                           st.session_state.killed["defender"] or die_id in st.session_state.blocked_dice, label)
st.markdown(dice_row, unsafe_allow_html=True)

# Selector para usar cada dado
for actor, dice_list in [("attacker", st.session_state.attacker_dice), ("defender", st.session_state.defender_dice)]:
    for die_type, die_id in dice_list:
        if die_id not in st.session_state.used_dice and not st.session_state.killed[actor]:
            handle_click(die_id, actor, die_type)

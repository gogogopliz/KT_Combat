import streamlit as st

st.set_page_config(layout="wide")

# Inicialización del estado de sesión
if "vidas" not in st.session_state:
    st.session_state.vidas = {"atacante": 12, "defensor": 12}
if "dados" not in st.session_state:
    st.session_state.dados = {"atacante": [], "defensor": []}
if "acciones" not in st.session_state:
    st.session_state.acciones = {"atacante": [], "defensor": []}
if "update_dados" not in st.session_state:
    st.session_state.update_dados = True

# Función para generar dados
def generar_dados(num_normales, num_criticos):
    return ["normal"] * num_normales + ["crítico"] * num_criticos

# Función para mostrar fila de dados
def mostrar_fila(nombre, color, dmg_norm, dmg_crit):
    col_vida, col_norm, col_crit = st.columns([1, 3, 3])
    with col_vida:
        st.session_state.vidas[nombre] = st.number_input(
            f"Vida {nombre}", 1, 30, st.session_state.vidas[nombre], key=f"vida_{nombre}"
        )
    with col_norm:
        num_normales = st.number_input(f"Éxitos normales {nombre}", 0, 6, len([d for d in st.session_state.dados[nombre] if d == "normal"]), key=f"norm_{nombre}")
    with col_crit:
        num_criticos = st.number_input(f"Éxitos críticos {nombre}", 0, 6, len([d for d in st.session_state.dados[nombre] if d == "crítico"]), key=f"crit_{nombre}")

    nuevos_dados = generar_dados(num_normales, num_criticos)
    if nuevos_dados != st.session_state.dados[nombre]:
        st.session_state.dados[nombre] = nuevos_dados
        st.session_state.acciones[nombre] = ["atacar"] * len(nuevos_dados)

    st.markdown(f"**{nombre.capitalize()}** (Daño: {dmg_norm}/{dmg_crit})")
    cols = st.columns(len(st.session_state.dados[nombre]) + 1)
    with cols[0]:
        st.markdown(f"**❤️ {st.session_state.vidas[nombre]}**")
    for i, dado in enumerate(st.session_state.dados[nombre]):
        with cols[i + 1]:
            if st.button(f"{dado} ({st.session_state.acciones[nombre][i]})", key=f"{nombre}_dado_{i}"):
                st.session_state.acciones[nombre][i] = (
                    "bloquear" if st.session_state.acciones[nombre][i] == "atacar" else "atacar"
                )

# Interfaz principal
st.title("Simulador de combate cuerpo a cuerpo - Kill Team 3")

col1, col2 = st.columns(2)
with col1:
    dmg_norm_atac = st.number_input("Daño normal atacante", 1, 10, 3)
    dmg_crit_atac = st.number_input("Daño crítico atacante", 1, 10, 5)
    mostrar_fila("atacante", "red", dmg_norm_atac, dmg_crit_atac)
with col2:
    dmg_norm_def = st.number_input("Daño normal defensor", 1, 10, 3)
    dmg_crit_def = st.number_input("Daño crítico defensor", 1, 10, 5)
    mostrar_fila("defensor", "blue", dmg_norm_def, dmg_crit_def)
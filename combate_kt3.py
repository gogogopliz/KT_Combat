import streamlit as st

st.set_page_config(layout="wide")
st.title("Simulador Combate Kill Team")

# Resetear
if st.button("🔄 Resetear"):
    st.session_state.clear()
    st.experimental_rerun()

# Inicializar estado
if "dados_aliado" not in st.session_state:
    st.session_state.dados_aliado = []
    st.session_state.dados_enemigo = []
    st.session_state.acciones = []
    st.session_state.vida_aliado_actual = 12
    st.session_state.vida_enemigo_actual = 12

# Columnas para la configuración
col1, col2 = st.columns(2)

with col1:
    st.header("⚔️ Atacante")
    vida_aliado = st.number_input("Vida inicial", min_value=1, max_value=50, value=12, key="vida_aliado")
    exito_normal_aliado = st.number_input("Éxitos normales", min_value=0, max_value=10, value=2, key="norm_aliado")
    exito_critico_aliado = st.number_input("Éxitos críticos", min_value=0, max_value=10, value=1, key="crit_aliado")
    daño_normal_aliado = st.number_input("Daño por éxito normal", min_value=1, max_value=10, value=3, key="daño_normal_aliado")
    daño_critico_aliado = st.number_input("Daño por éxito crítico", min_value=1, max_value=10, value=5, key="daño_critico_aliado")

with col2:
    st.header("🛡️ Defensor")
    vida_enemigo = st.number_input("Vida inicial", min_value=1, max_value=50, value=12, key="vida_enemigo")
    exito_normal_enemigo = st.number_input("Éxitos normales", min_value=0, max_value=10, value=2, key="norm_enemigo")
    exito_critico_enemigo = st.number_input("Éxitos críticos", min_value=0, max_value=10, value=1, key="crit_enemigo")
    daño_normal_enemigo = st.number_input("Daño por éxito normal", min_value=1, max_value=10, value=3, key="daño_normal_enemigo")
    daño_critico_enemigo = st.number_input("Daño por éxito crítico", min_value=1, max_value=10, value=5, key="daño_critico_enemigo")

# Cargar o resetear dados
if st.button("🎲 Cargar dados"):
    st.session_state.dados_aliado = [{"tipo": "critico", "usado": False}] * exito_critico_aliado + [{"tipo": "normal", "usado": False}] * exito_normal_aliado
    st.session_state.dados_enemigo = [{"tipo": "critico", "usado": False}] * exito_critico_enemigo + [{"tipo": "normal", "usado": False}] * exito_normal_enemigo
    st.session_state.vida_aliado_actual = vida_aliado
    st.session_state.vida_enemigo_actual = vida_enemigo
    st.session_state.acciones = []

# Función para mostrar dados
def mostrar_dados(dados, rival, is_aliado=True):
    fila = []
    for i, dado in enumerate(dados):
        color = "#FFD700" if dado["tipo"] == "critico" else "#FFFFFF"
        if dado["usado"]:
            color = "#CCCCCC"

        label = "💥" if dado["tipo"] == "critico" else "⚪"

        if not dado["usado"] and rival is not None:
            if st.button(label, key=f"{'a' if is_aliado else 'd'}_{i}"):
                accion = st.radio(
                    f"¿Qué hacer con este dado?", ["Atacar", "Bloquear"],
                    key=f"accion_{'a' if is_aliado else 'd'}_{i}"
                )
                if accion == "Atacar":
                    daño = daño_critico_aliado if (is_aliado and dado["tipo"] == "critico") else (
                        daño_normal_aliado if is_aliado else (
                            daño_critico_enemigo if dado["tipo"] == "critico" else daño_normal_enemigo
                        )
                    )
                    if is_aliado:
                        st.session_state.vida_enemigo_actual -= daño
                    else:
                        st.session_state.vida_aliado_actual -= daño
                    st.session_state.acciones.append(f"{'Atacante' if is_aliado else 'Defensor'} hace {daño} de daño.")
                else:
                    # Buscar primer dado rival sin usar y marcarlo
                    for rival_dado in rival:
                        if not rival_dado["usado"]:
                            rival_dado["usado"] = True
                            st.session_state.acciones.append(f"{'Atacante' if is_aliado else 'Defensor'} bloquea un dado del rival.")
                            break

                dado["usado"] = True

        if st.session_state.vida_aliado_actual <= 0 and is_aliado:
            label = "💀 ¡Muerto!"
        elif st.session_state.vida_enemigo_actual <= 0 and not is_aliado:
            label = "💀 ¡Muerto!"

        fila.append(st.markdown(
            f"<div style='display:inline-block;margin:2px;padding:8px;background-color:{color};border-radius:5px;text-align:center;'>{label}</div>",
            unsafe_allow_html=True
        ))

# Mostrar dados
st.markdown("### ⚔️ Zona de combate")

# Vida del Atacante
col_vida_a1, col_dados_a = st.columns([1, 9])
with col_vida_a1:
    st.markdown(f"❤️ {st.session_state.vida_aliado_actual}")
with col_dados_a:
    mostrar_dados(st.session_state.dados_aliado, st.session_state.dados_enemigo, is_aliado=True)

# Vida del Defensor
col_vida_e1, col_dados_e = st.columns([1, 9])
with col_vida_e1:
    st.markdown(f"❤️ {st.session_state.vida_enemigo_actual}")
with col_dados_e:
    mostrar_dados(st.session_state.dados_enemigo, st.session_state.dados_aliado, is_aliado=False)

# Mostrar acciones
if st.session_state.acciones:
    st.markdown("### 📜 Registro de acciones")
    for acc in st.session_state.acciones:
        st.markdown(f"- {acc}")
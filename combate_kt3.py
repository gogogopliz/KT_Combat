import streamlit as st

# Configuración general
st.set_page_config(page_title="Simulador Cuerpo a Cuerpo - Kill Team", layout="centered")

# Estado inicial
if "fase" not in st.session_state:
    st.session_state.fase = "inicio"
    st.session_state.vidas = {"atacante": 10, "defensor": 10}
    st.session_state.dmg = {
        "atacante": {"normal": 3, "critico": 5},
        "defensor": {"normal": 3, "critico": 5},
    }
    st.session_state.dados = {
        "atacante": {"normal": 0, "critico": 0},
        "defensor": {"normal": 0, "critico": 0},
    }
    st.session_state.resueltos = {"atacante": [], "defensor": []}
    st.session_state.turno = "atacante"
    st.session_state.historial = []

# Volver al inicio
def reiniciar():
    for k in ["fase", "vidas", "dmg", "dados", "resueltos", "turno", "historial"]:
        if k in st.session_state:
            del st.session_state[k]
    st.experimental_rerun()

st.title("⚔️ Simulador de Combate Cuerpo a Cuerpo - Kill Team")

if st.session_state.fase == "inicio":
    st.markdown("### Ajustes de combate")
    cols = st.columns(2)
    with cols[0]:
        vida_atac = st.number_input("Vida atacante", 1, 30, 10, key="vida_atac")
        dmg_norm_atac = st.number_input("Daño normal atacante", 1, 10, 3)
        dmg_crit_atac = st.number_input("Daño crítico atacante", 1, 15, 5)
        norm_atac = st.number_input("Éxitos normales", 0, 10, 2, key="norm_atac")
        crit_atac = st.number_input("Éxitos críticos", 0, 10, 1, key="crit_atac")
    with cols[1]:
        vida_def = st.number_input("Vida defensor", 1, 30, 10, key="vida_def")
        dmg_norm_def = st.number_input("Daño normal defensor", 1, 10, 3)
        dmg_crit_def = st.number_input("Daño crítico defensor", 1, 15, 5)
        norm_def = st.number_input("Éxitos normales", 0, 10, 2, key="norm_def")
        crit_def = st.number_input("Éxitos críticos", 0, 10, 1, key="crit_def")

    if st.button("Iniciar combate"):
        st.session_state.vidas = {"atacante": vida_atac, "defensor": vida_def}
        st.session_state.dmg = {
            "atacante": {"normal": dmg_norm_atac, "critico": dmg_crit_atac},
            "defensor": {"normal": dmg_norm_def, "critico": dmg_crit_def},
        }
        st.session_state.dados = {
            "atacante": {"normal": norm_atac, "critico": crit_atac},
            "defensor": {"normal": norm_def, "critico": crit_def},
        }
        st.session_state.fase = "combate"
        st.experimental_rerun()

elif st.session_state.fase == "combate":
    def mostrar_estado():
        st.markdown(f"#### Vida atacante: {st.session_state.vidas['atacante']}")
        st.markdown(f"#### Vida defensor: {st.session_state.vidas['defensor']}")
        st.markdown("---")
        st.markdown(f"**Turno actual:** {st.session_state.turno.capitalize()}")

    def hay_dados_sin_resolver(lado):
        return sum(st.session_state.dados[lado].values()) > 0

    def mostrar_dados(lado):
        dados = []
        for tipo in ["critico", "normal"]:
            for _ in range(st.session_state.dados[lado][tipo]):
                color = "#FFD700" if tipo == "critico" else "#CCCCCC"
                if st.button(f"{tipo[:1].upper()}", key=f"{lado}_{tipo}_{_}", help=f"{tipo}", use_container_width=True):
                    opciones = ["Golpear", "Bloquear"]
                    eleccion = st.radio("¿Qué hacer con este dado?", opciones, key=f"accion_{lado}_{tipo}_{_}")
                    st.session_state.accion_pendiente = (lado, tipo, eleccion)
                dados.append((tipo, color))
        return dados

    def ejecutar_accion():
        lado, tipo, accion = st.session_state.accion_pendiente
        opuesto = "defensor" if lado == "atacante" else "atacante"
        if accion == "Golpear":
            dmg = st.session_state.dmg[lado][tipo]
            st.session_state.vidas[opuesto] -= dmg
            st.session_state.historial.append(f"{lado} golpea con {tipo} y hace {dmg} de daño.")
        elif accion == "Bloquear":
            if st.session_state.dados[opuesto]["critico"] > 0 and tipo == "critico":
                st.session_state.dados[opuesto]["critico"] -= 1
                st.session_state.historial.append(f"{lado} bloquea un crítico del {opuesto}.")
            elif st.session_state.dados[opuesto]["normal"] > 0:
                st.session_state.dados[opuesto]["normal"] -= 1
                st.session_state.historial.append(f"{lado} bloquea un normal del {opuesto}.")
            else:
                st.session_state.historial.append(f"{lado} intentó bloquear pero no había dados.")
        st.session_state.dados[lado][tipo] -= 1
        del st.session_state["accion_pendiente"]
        st.session_state.turno = opuesto

    mostrar_estado()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Dados Atacante")
        mostrar_dados("atacante")
    with col2:
        st.markdown("### Dados Defensor")
        mostrar_dados("defensor")

    if "accion_pendiente" in st.session_state:
        st.button("Ejecutar acción", on_click=ejecutar_accion)

    if st.session_state.vidas["atacante"] <= 0 or st.session_state.vidas["defensor"] <= 0:
        st.session_state.fase = "final"
        st.experimental_rerun()

elif st.session_state.fase == "final":
    ganador = (
        "Empate"
        if st.session_state.vidas["atacante"] <= 0 and st.session_state.vidas["defensor"] <= 0
        else "Defensor"
        if st.session_state.vidas["atacante"] <= 0
        else "Atacante"
    )
    st.markdown(f"## 🏁 Combate finalizado - Ganador: **{ganador}**")
    st.markdown("### Historial de acciones:")
    for h in st.session_state.historial:
        st.markdown(f"- {h}")
    st.button("🔁 Volver al inicio", on_click=reiniciar)
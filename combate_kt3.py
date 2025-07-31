import streamlit as st

st.set_page_config(page_title="Combate KT3", layout="centered")

if "fase" not in st.session_state:
    st.session_state.fase = "inicio"
if "datos" not in st.session_state:
    st.session_state.datos = {}
if "turno" not in st.session_state:
    st.session_state.turno = "atacante"
if "acciones" not in st.session_state:
    st.session_state.acciones = {"atacante": [], "defensor": []}
if "dados" not in st.session_state:
    st.session_state.dados = {}

def reiniciar():
    st.session_state.fase = "inicio"
    st.session_state.datos = {}
    st.session_state.turno = "atacante"
    st.session_state.acciones = {"atacante": [], "defensor": []}
    st.session_state.dados = {}

# FASE INICIAL
if st.session_state.fase == "inicio":
    st.title("⚔️ Combate Cuerpo a Cuerpo - Kill Team 3")

    col1, col2 = st.columns(2)
    with col1:
        vida_atac = st.number_input("Vida Atacante", 1, 30, 12)
        dmg_n_atac = st.number_input("Daño Normal Atacante", 1, 10, 3)
        dmg_c_atac = st.number_input("Daño Crítico Atacante", 1, 20, 5)
        norm_atac = st.number_input("Éxitos normales A", 0, 10, 2)
        crit_atac = st.number_input("Éxitos críticos A", 0, 10, 1)
    with col2:
        vida_def = st.number_input("Vida Defensor", 1, 30, 12)
        dmg_n_def = st.number_input("Daño Normal Defensor", 1, 10, 3)
        dmg_c_def = st.number_input("Daño Crítico Defensor", 1, 20, 5)
        norm_def = st.number_input("Éxitos normales D", 0, 10, 2)
        crit_def = st.number_input("Éxitos críticos D", 0, 10, 1)

    if st.button("Iniciar combate"):
        st.session_state.datos = {
            "atacante": {
                "vida": vida_atac,
                "dano_normal": dmg_n_atac,
                "dano_critico": dmg_c_atac,
                "dados": ["critico"] * crit_atac + ["normal"] * norm_atac
            },
            "defensor": {
                "vida": vida_def,
                "dano_normal": dmg_n_def,
                "dano_critico": dmg_c_def,
                "dados": ["critico"] * crit_def + ["normal"] * norm_def
            }
        }
        st.session_state.fase = "combate"
        st.session_state.dados = {
            "atacante": st.session_state.datos["atacante"]["dados"].copy(),
            "defensor": st.session_state.datos["defensor"]["dados"].copy(),
        }
        st.experimental_rerun()

# FASE DE COMBATE
elif st.session_state.fase == "combate":
    st.title("⚔️ Resolución del combate")

    atacante = st.session_state.turno
    defensor = "defensor" if atacante == "atacante" else "atacante"

    vida_a = st.session_state.datos["atacante"]["vida"]
    vida_d = st.session_state.datos["defensor"]["vida"]

    st.markdown(f"**Turno de:** :red[{atacante.upper()}]")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Atacante")
        st.markdown(f"❤️ Vida: {vida_a}")
        st.markdown("🎲 Dados: " + " ".join([f"🔴" if d == "critico" else "⚪️" for d in st.session_state.dados["atacante"]]))
    with col2:
        st.subheader("Defensor")
        st.markdown(f"❤️ Vida: {vida_d}")
        st.markdown("🎲 Dados: " + " ".join([f"🔴" if d == "critico" else "⚪️" for d in st.session_state.dados["defensor"]]))

    opciones = []
    for i, dado in enumerate(st.session_state.dados[atacante]):
        if dado not in ["critico", "normal"]: continue
        opciones.append(f"{i+1} - {dado}")

    if opciones:
        eleccion = st.selectbox("Selecciona un dado", opciones, key="select_dado")
        accion = st.radio("¿Qué hacer?", ["Atacar", "Bloquear"], horizontal=True)

        if st.button("Ejecutar"):
            i = int(eleccion.split(" - ")[0]) - 1
            tipo_dado = st.session_state.dados[atacante][i]
            st.session_state.dados[atacante][i] = "usado"

            if accion == "Atacar":
                dmg = st.session_state.datos[atacante][f"dano_{tipo_dado}"]
                st.session_state.datos[defensor]["vida"] -= dmg
            elif accion == "Bloquear":
                dados_rivales = st.session_state.dados[defensor]
                for j, d in enumerate(dados_rivales):
                    if d in ["normal", "critico"]:
                        if tipo_dado == "normal" and d == "normal":
                            st.session_state.dados[defensor][j] = "bloqueado"
                            break
                        elif tipo_dado == "critico":
                            st.session_state.dados[defensor][j] = "bloqueado"
                            break
            # Cambiar turno si ambos tienen dados
            if any(d in ["normal", "critico"] for d in st.session_state.dados[defensor]):
                st.session_state.turno = defensor
            st.experimental_rerun()
    else:
        # Si ya no quedan dados, pasar a final
        st.session_state.fase = "final"
        st.experimental_rerun()

# FASE FINAL
elif st.session_state.fase == "final":
    st.title("✅ Combate finalizado")
    vida_a = st.session_state.datos["atacante"]["vida"]
    vida_d = st.session_state.datos["defensor"]["vida"]

    st.markdown(f"**Vida final Atacante:** ❤️ {vida_a}")
    st.markdown(f"**Vida final Defensor:** ❤️ {vida_d}")

    if vida_a > vida_d:
        ganador = "Atacante"
    elif vida_d > vida_a:
        ganador = "Defensor"
    else:
        ganador = "Empate"

    st.success(f"Resultado: **{ganador}**")

    st.button("🔁 Volver al inicio", on_click=reiniciar)
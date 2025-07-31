
import streamlit as st

st.set_page_config(page_title="Simulador de Combate - Kill Team 3", layout="centered")

# Reiniciar aplicación
def reset_app():
    for key in st.session_state.keys():
        del st.session_state[key]
    st.experimental_rerun()

# Inicialización de estado
if "fase" not in st.session_state:
    st.session_state.fase = "inicio"
    st.session_state.vidas = {"atacante": 10, "defensor": 10}
    st.session_state.daño = {"atacante": [3, 5], "defensor": [3, 5]}  # [normal, crítico]
    st.session_state.éxitos = {"atacante": [], "defensor": []}
    st.session_state.resultados = []
    st.session_state.exitos_usados = {"atacante": [], "defensor": []}

st.title("⚔️ Simulador Combate Kill Team 3")

if st.session_state.fase == "inicio":
    st.subheader("Introduce los datos de combate")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Atacante")
        st.session_state.vidas["atacante"] = st.number_input("Vida Atacante", 1, 30, st.session_state.vidas["atacante"], key="vida_atacante")
        st.session_state.daño["atacante"][0] = st.number_input("Daño Normal", 1, 10, st.session_state.daño["atacante"][0], key="daño_normal_a")
        st.session_state.daño["atacante"][1] = st.number_input("Daño Crítico", 1, 15, st.session_state.daño["atacante"][1], key="daño_critico_a")
        st.session_state.éxitos["atacante"] = st.multiselect("Éxitos Atacante", ["✅"] * 6 + ["✴️"] * 6, key="exitos_atacante")

    with col2:
        st.markdown("#### Defensor")
        st.session_state.vidas["defensor"] = st.number_input("Vida Defensor", 1, 30, st.session_state.vidas["defensor"], key="vida_defensor")
        st.session_state.daño["defensor"][0] = st.number_input("Daño Normal", 1, 10, st.session_state.daño["defensor"][0], key="daño_normal_d")
        st.session_state.daño["defensor"][1] = st.number_input("Daño Crítico", 1, 15, st.session_state.daño["defensor"][1], key="daño_critico_d")
        st.session_state.éxitos["defensor"] = st.multiselect("Éxitos Defensor", ["✅"] * 6 + ["✴️"] * 6, key="exitos_defensor")

    if st.button("Iniciar combate"):
        st.session_state.fase = "combate"
        st.session_state.turno = "atacante"
        st.session_state.exitos_usados = {"atacante": [], "defensor": []}
        st.experimental_rerun()

elif st.session_state.fase == "combate":
    atacante = st.session_state.turno
    defensor = "defensor" if atacante == "atacante" else "atacante"

    st.markdown(f"### Turno de {atacante.capitalize()}")
    st.markdown(f"**Vida Atacante:** {st.session_state.vidas['atacante']}")
    st.markdown(f"**Vida Defensor:** {st.session_state.vidas['defensor']}")

    éxitos_actuales = [e for i, e in enumerate(st.session_state.éxitos[atacante]) if i not in st.session_state.exitos_usados[atacante]]
    éxitos_rival = [e for i, e in enumerate(st.session_state.éxitos[defensor]) if i not in st.session_state.exitos_usados[defensor]]

    if not éxitos_actuales:
        st.session_state.turno = defensor if éxitos_rival else None
        if st.session_state.turno:
            st.experimental_rerun()
        else:
            st.session_state.fase = "resultado"
            st.experimental_rerun()

    for i, exito in enumerate(éxitos_actuales):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"Dado {i+1}: {exito}")
            if st.button(f"⚔️ Golpear {i}", key=f"golpe_{atacante}_{i}"):
                daño = st.session_state.daño[atacante][1 if exito == "✴️" else 0]
                st.session_state.vidas[defensor] -= daño
                st.session_state.exitos_usados[atacante].append(i)
                if st.session_state.vidas[defensor] <= 0:
                    st.session_state.fase = "resultado"
                else:
                    st.session_state.turno = defensor
                st.experimental_rerun()
        with col2:
            for j, rival_exito in enumerate(éxitos_rival):
                puede_bloquear = (exito == "✴️") or (exito == "✅" and rival_exito == "✅")
                if puede_bloquear and st.button(f"🛡️ Bloquear {j}", key=f"bloqueo_{atacante}_{i}_{j}"):
                    st.session_state.exitos_usados[atacante].append(i)
                    st.session_state.exitos_usados[defensor].append(j)
                    st.session_state.turno = defensor
                    st.experimental_rerun()

elif st.session_state.fase == "resultado":
    st.success("¡Combate finalizado!")
    st.markdown(f"**Vida Atacante restante:** {st.session_state.vidas['atacante']}")
    st.markdown(f"**Vida Defensor restante:** {st.session_state.vidas['defensor']}")
    st.button("Volver al inicio", on_click=reset_app)

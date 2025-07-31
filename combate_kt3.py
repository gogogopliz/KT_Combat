
import streamlit as st
from collections import deque

st.set_page_config(page_title="Combate Kill Team", layout="wide")

if "fase" not in st.session_state:
    st.session_state.fase = "inicio"
    st.session_state.acciones = deque()
    st.session_state.resultado = ""
    st.session_state.atacante = {"vida": 10, "norm": 0, "crit": 0, "dano_norm": 3, "dano_crit": 5}
    st.session_state.defensor = {"vida": 10, "norm": 0, "crit": 0, "dano_norm": 3, "dano_crit": 5}

def resetear():
    st.session_state.fase = "inicio"
    st.session_state.acciones = deque()
    st.session_state.resultado = ""
    st.session_state.atacante.update({"vida": 10, "norm": 0, "crit": 0, "dano_norm": 3, "dano_crit": 5})
    st.session_state.defensor.update({"vida": 10, "norm": 0, "crit": 0, "dano_crit": 5, "dano_norm": 3})

if st.session_state.fase == "inicio":
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### Atacante")
        st.session_state.atacante["vida"] = st.number_input("Vida A", 1, 30, 10, key="vidaA")
        st.session_state.atacante["norm"] = st.number_input("Éxitos Normales A", 0, 5, 0)
        st.session_state.atacante["crit"] = st.number_input("Críticos A", 0, 5, 0)
        st.session_state.atacante["dano_norm"] = st.number_input("Daño Normal A", 1, 10, 3)
        st.session_state.atacante["dano_crit"] = st.number_input("Daño Crítico A", 1, 20, 5)
    with c2:
        st.markdown("### Defensor")
        st.session_state.defensor["vida"] = st.number_input("Vida D", 1, 30, 10, key="vidaD")
        st.session_state.defensor["norm"] = st.number_input("Éxitos Normales D", 0, 5, 0)
        st.session_state.defensor["crit"] = st.number_input("Críticos D", 0, 5, 0)
        st.session_state.defensor["dano_norm"] = st.number_input("Daño Normal D", 1, 10, 3)
        st.session_state.defensor["dano_crit"] = st.number_input("Daño Crítico D", 1, 20, 5)
    if st.button("Iniciar combate"):
        for t, jugador in [("A", "atacante"), ("D", "defensor")]:
            for _ in range(st.session_state[jugador]["crit"]):
                st.session_state.acciones.append((t, "crit"))
            for _ in range(st.session_state[jugador]["norm"]):
                st.session_state.acciones.append((t, "norm"))
        st.session_state.fase = "combate"

elif st.session_state.fase == "combate":
    st.markdown("## Resolución de combate")
    st.markdown(f"**Vida A:** {st.session_state.atacante['vida']} | **Vida D:** {st.session_state.defensor['vida']}")
    if st.session_state.acciones:
        turno, tipo = st.session_state.acciones.popleft()
        jugador = "atacante" if turno == "A" else "defensor"
        oponente = "defensor" if jugador == "atacante" else "atacante"
        st.markdown(f"Dado de **{jugador.upper()}** ({'crítico' if tipo=='crit' else 'normal'})")
        accion = st.radio("Acción:", ["Golpear", "Bloquear"], horizontal=True, key=f"accion_{len(st.session_state.acciones)}")
        if st.button("Ejecutar acción", key=f"ejecutar_{len(st.session_state.acciones)}"):
            if accion == "Golpear":
                dano = st.session_state[jugador][f"dano_{tipo}"]
                st.session_state[oponente]["vida"] -= dano
                st.session_state.resultado += f"{jugador} golpea ({tipo}) y hace {dano} de daño.\n"
            else:
                st.session_state.resultado += f"{jugador} bloquea con un éxito {tipo}.\n"
            if st.session_state.atacante["vida"] <= 0 or st.session_state.defensor["vida"] <= 0:
                st.session_state.fase = "fin"
            st.experimental_rerun()
    else:
        st.session_state.fase = "fin"

elif st.session_state.fase == "fin":
    st.markdown("## Combate terminado")
    st.text(st.session_state.resultado)
    st.markdown(f"**Vida final Atacante:** {st.session_state.atacante['vida']}")
    st.markdown(f"**Vida final Defensor:** {st.session_state.defensor['vida']}")
    if st.button("Volver al inicio"):
        resetear()
        st.experimental_rerun()


import streamlit as st

st.set_page_config(page_title="Simulador Cuerpo a Cuerpo KT3", layout="wide")

if "reset" not in st.session_state:
    st.session_state.reset = False
if st.session_state.reset:
    for key in st.session_state.keys():
        del st.session_state[key]
    st.session_state.reset = False
    st.experimental_rerun()

st.title("Simulador Cuerpo a Cuerpo - Kill Team 3")

if "fase" not in st.session_state:
    st.session_state.fase = "inicio"

if st.session_state.fase == "inicio":
    with st.form("datos_combate"):
        st.subheader("Datos del atacante")
        vida_at = st.number_input("Vida atacante", 1, 30, 10, key="vida_at")
        dano_n_at = st.number_input("Daño normal atacante", 1, 10, 3)
        dano_c_at = st.number_input("Daño crítico atacante", 1, 15, 5)
        aciertos_n_at = st.slider("Éxitos normales atacante", 0, 6, 2)
        aciertos_c_at = st.slider("Éxitos críticos atacante", 0, 6, 1)

        st.subheader("Datos del defensor")
        vida_def = st.number_input("Vida defensor", 1, 30, 10, key="vida_def")
        dano_n_def = st.number_input("Daño normal defensor", 1, 10, 3)
        dano_c_def = st.number_input("Daño crítico defensor", 1, 15, 5)
        aciertos_n_def = st.slider("Éxitos normales defensor", 0, 6, 2)
        aciertos_c_def = st.slider("Éxitos críticos defensor", 0, 6, 1)

        submit = st.form_submit_button("Iniciar combate")

    if submit:
        st.session_state.fase = "combate"
        st.session_state.atacante = {
            "vida": vida_at,
            "dano_n": dano_n_at,
            "dano_c": dano_c_at,
            "dados": [{"tipo": "C", "usado": False}] * aciertos_c_at + [{"tipo": "N", "usado": False}] * aciertos_n_at,
        }
        st.session_state.defensor = {
            "vida": vida_def,
            "dano_n": dano_n_def,
            "dano_c": dano_c_def,
            "dados": [{"tipo": "C", "usado": False}] * aciertos_c_def + [{"tipo": "N", "usado": False}] * aciertos_n_def,
        }
        st.session_state.turno = "atacante"
        st.session_state.mensaje = ""
        st.experimental_rerun()


import streamlit as st
import random

st.set_page_config(layout="wide")
st.title("Simulador de Combate - Kill Team 3")

st.markdown("### Configuración de combate")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Atacante")
    éxitos_normales_atk = st.number_input("Éxitos normales", min_value=0, max_value=6, value=2, key="normales_atk")
    éxitos_críticos_atk = st.number_input("Éxitos críticos", min_value=0, max_value=6, value=1, key="criticos_atk")
    daño_normal_atk = st.number_input("Daño normal", min_value=1, max_value=10, value=3, key="daño_normal_atk")
    daño_critico_atk = st.number_input("Daño crítico", min_value=1, max_value=10, value=5, key="daño_critico_atk")
    vida_atk = st.number_input("Vida inicial", min_value=1, max_value=50, value=12, key="vida_atk")

with col2:
    st.subheader("Defensor")
    éxitos_normales_def = st.number_input("Éxitos normales", min_value=0, max_value=6, value=2, key="normales_def")
    éxitos_críticos_def = st.number_input("Éxitos críticos", min_value=0, max_value=6, value=1, key="criticos_def")
    daño_normal_def = st.number_input("Daño normal", min_value=1, max_value=10, value=3, key="daño_normal_def")
    daño_critico_def = st.number_input("Daño crítico", min_value=1, max_value=10, value=5, key="daño_critico_def")
    vida_def = st.number_input("Vida inicial", min_value=1, max_value=50, value=12, key="vida_def")

st.markdown("### Resolución del combate")

st.write("Haz clic en los dados para elegir si atacan, bloquean o son bloqueados (en desarrollo).")

col_dados = st.columns(2)

with col_dados[0]:
    st.markdown("**Atacante**")
    st.text(f"❤️ Vida: {vida_atk}")
    for i in range(éxitos_críticos_atk):
        st.button("🎯", key=f"atk_crit_{i}")
    for i in range(éxitos_normales_atk):
        st.button("🎲", key=f"atk_norm_{i}")

with col_dados[1]:
    st.markdown("**Defensor**")
    st.text(f"❤️ Vida: {vida_def}")
    for i in range(éxitos_críticos_def):
        st.button("🎯", key=f"def_crit_{i}")
    for i in range(éxitos_normales_def):
        st.button("🎲", key=f"def_norm_{i}")

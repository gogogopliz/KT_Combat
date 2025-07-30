import streamlit as st
from PIL import Image
import base64

st.set_page_config(layout="wide")

# --- Estado inicial ---
if "dados_aliado" not in st.session_state:
    st.session_state.dados_aliado = []
if "dados_enemigo" not in st.session_state:
    st.session_state.dados_enemigo = []
if "acciones" not in st.session_state:
    st.session_state.acciones = []

# --- Funciones ---
def crear_dados(tipo, cantidad, origen):
    return [{"tipo": tipo, "usado": False, "accion": None, "origen": origen, "bloqueado": False} for _ in range(cantidad)]

def resetear():
    st.session_state.dados_aliado = crear_dados("normal", st.session_state.n_aliado, "aliado") + \
                                     crear_dados("critico", st.session_state.c_aliado, "aliado")
    st.session_state.dados_enemigo = crear_dados("normal", st.session_state.n_enemigo, "enemigo") + \
                                      crear_dados("critico", st.session_state.c_enemigo, "enemigo")
    st.session_state.acciones = []

def actualizar_vidas():
    vida_aliado = st.session_state.vida_aliado
    vida_enemigo = st.session_state.vida_enemigo
    for accion in st.session_state.acciones:
        if accion["accion"] == "atacar":
            if accion["origen"] == "aliado":
                vida_enemigo -= accion["daño"]
            else:
                vida_aliado -= accion["daño"]
    return max(vida_aliado, 0), max(vida_enemigo, 0)

def elegir_accion(idx, origen):
    dado = None
    if origen == "aliado":
        dado = st.session_state.dados_aliado[idx]
    else:
        dado = st.session_state.dados_enemigo[idx]

    if dado["usado"]:
        return

    opciones = []
    opuesto = "enemigo" if origen == "aliado" else "aliado"
    dados_opuestos = st.session_state.dados_enemigo if opuesto == "enemigo" else st.session_state.dados_aliado
    hay_bloqueables = any(not d["usado"] and not d["bloqueado"] for d in dados_opuestos)

    if hay_bloqueables:
        opciones.append("Bloquear")
    opciones.append("Atacar")

    eleccion = st.radio(
        f"¿Qué hace el {origen} con este dado ({dado['tipo']})?",
        opciones,
        key=f"accion_{origen}_{idx}"
    )

    if eleccion == "Bloquear":
        for i, d in enumerate(dados_opuestos):
            if not d["usado"] and not d["bloqueado"]:
                d["bloqueado"] = True
                break
        dado["usado"] = True
        dado["accion"] = "bloquear"
        st.session_state.acciones.append({"origen": origen, "accion": "bloquear", "tipo": dado["tipo"], "daño": 0})
    elif eleccion == "Atacar":
        daño = st.session_state.daño_normal_aliado if origen == "aliado" else st.session_state.daño_normal_enemigo
        if dado["tipo"] == "critico":
            daño = st.session_state.daño_critico_aliado if origen == "aliado" else st.session_state.daño_critico_enemigo
        dado["usado"] = True
        dado["accion"] = "atacar"
        st.session_state.acciones.append({"origen": origen, "accion": "atacar", "tipo": dado["tipo"], "daño": daño})

# --- Configuración inicial ---
st.title("⚔️ Simulador Interactivo de Combate – Kill Team 3")

col1, col2 = st.columns(2)

with col1:
    st.subheader("⚔️ Atacante")
    st.session_state.vida_aliado = st.number_input("Vida inicial", min_value=1, max_value=50, value=12, key="vida_aliado")
    st.session_state.n_aliado = st.number_input("Éxitos normales", min_value=0, max_value=10, value=2, key="n_aliado")
    st.session_state.c_aliado = st.number_input("Éxitos críticos", min_value=0, max_value=10, value=1, key="c_aliado")
    st.session_state.daño_normal_aliado = st.number_input("Daño por éxito normal", min_value=1, max_value=10, value=3)
    st.session_state.daño_critico_aliado = st.number_input("Daño por crítico", min_value=1, max_value=20, value=5)

with col2:
    st.subheader("🛡️ Defensor")
    st.session_state.vida_enemigo = st.number_input("Vida inicial", min_value=1, max_value=50, value=10, key="vida_enemigo")
    st.session_state.n_enemigo = st.number_input("Éxitos normales", min_value=0, max_value=10, value=2, key="n_enemigo")
    st.session_state.c_enemigo = st.number_input("Éxitos críticos", min_value=0, max_value=10, value=1, key="c_enemigo")
    st.session_state.daño_normal_enemigo = st.number_input("Daño por éxito normal", min_value=1, max_value=10, value=2)
    st.session_state.daño_critico_enemigo = st.number_input("Daño por crítico", min_value=1, max_value=20, value=4)

st.button("🔁 Generar dados / Reiniciar", on_click=resetear)

# --- Mostrar dados ---
st.markdown("---")

vida_aliado_actual, vida_enemigo_actual = actualizar_vidas()

def mostrar_dados(dados, origen, vida_restante):
    col1, col2 = st.columns([1, 8])
    with col1:
        if vida_restante <= 0:
            st.markdown("💀 **¡Muerto!**")
        else:
            st.markdown(f"❤️ {vida_restante}")
    with col2:
        cols = st.columns(len(dados))
        for i, dado in enumerate(dados):
            estilo = "opacity: 0.3;" if dado["usado"] or dado["bloqueado"] or vida_restante <= 0 else ""
            color = "#fff" if dado["tipo"] == "normal" else "#ff0"
            simbolo = "✴️" if dado["tipo"] == "critico" else "🎯"
            if dado["accion"] == "bloquear":
                simbolo = "🛡️"
            elif dado["accion"] == "atacar":
                simbolo = "💥"
            with cols[i]:
                st.markdown(
                    f'<div style="font-size:40px; text-align:center; background-color:{color}; {estilo}" onclick="">{simbolo}</div>',
                    unsafe_allow_html=True,
                )
                if not dado["usado"] and not dado["bloqueado"] and vida_restante > 0:
                    if st.button("⚙️", key=f"{origen}_{i}"):
                        elegir_accion(i, origen)

# --- Mostrar dados en 2 filas ---
mostrar_dados(st.session_state.dados_aliado, "aliado", vida_aliado_actual)
mostrar_dados(st.session_state.dados_enemigo, "enemigo", vida_enemigo_actual)
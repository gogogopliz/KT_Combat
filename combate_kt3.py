import streamlit as st

st.set_page_config(page_title="Simulador Cuerpo a Cuerpo KT3", layout="wide")

# ---------- INICIALIZACIÓN ----------
if "estado" not in st.session_state:
    st.session_state.estado = "inicio"
if "turno" not in st.session_state:
    st.session_state.turno = "atacante"
if "dados" not in st.session_state:
    st.session_state.dados = {
        "atacante": {"normales": 0, "criticos": 0},
        "defensor": {"normales": 0, "criticos": 0},
    }
if "vidas" not in st.session_state:
    st.session_state.vidas = {"atacante": 10, "defensor": 10}
if "daños" not in st.session_state:
    st.session_state.daños = {"normal": 3, "critico": 5}
if "acciones" not in st.session_state:
    st.session_state.acciones = []
if "resueltos" not in st.session_state:
    st.session_state.resueltos = {"atacante": [], "defensor": []}
if "dados_bloqueados" not in st.session_state:
    st.session_state.dados_bloqueados = {"atacante": [], "defensor": []}

# ---------- FUNCIONES ----------
def reiniciar():
    for key in [
        "estado", "turno", "dados", "vidas", "daños", "acciones",
        "resueltos", "dados_bloqueados"
    ]:
        if key in st.session_state:
            del st.session_state[key]

def mostrar_dados(jugador):
    norm = st.session_state.dados[jugador]["normales"]
    crit = st.session_state.dados[jugador]["criticos"]
    bloqueados = st.session_state.dados_bloqueados[jugador]
    resueltos = st.session_state.resueltos[jugador]

    st.markdown(f"**{jugador.capitalize()}**")
    cols = st.columns(norm + crit if norm + crit > 0 else 1)
    i = 0
    for _ in range(norm):
        estado = "✅" if i in resueltos else ("❌" if i in bloqueados else "⚪")
        if cols[i].button(f"{estado} N{i+1}", key=f"{jugador}_N{i}"):
            seleccionar_dado(jugador, i, "normal")
        i += 1
    for _ in range(crit):
        estado = "✅" if i in resueltos else ("❌" if i in bloqueados else "🔴")
        if cols[i].button(f"{estado} C{i+1}", key=f"{jugador}_C{i}"):
            seleccionar_dado(jugador, i, "critico")
        i += 1

def seleccionar_dado(jugador, idx, tipo):
    if st.session_state.turno != jugador:
        return
    acciones = ["Golpear", "Bloquear"]
    eleccion = st.radio("¿Qué quieres hacer?", acciones, key=f"accion_{jugador}_{idx}")
    ejecutar_accion(jugador, idx, tipo, eleccion)

def ejecutar_accion(jugador, idx, tipo, accion):
    rival = "defensor" if jugador == "atacante" else "atacante"
    if idx in st.session_state.resueltos[jugador]:
        return

    # GOLPE
    if accion == "Golpear":
        daño = st.session_state.daños["normal"] if tipo == "normal" else st.session_state.daños["critico"]
        st.session_state.vidas[rival] -= daño
        st.session_state.resueltos[jugador].append(idx)

    # BLOQUEO
    elif accion == "Bloquear":
        objetivo = buscar_objetivo_para_bloquear(rival, tipo)
        if objetivo is not None:
            st.session_state.dados_bloqueados[rival].append(objetivo)
            st.session_state.resueltos[jugador].append(idx)

    cambiar_turno()

def buscar_objetivo_para_bloquear(rival, tipo):
    critico = tipo == "critico"
    for i in range(st.session_state.dados[rival]["criticos"]):
        if i not in st.session_state.resueltos[rival] and i not in st.session_state.dados_bloqueados[rival]:
            return i if critico else None
    for i in range(st.session_state.dados[rival]["normales"]):
        if i not in st.session_state.resueltos[rival] and i not in st.session_state.dados_bloqueados[rival]:
            return i
    return None

def cambiar_turno():
    if comprobar_fin_combate():
        st.session_state.estado = "fin"
        return
    st.session_state.turno = "defensor" if st.session_state.turno == "atacante" else "atacante"

def comprobar_fin_combate():
    return (
        st.session_state.vidas["atacante"] <= 0
        or st.session_state.vidas["defensor"] <= 0
    )

# ---------- INTERFAZ ----------

st.markdown("<h4 style='text-align:center;'>Simulador Cuerpo a Cuerpo - Kill Team 3</h4>", unsafe_allow_html=True)

if st.session_state.estado == "inicio":
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.vidas["atacante"] = st.number_input("Vida atacante", 1, 30, 10)
        st.session_state.dados["atacante"]["normales"] = st.number_input("Éxitos normales atacante", 0, 5, 2)
        st.session_state.dados["atacante"]["criticos"] = st.number_input("Éxitos críticos atacante", 0, 5, 1)
    with col2:
        st.session_state.vidas["defensor"] = st.number_input("Vida defensor", 1, 30, 10)
        st.session_state.dados["defensor"]["normales"] = st.number_input("Éxitos normales defensor", 0, 5, 2)
        st.session_state.dados["defensor"]["criticos"] = st.number_input("Éxitos críticos defensor", 0, 5, 1)

    col3, col4 = st.columns(2)
    with col3:
        st.session_state.daños["normal"] = st.number_input("Daño normal", 1, 10, 3)
    with col4:
        st.session_state.daños["critico"] = st.number_input("Daño crítico", 1, 10, 5)

    if st.button("Empezar combate"):
        st.session_state.estado = "combate"
        st.experimental_rerun()

elif st.session_state.estado == "combate":
    col1, col2 = st.columns(2)
    with col1:
        mostrar_dados("atacante")
    with col2:
        mostrar_dados("defensor")

    st.markdown(
        f"<div style='text-align:center;'>"
        f"<h5>Turno de: {st.session_state.turno.capitalize()}</h5>"
        f"<p>Vida Atacante: {st.session_state.vidas['atacante']}</p>"
        f"<p>Vida Defensor: {st.session_state.vidas['defensor']}</p>"
        f"</div>",
        unsafe_allow_html=True
    )

elif st.session_state.estado == "fin":
    ganador = "Atacante" if st.session_state.vidas["defensor"] <= 0 else "Defensor"
    st.success(f"¡{ganador} ha ganado el combate!")
    if st.button("Volver al inicio"):
        reiniciar()
        st.experimental_rerun()
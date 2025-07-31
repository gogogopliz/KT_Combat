import streamlit as st

st.set_page_config(layout="wide")

st.title("Simulador de Combate - Kill Team 3")

# Inicializar estados
if "dados_atacante" not in st.session_state:
    st.session_state.dados_atacante = []
if "dados_defensor" not in st.session_state:
    st.session_state.dados_defensor = []
if "vidas" not in st.session_state:
    st.session_state.vidas = {"atacante": 12, "defensor": 12}
if "accion_dado" not in st.session_state:
    st.session_state.accion_dado = None  # (jugador, índice)

# Reset
if st.button("🔁 Reiniciar"):
    st.session_state.dados_atacante = []
    st.session_state.dados_defensor = []
    st.session_state.vidas = {"atacante": 12, "defensor": 12}
    st.session_state.accion_dado = None
    st.experimental_rerun()

# CONFIGURACIÓN
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Atacante")
    vida_atac = st.number_input("Vida", 1, 30, st.session_state.vidas["atacante"], key="vida_atac")
    crits_atac = st.number_input("Éxitos críticos", 0, 6, 1, key="crits_atac")
    norms_atac = st.number_input("Éxitos normales", 0, 6, 2, key="norms_atac")
    dmg_norm_atac = st.number_input("Daño normal", 1, 10, 3, key="dmg_norm_atac")
    dmg_crit_atac = st.number_input("Daño crítico", 1, 12, 5, key="dmg_crit_atac")

with col2:
    st.markdown("### Defensor")
    vida_def = st.number_input("Vida", 1, 30, st.session_state.vidas["defensor"], key="vida_def")
    crits_def = st.number_input("Éxitos críticos", 0, 6, 1, key="crits_def")
    norms_def = st.number_input("Éxitos normales", 0, 6, 2, key="norms_def")
    dmg_norm_def = st.number_input("Daño normal", 1, 10, 2, key="dmg_norm_def")
    dmg_crit_def = st.number_input("Daño crítico", 1, 12, 4, key="dmg_crit_def")

# Actualizar vidas
st.session_state.vidas["atacante"] = vida_atac
st.session_state.vidas["defensor"] = vida_def

# Crear dados si están vacíos
def crear_dados(crit, norm, jugador):
    dados = []
    for i in range(crit):
        dados.append({"tipo": "crit", "usado": False, "jugador": jugador})
    for i in range(norm):
        dados.append({"tipo": "norm", "usado": False, "jugador": jugador})
    return dados

if not st.session_state.dados_atacante:
    st.session_state.dados_atacante = crear_dados(crits_atac, norms_atac, "atacante")
if not st.session_state.dados_defensor:
    st.session_state.dados_defensor = crear_dados(crits_def, norms_def, "defensor")

def mostrar_dados(dados, jugador):
    cols = st.columns(len(dados)+1)
    cols[0].markdown(f"❤️ {st.session_state.vidas[jugador]}")
    for i, dado in enumerate(dados):
        simbolo = "🟡" if dado["tipo"] == "crit" else "⚪"
        if dado["usado"]:
            simbolo = "🔒"
        if cols[i+1].button(simbolo, key=f"btn_{jugador}_{i}"):
            st.session_state.accion_dado = (jugador, i)

st.markdown("### Combate")

st.markdown("**Atacante**")
mostrar_dados(st.session_state.dados_atacante, "atacante")

st.markdown("**Defensor**")
mostrar_dados(st.session_state.dados_defensor, "defensor")

# Proceso de acción sobre dado pulsado
if st.session_state.accion_dado:
    jugador, index = st.session_state.accion_dado
    enemigo = "defensor" if jugador == "atacante" else "atacante"
    dados_jugador = st.session_state.dados_atacante if jugador == "atacante" else st.session_state.dados_defensor
    dados_enemigo = st.session_state.dados_defensor if jugador == "atacante" else st.session_state.dados_atacante
    dmg_norm = dmg_norm_atac if jugador == "atacante" else dmg_norm_def
    dmg_crit = dmg_crit_atac if jugador == "atacante" else dmg_crit_def
    vida_enemigo = st.session_state.vidas[enemigo]

    if not dados_jugador[index]["usado"]:
        accion = st.radio("¿Qué quieres hacer?", ["Atacar", "Bloquear"], horizontal=True)
        if st.button("✅ Confirmar acción"):
            if accion == "Atacar":
                daño = dmg_crit if dados_jugador[index]["tipo"] == "crit" else dmg_norm
                st.session_state.vidas[enemigo] -= daño
            else:
                for d in dados_enemigo:
                    if not d["usado"]:
                        d["usado"] = True
                        break
            dados_jugador[index]["usado"] = True
            st.session_state.accion_dado = None
            st.experimental_rerun()

# Resultado
if st.session_state.vidas["atacante"] <= 0:
    st.error("💀 ¡El Atacante ha muerto!")
elif st.session_state.vidas["defensor"] <= 0:
    st.success("☠️ ¡El Defensor ha muerto!")
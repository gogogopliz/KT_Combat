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
if "dados_usados" not in st.session_state:
    st.session_state.dados_usados = []

# Reset
if st.button("🔁 Reiniciar"):
    st.session_state.dados_atacante = []
    st.session_state.dados_defensor = []
    st.session_state.vidas = {"atacante": 12, "defensor": 12}
    st.session_state.dados_usados = []
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

# Crear dados
def crear_dados(crit, norm, jugador):
    dados = []
    for i in range(crit):
        dados.append({"tipo": "crit", "usado": False, "jugador": jugador})
    for i in range(norm):
        dados.append({"tipo": "norm", "usado": False, "jugador": jugador})
    return dados

st.session_state.dados_atacante = crear_dados(crits_atac, norms_atac, "atacante")
st.session_state.dados_defensor = crear_dados(crits_def, norms_def, "defensor")

def mostrar_dados(dados, rival_dados, jugador, rival, dmg_norm, dmg_crit):
    vida = st.session_state.vidas[rival]
    cols = st.columns(len(dados)+1)
    cols[0].markdown(f"**❤️ {st.session_state.vidas[jugador]}**")

    for i, dado in enumerate(dados):
        estado = "⚪" if dado["tipo"] == "norm" else "🟡"
        opacidad = ":white_circle:" if not dado["usado"] else "🔒"

        if st.session_state.vidas[jugador] <= 0:
            cols[i+1].markdown("💀 ¡Muerto!")
            continue

        if not dado["usado"]:
            if cols[i+1].button(f"{estado}", key=f"{jugador}_{i}"):
                accion = st.radio(f"{jugador.upper()} - Dado {i+1}", ["Atacar", "Bloquear"], horizontal=True, key=f"accion_{jugador}_{i}")
                if accion == "Atacar":
                    daño = dmg_crit if dado["tipo"] == "crit" else dmg_norm
                    st.session_state.vidas[rival] -= daño
                else:
                    # Bloqueo: buscar dado rival no usado
                    for rival_dado in rival_dados:
                        if not rival_dado["usado"]:
                            rival_dado["usado"] = True
                            break
                dado["usado"] = True
                st.experimental_rerun()
        else:
            cols[i+1].markdown(f"{opacidad}")

# Mostrar dados en filas
st.markdown("### Combate")
st.markdown("**Atacante**")
mostrar_dados(st.session_state.dados_atacante, st.session_state.dados_defensor, "atacante", "defensor", dmg_norm_atac, dmg_crit_atac)

st.markdown("**Defensor**")
mostrar_dados(st.session_state.dados_defensor, st.session_state.dados_atacante, "defensor", "atacante", dmg_norm_def, dmg_crit_def)

# Resultado
if st.session_state.vidas["atacante"] <= 0:
    st.error("💀 ¡El Atacante ha muerto!")
elif st.session_state.vidas["defensor"] <= 0:
    st.success("☠️ ¡El Defensor ha muerto!")
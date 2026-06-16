import streamlit as st
from database import init_db, get_random_location
from static_maps import get_satellite_image
from game_logic import check_guess

st.set_page_config(page_title="Onde Fica Isso?", page_icon="🌍", layout="centered")

# Inicialização
if "initialized" not in st.session_state:
    init_db()
    st.session_state.initialized = True
    st.session_state.score = 0
    st.session_state.attempts = 0
    st.session_state.current_location = None
    st.session_state.image = None
    st.session_state.zoom = 18

st.title("🌍 Onde Fica Isso?")
st.markdown("**Adivinhe o lugar pela imagem de satélite!**")

if st.button("🎲 Novo Local", type="primary", use_container_width=True) or st.session_state.current_location is None:
    with st.spinner("Carregando imagem..."):
        st.session_state.current_location = get_random_location()
        st.session_state.zoom = 18
        st.session_state.image = get_satellite_image(
            st.session_state.current_location["lat"], 
            st.session_state.current_location["lon"], 
            st.session_state.zoom
        )
    st.rerun()

if st.session_state.image and st.session_state.current_location:
    st.image(st.session_state.image, use_column_width=True, caption="🔍 Imagem de satélite (zoom alto)")

    guess = st.text_input("Qual é este lugar?", placeholder="Cristo Redentor, Rio de Janeiro, Paris...")

    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("✅ Enviar Palpite", type="primary", use_container_width=True):
            if check_guess(guess, st.session_state.current_location["answer"]):
                st.success(f"🎉 ACERTOU! Era **{st.session_state.current_location['answer']}**")
                st.session_state.score += 1
                st.balloons()
            else:
                st.error("❌ Errou!")
                st.session_state.attempts += 1
                if st.session_state.zoom > 15:
                    st.session_state.zoom -= 3
                    st.session_state.image = get_satellite_image(
                        st.session_state.current_location["lat"], 
                        st.session_state.current_location["lon"], 
                        st.session_state.zoom
                    )
                st.info(f"**Resposta:** {st.session_state.current_location['answer']}")

    with col2:
        st.metric("Pontos", st.session_state.score)

st.sidebar.metric("Pontuação", st.session_state.score)
st.sidebar.metric("Tentativas", st.session_state.attempts)
st.caption("Jogo em Python com Streamlit")
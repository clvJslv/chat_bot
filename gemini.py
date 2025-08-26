#import google.generativeai as genai

#genai.configure(api_key="AIzaSyDz6PLA2Z1nT0-zuwZ-NehWFzU3pX7OMt0")

#model = genai.GenerativeModel("gemini-1.5-flash")

#response = model.generate_content("Explique o que é Snowflake em 3 frases.")
#print(response.text)

#for m in genai.list_models():
#    print(m.name)
import streamlit as st
import google.generativeai as genai
import requests

gemini_key = st.secrets["GEMINI_API_KEY"]
SERP_API_KEY = st.secrets["SERP_API_KEYS"]
api_key = st.secrets["YOUTUBE_API_KEY"]

# Configurar Gemini

genai.configure(api_key="GEMINI_API_KEY") 
#genai.configure(api_key="AIzaSyDz6PLA2Z1nT0-zuwZ-NehWFzU3pX7OMt0")
model = genai.GenerativeModel("gemini-1.5-flash")

# Configurar SerpAPI
#SERP_API_KEY = "SERP_API_KEY"
#SERP_API_KEY = "19d8eb43b1f35459653abe2248c3788d0a2fd3274587b3d92c7bc137724b5b10"

# Configurar YouTube API
#api_key = "AIzaSyDz6PLA2Z1nT0-zuwZ-NehWFzU3pX7OMt0"


# Funções de busca
def buscar_links_serpapi(consulta):
    url = "https://serpapi.com/search"
    params = {
        "q": consulta,
        "location": "Brazil",
        "hl": "pt",
        "gl": "br",
        "api_key": SERP_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    resultados = []
    for item in data.get("organic_results", []):
        titulo = item.get("title")
        link = item.get("link")
        if titulo and link:
            resultados.append((titulo, link))
    return resultados

def buscar_videos_youtube(consulta):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": consulta,
        "type": "video",
        "maxResults": 3,
        "key": api_key
    }
    response = requests.get(url, params=params)
    data = response.json()
    videos = []
    for item in data.get("items", []):
        titulo = item["snippet"]["title"]
        video_id = item["id"]["videoId"]
        link = f"https://www.youtube.com/watch?v={video_id}"
        videos.append((titulo, link))
    return videos

# Inicializar histórico
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Interface
st.title("💬 Chatbot Inteligente com Links e Vídeos")
if st.button("🧹 Limpar conversa"):
    st.session_state.chat_history = []
    st.rerun()

user_input = st.text_input("Você:", key="input")

if user_input:
    # Adicionar pergunta ao histórico
    st.session_state.chat_history.append(("user", user_input))

    # Gerar resposta do Gemini
    #resposta = model.generate_content(user_input)
    resposta = model.generate_content(f"Responda como um chatbot amigável, em até 5 linhas:\n{user_input}")
    bot_reply = resposta.text.strip()
    st.session_state.chat_history.append(("bot", bot_reply))

    # Buscar links e vídeos
    links = buscar_links_serpapi(user_input)
    videos = buscar_videos_youtube(user_input)

    # Adicionar sugestões ao histórico
    if links:
        st.session_state.chat_history.append(("bot", "🔗 Aqui estão alguns links úteis:"))
        for titulo, url in links:
            st.session_state.chat_history.append(("bot", f"[{titulo}]({url})"))
    else:
        st.session_state.chat_history.append(("bot", "⚠️ Nenhum link encontrado."))

    if videos:
        st.session_state.chat_history.append(("bot", "🎥 Vídeos relacionados:"))
        for titulo, url in videos:
            st.session_state.chat_history.append(("bot", f"[{titulo}]({url})"))
    else:
        st.session_state.chat_history.append(("bot", "⚠️ Nenhum vídeo encontrado."))

# Exibir histórico de conversa
for autor, mensagem in st.session_state.chat_history:
    if autor == "user":
        st.markdown(f"**👤 Você:** {mensagem}")
    else:
        st.markdown(f"**🤖 Bot:** {mensagem}")


        
        

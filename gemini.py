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


# Configurar Gemini
genai.configure(api_key="AIzaSyDz6PLA2Z1nT0-zuwZ-NehWFzU3pX7OMt0")
model = genai.GenerativeModel("gemini-1.5-flash")

# Configurar SerpAPI
SERP_API_KEY = "19d8eb43b1f35459653abe2248c3788d0a2fd3274587b3d92c7bc137724b5b10"

# Configurar YouTube API
api_key = "AIzaSyDz6PLA2Z1nT0-zuwZ-NehWFzU3pX7OMt0"


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

# Interface
st.title("🔎 Chatbot com Links Reais e Vídeos")
user_input = st.text_input("Digite sua pergunta:")

if user_input:
    resposta = model.generate_content(f"Responda em 2 linhas:\n{user_input}")
    st.markdown("### 🤖 Resposta do Gemini:")
    st.markdown(resposta.text)

    st.markdown("### 🔗 Links úteis:")
    links = buscar_links_serpapi(user_input)
    if links:
        for titulo, url in links:
            st.markdown(f"- [{titulo}]({url})")
    else:
        st.warning("Nenhum link encontrado.")

    st.markdown("### 🎥 Vídeos relacionados:")
    videos = buscar_videos_youtube(user_input)
    if videos:
        for titulo, url in videos:
            st.markdown(f"- [{titulo}]({url})")
    else:
        st.warning("Nenhum vídeo encontrado.")

        
        

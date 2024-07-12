import os
import streamlit as st
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

AUDIO_DIR = "recordings"


def upload_to_gemini(path, mime_type=None):
    """Uploads the given file to Gemini."""
    file = genai.upload_file(path, mime_type=mime_type)
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file


def list_recordings(directory):
    """Lista os arquivos .wav no diretório especificado."""
    return [f for f in os.listdir(directory) if f.endswith('.wav')]


def list_and_chat_page():
    st.title("Listar Áudios e Chat com IA")
    st.header("Gravações")
    recordings = list_recordings(AUDIO_DIR)
    if recordings:
        selected_recording = st.selectbox("Selecione uma gravação", recordings)
        filepath = os.path.join(AUDIO_DIR, selected_recording)
        st.audio(filepath, format='audio/wav')

        st.header("Chat com IA")
        user_input = st.text_area("Digite sua mensagem para a IA")
    with st.spinner("Enviando mensagem..."):
        if st.button("Enviar"):
            try:
                # Upload do arquivo selecionado para a IA
                file = upload_to_gemini(filepath, mime_type="audio/wav")

                # IA Config
                generation_config = {
                    "temperature": 1,
                    "top_p": 0.95,
                    "top_k": 64,
                    "max_output_tokens": 8192,
                    "response_mime_type": "text/plain",
                }

                safety_settings = {
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                }

                model = genai.GenerativeModel(
                    model_name="gemini-1.5-pro",
                    generation_config=generation_config,
                    system_instruction="resuma o conteúdo do áudio a seguir de forma abrangente. O resumo deve capturar as informações mais importantes e a essência do material original, mantendo todos os pontos principais discutidos no áudio. Utilize uma linguagem formal e clara, adequada para um público acadêmico. Certifique-se de incluir detalhes importantes, como nomes, datas, eventos e quaisquer pontos críticos mencionados, mas evite informações redundantes ou menos relevantes. O objetivo é fornecer uma visão completa e precisa do conteúdo do áudio para leitores que buscam uma compreensão aprofundada do material.",
                    safety_settings=safety_settings,
                )

                # Iniciar sessão de chat com a IA
                chat_session = model.start_chat(
                    history=[
                        {
                            "role": "user",
                            "parts": [
                                file
                            ],
                        },
                    ]
                )

                # Enviar mensagem do usuário para a IA

                response = chat_session.send_message(user_input)
                st.title("Resposta da IA: ")
                st.write(response.text)
            except Exception as e:
                st.error(f"Erro ao comunicar com a IA: {e}")
        else:
            st.write("Nenhuma gravação disponível.")

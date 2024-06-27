import os
import signal
import subprocess
import sys
import streamlit as st

AUDIO_DIR = "recordings"
PID_FILE = "recorder_pid.txt"

os.makedirs(AUDIO_DIR, exist_ok=True)


def get_recorder_pid():
    """ Retorna o PID do processo de gravação, se existir. """
    try:
        with open(PID_FILE, "r") as f:
            return int(f.read().strip())
    except FileNotFoundError:
        return None


def manage_recorder_pid(pid=None, action='save'):
    """ Salva ou deleta o PID do processo baseado na ação. """
    if action == 'save' and pid is not None:
        with open(PID_FILE, "w") as f:
            f.write(str(pid))
    elif action == 'delete' and os.path.exists(PID_FILE):
        os.remove(PID_FILE)


def record_page():
    st.title("Gravador de Áudio")
    filename = st.text_input(
        "Digite o nome do arquivo para a gravação:", "recording")

    if st.button("Iniciar Gravação"):
        pid = get_recorder_pid()
        if pid:
            st.warning("Já está gravando...")
        elif filename:
            filepath = os.path.join(AUDIO_DIR, f"{filename}.wav")
            process = subprocess.Popen(
                [sys.executable, "audio_recorder.py", filepath])
            manage_recorder_pid(process.pid, 'save')
            st.success("Gravando...")
        else:
            st.error("Por favor, digite um nome válido para o arquivo.")

    if st.button("Finalizar Gravação"):
        pid = get_recorder_pid()
        if pid:
            os.kill(pid, signal.SIGTERM)
            manage_recorder_pid(action='delete')
            st.info("Gravação finalizada.")
        else:
            st.error("Nenhuma gravação em andamento.")

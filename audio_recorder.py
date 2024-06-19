import signal
import sys
import sounddevice as sd
import wave
import logging

# Configuração do logger
logging.basicConfig(level=logging.INFO)

def record_audio(filename, fs=44100):
    """ Grava áudio no arquivo especificado com a taxa de amostragem e canais definidos. """
    logging.info(f"Iniciando gravação... {filename}")
    with sd.InputStream(samplerate=fs, channels=2, dtype='int16') as stream:
        with wave.open(filename, 'wb') as wave_file:
            wave_file.setnchannels(2)
            wave_file.setsampwidth(2)
            wave_file.setframerate(fs)
            while True:
                data, _ = stream.read(1024)
                wave_file.writeframes(data)

def handle_signal(signum, frame):
    """ Gerencia sinais para finalizar a gravação de forma limpa. """
    logging.info("Finalizando gravação...")
    raise SystemExit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGINT, handle_signal)
    filename = sys.argv[1] if len(sys.argv) > 1 else "default_recording.wav"
    record_audio(filename)

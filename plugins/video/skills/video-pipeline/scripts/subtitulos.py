#!/usr/bin/env python3
"""Genera subtítulos .srt cortos (para redes) a partir de un audio, con faster-whisper (local, sin coste).

Uso: python3 subtitulos.py voz.mp3 subs.srt [--idioma es] [--modelo small] [--palabras 4] [--instalar]

--instalar  instala faster-whisper con pip si falta (unos 100 MB más el modelo, que se descarga la primera vez).
"""
import argparse
import subprocess
import sys
from pathlib import Path


def cargar_whisper(instalar: bool):
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        if not instalar:
            sys.exit("Falta faster-whisper. Vuelve a ejecutar con --instalar o: pip install faster-whisper")
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "faster-whisper"], check=True)
        from faster_whisper import WhisperModel
    return WhisperModel


def marca(segundos: float) -> str:
    ms = round(segundos * 1000)
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("audio", type=Path)
    parser.add_argument("srt", type=Path)
    parser.add_argument("--idioma", default="es")
    parser.add_argument("--modelo", default="small", help="tiny, base, small, medium, large-v3")
    parser.add_argument("--palabras", type=int, default=4, help="palabras máximas por subtítulo")
    parser.add_argument("--instalar", action="store_true")
    args = parser.parse_args()

    WhisperModel = cargar_whisper(args.instalar)
    import numpy as np  # viene con faster-whisper

    # Se decodifica con ffmpeg (16 kHz mono) para no depender de la versión de PyAV que traiga faster-whisper.
    crudo = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(args.audio), "-f", "f32le", "-ac", "1", "-ar", "16000", "-"],
        capture_output=True, check=True,
    ).stdout
    audio = np.frombuffer(crudo, dtype=np.float32)
    modelo = WhisperModel(args.modelo, device="cpu", compute_type="int8")
    segmentos, _ = modelo.transcribe(audio, language=args.idioma, word_timestamps=True, vad_filter=True)

    palabras = [p for seg in segmentos for p in (seg.words or [])]
    bloques, actual = [], []
    for palabra in palabras:
        actual.append(palabra)
        corta_frase = palabra.word.strip().endswith((".", ",", "?", "!", ":", ";"))
        if len(actual) >= args.palabras or corta_frase:
            bloques.append(actual)
            actual = []
    if actual:
        bloques.append(actual)

    lineas = []
    for i, bloque in enumerate(bloques, 1):
        texto = " ".join(p.word.strip() for p in bloque).strip()
        lineas += [str(i), f"{marca(bloque[0].start)} --> {marca(bloque[-1].end)}", texto, ""]
    args.srt.parent.mkdir(parents=True, exist_ok=True)
    args.srt.write_text("\n".join(lineas), encoding="utf-8")
    print(f"Listo: {args.srt} ({len(bloques)} subtítulos)")


if __name__ == "__main__":
    main()

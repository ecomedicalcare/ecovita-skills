#!/usr/bin/env python3
"""Monta un video listo para publicar a partir de plan.json (ver reference/plan.md).

Uso: python3 montar.py ruta/al/plan.json [--formato 9:16]

Solo necesita ffmpeg y ffprobe. Escribe en <carpeta del plan>/salida/.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

FORMATOS = {
    "9:16": (1080, 1920),
    "1:1": (1080, 1080),
    "4:5": (1080, 1350),
    "16:9": (1920, 1080),
}
EXT_VIDEO = {".mp4", ".mov", ".webm", ".mkv", ".m4v"}
ZOOM = 0.12  # cuánto acerca o aleja cada escena


def duracion(ruta: Path) -> float:
    salida = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(ruta)],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    return float(salida)


def filtro_imagen(entrada: int, seg: float, movimiento: str, w: int, h: int, fps: int, etiqueta: str) -> str:
    n = max(1, round(seg * fps))
    centro_x, centro_y = "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"
    z, x, y = {
        "zoom_in": (f"1+{ZOOM}*on/{n}", centro_x, centro_y),
        "zoom_out": (f"{1 + ZOOM}-{ZOOM}*on/{n}", centro_x, centro_y),
        "paneo_der": (f"{1 + ZOOM}", f"(iw-iw/zoom)*on/{n}", centro_y),
        "paneo_izq": (f"{1 + ZOOM}", f"(iw-iw/zoom)*(1-on/{n})", centro_y),
        "fijo": ("1", "0", "0"),
    }.get(movimiento, (f"1+{ZOOM}*on/{n}", centro_x, centro_y))
    # Se escala al doble antes del zoom para que el movimiento no tiemble.
    return (
        f"[{entrada}:v]scale={w * 2}:{h * 2}:force_original_aspect_ratio=increase,crop={w * 2}:{h * 2},"
        f"zoompan=z='{z}':x='{x}':y='{y}':d={n}:s={w}x{h}:fps={fps},"
        f"trim=end_frame={n},setsar=1,format=yuv420p[{etiqueta}]"
    )


def filtro_clip(entrada: int, seg: float, w: int, h: int, fps: int, etiqueta: str) -> str:
    return (
        f"[{entrada}:v]scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},fps={fps},"
        f"tpad=stop_mode=clone:stop_duration={seg:.3f},trim=duration={seg:.3f},setpts=PTS-STARTPTS,"
        f"setsar=1,format=yuv420p[{etiqueta}]"
    )


def estilo_subtitulos(estilo: dict, h: int) -> str:
    # libass mide los .srt sobre una altura de 288: se convierten los píxeles reales a esa escala.
    escala = 288 / h
    tamano = round(estilo.get("tamano", 64) * escala, 1)
    margen = round(estilo.get("margen_inferior", 480 if h > 1500 else 120) * escala)
    color = estilo.get("color", "FFFFFF")
    borde = estilo.get("borde", "000000")
    bgr = lambda hexa: hexa[4:6] + hexa[2:4] + hexa[0:2]  # noqa: E731 (ASS usa BGR)
    return (
        f"FontName={estilo.get('fuente', 'Inter')},FontSize={tamano},Bold=1,"
        f"PrimaryColour=&H00{bgr(color)},OutlineColour=&H00{bgr(borde)},BorderStyle=1,Outline=1.6,Shadow=0,"
        f"Alignment=2,MarginV={margen}"
    )


def montar(plan_path: Path, formato: str) -> Path:
    carpeta = plan_path.resolve().parent
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    w, h = FORMATOS[formato]
    fps = int(plan.get("fps", 30))
    escenas = [dict(e) for e in plan["escenas"]]
    if not escenas:
        sys.exit("El plan no tiene escenas.")

    voz = carpeta / plan["voz"] if plan.get("voz") else None
    if voz:
        total_escenas = sum(float(e["duracion"]) for e in escenas)
        dur_voz = duracion(voz) + 0.4  # respiro al final
        if dur_voz > total_escenas:
            escenas[-1]["duracion"] = float(escenas[-1]["duracion"]) + dur_voz - total_escenas
    if plan.get("cierre"):
        escenas.append(dict(plan["cierre"]))

    entradas, filtros, etiquetas = [], [], []
    for i, escena in enumerate(escenas):
        archivo = carpeta / escena["archivo"]
        if not archivo.exists():
            sys.exit(f"No existe {archivo}")
        seg = float(escena["duracion"])
        etiqueta = f"v{i}"
        entradas += ["-i", str(archivo)]
        if archivo.suffix.lower() in EXT_VIDEO:
            filtros.append(filtro_clip(i, seg, w, h, fps, etiqueta))
        else:
            filtros.append(filtro_imagen(i, seg, escena.get("movimiento", "zoom_in"), w, h, fps, etiqueta))
        etiquetas.append(f"[{etiqueta}]")
    total = sum(float(e["duracion"]) for e in escenas)

    filtros.append(f"{''.join(etiquetas)}concat=n={len(etiquetas)}:v=1:a=0[vbase]")
    video_final = "[vbase]"
    if plan.get("subtitulos"):
        srt = (carpeta / plan["subtitulos"]).resolve()
        ruta = str(srt).replace("\\", "/").replace(":", r"\:").replace("'", r"\'")
        estilo = estilo_subtitulos(plan.get("estilo_subtitulos", {}), h)
        filtros.append(f"[vbase]subtitles='{ruta}':force_style='{estilo}'[vsub]")
        video_final = "[vsub]"

    siguiente = len(escenas)
    audio_final = None
    if voz:
        entradas += ["-i", str(voz)]
        indice_voz = siguiente
        siguiente += 1
        if plan.get("musica"):
            entradas += ["-stream_loop", "-1", "-i", str(carpeta / plan["musica"])]
            vol = float(plan.get("volumen_musica", 0.12))
            filtros.append(f"[{indice_voz}:a]aresample=48000,asplit=2[voz][llave]")
            filtros.append(f"[{siguiente}:a]aresample=48000,volume={vol}[mus]")
            # La música baja sola cuando habla la voz (ducking).
            filtros.append("[mus][llave]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[musd]")
            filtros.append("[voz][musd]amix=inputs=2:duration=longest:normalize=0[mezcla]")
            fuente = "[mezcla]"
        else:
            fuente = f"[{indice_voz}:a]"
        filtros.append(f"{fuente}apad,atrim=duration={total:.3f},loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[afinal]")
        audio_final = "[afinal]"

    salida = carpeta / "salida" / f"{plan.get('slug', carpeta.name)}_{formato.replace(':', 'x')}.mp4"
    salida.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *entradas,
           "-filter_complex", ";".join(filtros), "-map", video_final]
    if audio_final:
        cmd += ["-map", audio_final, "-c:a", "aac", "-b:a", "192k", "-ar", "48000"]
    cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-r", str(fps),
            "-t", f"{total:.3f}", "-movflags", "+faststart", str(salida)]
    subprocess.run(cmd, check=True)
    if audio_final:
        ajustar_volumen(salida)
    return salida


def ajustar_volumen(salida: Path, objetivo: float = -14.0) -> None:
    """loudnorm en una pasada se queda corto en clips breves: se mide y se corrige la ganancia."""
    medida = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(salida), "-af", "ebur128", "-f", "null", "-"],
                            capture_output=True, text=True).stderr
    valores = re.findall(r"I:\s+(-?\d+(?:\.\d+)?) LUFS", medida)
    if not valores:
        return
    ganancia = objetivo - float(valores[-1])
    if abs(ganancia) < 0.5:
        return
    temporal = salida.with_suffix(".tmp.mp4")
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(salida), "-c:v", "copy",
                    "-af", f"volume={ganancia:.2f}dB,alimiter=limit=0.84:level=false", "-c:a", "aac", "-b:a", "192k",
                    "-ar", "48000", "-movflags", "+faststart", str(temporal)], check=True)
    temporal.replace(salida)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("plan", type=Path)
    parser.add_argument("--formato", choices=FORMATOS, help="Solo este formato (por defecto, los del plan)")
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    formatos = [args.formato] if args.formato else plan.get("formatos", ["9:16"])
    for formato in formatos:
        if formato not in FORMATOS:
            sys.exit(f"Formato desconocido: {formato}. Usa uno de {', '.join(FORMATOS)}")
        print(f"Listo: {montar(args.plan, formato)}")


if __name__ == "__main__":
    main()

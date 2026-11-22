---
name: video-pipeline
description: Produce un video listo para publicar (Reel/TikTok/Short 9:16, post 1:1 o 4:5, YouTube 16:9) de principio a fin — guion, imágenes, animación, voz en off, subtítulos, montaje y exportación por red. Úsala cuando pidan "haz un video", "un reel", "un short", "video para redes", "anima estas imágenes" o "ponle voz y subtítulos".
---

# Video pipeline (Ecovita)

Lleva un pedido de video desde la idea hasta uno o varios `.mp4` listos para subir. Sigue las fases en orden y
**para a pedir aprobación** donde se indica: varias fases gastan créditos de servicios externos.

## Reglas Ecovita (mandan sobre todo lo demás)

- **Contenido de salud:** nada de promesas de curación, diagnósticos ni cifras sin fuente. Si el guion menciona un
  dato clínico, cita la fuente en la descripción del post (puedes buscarla con el conector PubMed). Cierra con un aviso
  breve del tipo «Consulta a tu médico» cuando el tema lo pida.
- **Privacidad:** nunca uses fotos, nombres, voces ni datos de pacientes reales. Las personas que aparezcan son
  generadas o son modelos o equipo con consentimiento por escrito.
- **Créditos y claves:** antes de generar con un servicio de pago (ElevenLabs, Muapi/Open Higgsfield, Higgsfield), di
  qué vas a generar, cuántas piezas y el modelo, y espera el sí. No repitas una generación para "reintentar": cobra otra
  vez. Las API keys no se piden en el chat; van en la interfaz del servicio o como secreto del entorno.
- **Marca:** si existe una guía de marca (skill `brand-voice`), aplícala al guion, los textos en pantalla y los colores.

## Fase 0 · Brief (pregunta solo lo que falte)

Tema y objetivo (educar, captar citas, anunciar), red(es) y formato, duración (por defecto 30 s), tono, llamada a la
acción, idioma y acento de la voz, y si hay material propio (logo, fotos, clips). Guarda el plan en
`videos/<slug>/plan.json` (formato en `reference/plan.md`).

## Fase 1 · Guion y storyboard (gratis)

- Gancho en los primeros 2 s, una idea por escena, escenas de 3–6 s, CTA al final.
- ~2,5 palabras por segundo de voz: 30 s ≈ 75 palabras.
- Por escena: texto de la voz, texto en pantalla (máx. 6–8 palabras), prompt visual y duración.
- Muestra el guion y **espera aprobación** antes de gastar créditos.

## Fase 2 · Imágenes (elige la fuente)

| Fuente | Cuándo | Coste |
|---|---|---|
| Material propio del cliente | Siempre que lo haya | 0 |
| ElevenLabs `creative_generate_image` | Sesión en la nube, rápido | Créditos ElevenLabs |
| Open Higgsfield AI (local, Muapi) | Look de cine con control de cámara/lente | Créditos Muapi |
| Figma `generate_image` / plantillas Canva | Gráficos, portadas, textos de marca | Según plan |

Prompts: incluye formato (vertical 9:16), estilo coherente entre escenas (misma paleta, luz y lente) y "sin texto"
(el texto lo pone el montaje). Guarda en `videos/<slug>/escenas/01.png`, `02.png`…

## Fase 3 · Movimiento

- **Gratis:** el montaje aplica zoom/paneo lento (efecto Ken Burns) a cada imagen. Suele bastar para redes.
- **IA imagen→video:** ElevenLabs `creative_generate_video` (o modelos de video de Muapi). Úsalo solo en 1–3 tomas
  clave; confirma antes porque es lo más caro. Guarda como `escenas/03.mp4`.
- **Local y gratis con GPU NVIDIA:** ComfyUI + Wan 2.x o LTX-Video (en la computadora del usuario).

## Fase 4 · Voz en off

- ElevenLabs `creative_generate_speech`: el `voice_id` sale de `creative_list_voices` (nunca de memoria). Di qué voz
  elegiste. Guarda `videos/<slug>/voz.mp3`.
- Alternativa open source sin coste: Piper o Kokoro TTS en local.

## Fase 5 · Subtítulos (gratis)

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/video-pipeline/scripts/subtitulos.py" videos/<slug>/voz.mp3 videos/<slug>/subs.srt --idioma es
```

Usa faster-whisper en local (añade `--instalar` para instalarlo con pip si falta; pide permiso la primera vez). Revisa el `.srt`: corrige nombres propios y términos médicos.
Si no se puede instalar, genera el `.srt` a partir del guion y de la duración de cada escena.

## Fase 6 · Montaje

**Opción A — FFmpeg (por defecto, 100 % libre):**

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/video-pipeline/scripts/montar.py" videos/<slug>/plan.json
```

Une escenas (imagen con zoom o clip), voz, música opcional con ducking, subtítulos quemados y normaliza el volumen
a −14 LUFS. Sale `videos/<slug>/salida/<slug>_<formato>.mp4`.

**Opción B — Remotion (animaciones de texto, plantillas de marca, gráficos):** ver `reference/remotion.md`.
Ojo a la licencia: Remotion es gratis para personas y empresas de hasta 3 empleados; si no, hace falta licencia de
empresa. Pregunta antes de elegirla.

## Fase 7 · Control de calidad (obligatorio)

1. `ffprobe` del archivo: resolución, fps, duración y que tenga audio.
2. Extrae 3 fotogramas (inicio, medio, final) con `ffmpeg -ss … -frames:v 1` y míralos: texto legible, sin cortes,
   nada tapado por la interfaz de la red (zonas seguras en `reference/formatos.md`).
3. Repasa las reglas Ecovita de arriba.

## Fase 8 · Entrega y publicación

- Entrega el `.mp4`, una portada (fotograma o imagen) y un `publicacion.md` con título, texto del post, hashtags,
  fuentes citadas y texto alternativo.
- Exporta los formatos pedidos (`"formatos": ["9:16","1:1"]` en el plan).
- **Publicar** solo con un "sí, publícalo" explícito: con Zapier (YouTube, TikTok, Instagram, Facebook) si el usuario
  tiene esas cuentas conectadas, o lo sube a mano. Por defecto, programar como borrador o privado.

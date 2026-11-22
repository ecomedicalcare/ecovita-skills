# ecovita-video · procedencia

Pedido de 22-nov-2026: hacer videos listos para publicar (a partir de la guía «Open Higgsfield con Claude Code»).

- **Todo es propio** (MIT, como el repo): `SKILL.md`, `reference/` y los scripts `montar.py` (FFmpeg) y
  `subtitulos.py` (faster-whisper). Sin hooks. Los scripts solo usan la biblioteca estándar de Python y llaman a
  `ffmpeg`/`ffprobe`; `subtitulos.py` instala `faster-whisper` con pip solo si se le pasa `--instalar`.
- **Remotion:** sus skills oficiales (`remotion-dev/skills`) **no se copian**: no traen una licencia de redistribución
  propia y Remotion pide licencia de empresa a partir de 4 empleados. Se instalan dentro de cada proyecto de video
  con `npx remotion skills add` (ver `skills/video-pipeline/reference/remotion.md`).
- **Open Higgsfield AI** (`sunnychase/open-higgsfield-ai`) no se incluye: es una app web que corre en la computadora
  del usuario y genera imágenes con créditos de Muapi.ai. La skill la menciona como fuente de imágenes.

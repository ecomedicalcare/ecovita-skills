# plan.json

Lo lee `scripts/montar.py`. Las rutas son relativas a la carpeta del plan.

```json
{
  "slug": "hidratacion-verano",
  "formatos": ["9:16"],
  "fps": 30,
  "voz": "voz.mp3",
  "musica": "musica.mp3",
  "volumen_musica": 0.12,
  "subtitulos": "subs.srt",
  "estilo_subtitulos": { "fuente": "Inter", "tamano": 64, "color": "FFFFFF", "borde": "000000" },
  "escenas": [
    { "archivo": "escenas/01.png", "duracion": 4, "movimiento": "zoom_in" },
    { "archivo": "escenas/02.png", "duracion": 5, "movimiento": "zoom_out" },
    { "archivo": "escenas/03.mp4", "duracion": 4 },
    { "archivo": "escenas/04.png", "duracion": 5, "movimiento": "paneo_der" }
  ],
  "cierre": { "archivo": "escenas/logo.png", "duracion": 2.5, "movimiento": "fijo" }
}
```

- `musica`, `subtitulos` y `cierre` son opcionales. `musica` debe ser libre de derechos (Biblioteca de audio de
  YouTube, Pixabay Music…), y el plan debe anotar de dónde sale.
- `movimiento`: `zoom_in` (por defecto), `zoom_out`, `paneo_der`, `paneo_izq`, `fijo`. En clips de video se ignora.
- Si la voz dura más que la suma de escenas, la última escena se alarga; si dura menos, el video termina con la
  última escena.
- `formatos`: `9:16` (1080×1920), `1:1` (1080×1080), `4:5` (1080×1350), `16:9` (1920×1080). Las imágenes se recortan
  al centro para llenar el cuadro: genera con el formato principal y deja el sujeto centrado.

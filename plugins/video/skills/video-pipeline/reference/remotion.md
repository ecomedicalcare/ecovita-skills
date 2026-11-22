# Montaje con Remotion

Para títulos animados, plantillas de marca reutilizables, gráficos y transiciones que FFmpeg no da.

**Licencia:** Remotion no es open source estándar. Es gratis para personas, organizaciones sin ánimo de lucro y
empresas de hasta 3 empleados; las demás necesitan licencia de empresa (<https://www.remotion.dev/license>).
Confírmalo con el usuario antes de usarlo para Ecovita.

## Skills oficiales de Remotion

No se copian a este repo (no tienen una licencia de redistribución propia). Se instalan dentro del proyecto de video:

```bash
npx create-video@latest --yes --blank --no-tailwind --skills videos/remotion
```

o, en un proyecto que ya existe:

```bash
npx remotion skills add
```

Quedan disponibles `/remotion-best-practices`, `/remotion-create`, `/remotion-markup`, `/remotion-captions`,
`/remotion-render`, `/remotion-studio`, etc. Cárgalas antes de escribir código de Remotion.

## Flujo

1. Copia a `public/` las imágenes, los clips y `voz.mp3` del plan.
2. Una composición por formato (`Reel` 1080×1920, `Cuadrado` 1080×1080) a 30 fps; la duración la marca la voz
   (`calculateMetadata`).
3. Subtítulos: convierte el `.srt` con `@remotion/captions` y muéstralos palabra a palabra (skill `remotion-captions`).
4. Render: `npx remotion render <Composicion> ../<slug>/salida/<slug>_9x16.mp4`.
5. Pasa el control de calidad de la Fase 7 igual que con FFmpeg.

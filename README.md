# ecovita-skills

Skills, agentes y comandos de [ECC](https://github.com/affaan-m/ECC) elegidos para el CRM
[Ecovita](https://github.com/ecomedicalcare/ecovita-crm). Ecovita lo consulta en cada sesión de
Claude Code mediante su `.claude/settings.json`. **No incluye los hooks de ECC**, para que las
sesiones sean rápidas y no choquen con las reglas del CRM.

## Cómo funciona

- `skills.txt`: la lista de piezas (`skill:`, `agent:` o `command:` + nombre de ECC).
- `plugins/ecovita/`: el plugin con las piezas copiadas. **No se edita a mano**: lo genera el script.
- `scripts/sincronizar.mjs`: copia desde ECC lo que dice `skills.txt` y quita lo que ya no esté.
- `.github/workflows/sincronizar-ecc.yml`: cada lunes trae las novedades de ECC y abre un Pull
  Request para revisarlas. También se puede lanzar a mano desde la pestaña **Actions**.

## Agregar o quitar una pieza

1. Edita `skills.txt` (busca nombres en <https://github.com/affaan-m/ECC/tree/main/skills>,
   `agents/` o `commands/`).
2. Ejecuta `node scripts/sincronizar.mjs` y sube el cambio, o espera la sincronización semanal.

## Revisión de diseño: Impeccable (`plugins/diseno/`)

`plugins/diseno/skills/impeccable/` es la skill [Impeccable](https://github.com/DevvGwardo/impeccable) (de Paul Bakaus,
empaquetada por DevvGwardo, Apache 2.0, versión en `UPSTREAM`). Va en un plugin aparte (`ecovita-diseno`) porque el
sincronizador de ECC borra de `plugins/ecovita/` todo lo que no está en `skills.txt`.

- Se copiaron solo los textos (`SKILL.md`, `reference/`, `LICENSE`, `NOTICE.md`). **No** se copió `scripts/`: su lanzador
  descarga y ejecuta un binario; la skill funciona sin él (camino «Launcher unavailable»).
- `SKILL.md` lleva al principio un bloque **Ecovita** con las reglas del CRM (mandan las del repo y el kit, modo Operate,
  cómo se usa al migrar y al revisar lo ya migrado). Al actualizar desde el original, conservar ese bloque.

## Frontend Stack (`plugins/frontend/`)

Pedido de Carlos (19-nov-2026): las skills de diseño frontend de
[claude-code-frontend-skills](https://github.com/JaimeJunr/claude-code-frontend-skills), solo las que sirven al CRM y sin
scripts ni hooks: el enrutador `frontend-stack` (elige qué skill guía cada fase y resuelve choques entre paquetes, con los
agentes `design-director` y `ui-reviewer`), `frontend-design` de Anthropic, las de animación de Emil Kowalski, UX research
y copy, y Taste. Plugin `ecovita-frontend`. Mandan las reglas de Ecovita-crm (bloque «Ecovita» del enrutador). Detalle y
licencias en `plugins/frontend/NOTICE.md`.

## UI UX Pro Max (`plugins/uiux/`)

Pedido de Carlos (20-nov-2026): más criterio al diseñar componentes y estilo. Es la skill `ui-ux-pro-max` de
[ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) (MIT, versión en `UPSTREAM`) con su
buscador local (Python estándar, sin red): reglas de accesibilidad, toque, responsive, tipografía, color, animación,
formularios, navegación, gráficos y React. Plugin `ecovita-uiux`. Las demás skills del paquete no se instalaron (traen
descargas, IA externa o Tailwind/shadcn). El bloque «Ecovita» de su `SKILL.md` deja claro que manda el kit y que no se
usa `--persist`. Detalle en `plugins/uiux/NOTICE.md`.

## Licencia

El contenido de `plugins/ecovita/` viene de ECC (MIT, © Affaan Mustafa); ver `plugins/ecovita/LICENSE-ECC`.
El de `plugins/diseno/skills/impeccable/` viene de Impeccable (Apache 2.0); ver su `LICENSE` y `NOTICE.md`.
Los de `plugins/frontend/` conservan sus licencias MIT y Apache-2.0 (`plugins/frontend/LICENSE-*` y `NOTICE.md`).
El de `plugins/uiux/` viene de UI UX Pro Max (MIT, © Next Level Builder); ver `plugins/uiux/LICENSE`.

## Seguridad y revisión de código (`plugins/seguridad/`)

Pedido de Carlos (25-nov-2026): selección de [Anthropic-Cybersecurity-Skills](https://github.com/mukul975/Anthropic-Cybersecurity-Skills),
las guías de [Strix](https://github.com/usestrix/strix), [code-review-skill](https://github.com/awesome-skills/code-review-skill) y
las revisiones de [gstack](https://github.com/garrytan/gstack) (`cso`, `review`, `design-review`, `plan-design-review`, `qa-only`).
Plugin `ecovita-seguridad`, solo textos (sin scripts, binarios ni hooks). Detalle, versiones y licencias en
`plugins/seguridad/NOTICE.md`.

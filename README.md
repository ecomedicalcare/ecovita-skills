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

## Licencia

El contenido de `plugins/ecovita/` viene de ECC (MIT, © Affaan Mustafa); ver `plugins/ecovita/LICENSE-ECC`.
El de `plugins/diseno/skills/impeccable/` viene de Impeccable (Apache 2.0); ver su `LICENSE` y `NOTICE.md`.
Los de `plugins/frontend/` conservan sus licencias MIT y Apache-2.0 (`plugins/frontend/LICENSE-*` y `NOTICE.md`).

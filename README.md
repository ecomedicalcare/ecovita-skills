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

## Licencia

El contenido de `plugins/ecovita/` viene de ECC (MIT, © Affaan Mustafa); ver `plugins/ecovita/LICENSE-ECC`.

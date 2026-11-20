# ecovita-uiux · procedencia

Pedido de Carlos (20-nov-2026): tener más criterio al diseñar componentes y estilo.

- **Origen:** [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill), MIT
  (© 2024 Next Level Builder, ver `LICENSE`). Commit copiado en `UPSTREAM`.
- **Qué se copió:** solo la skill `ui-ux-pro-max` (`SKILL.md`, `references/`, `data/`) y su buscador
  (`scripts/search.py`, `core.py`, `design_system.py`, `reasoning_contract.py`, `preview.py`).
- **Qué no:** los tests y `validate_data.py` (mantenimiento del catálogo), la CLI, y las demás skills del paquete
  (`design-system`, `ui-styling`, `brand`, `design`, `slides`, `banner-design`): traen descargas de red, generadores con
  IA externa o se basan en Tailwind/shadcn, que el CRM no usa.
- **Revisión de seguridad:** el buscador es Python estándar (csv, json, re, argparse, pathlib…), sin red ni
  `subprocess`; lee sus CSV y solo escribe archivos si se le pide con `--persist`/`--preview`, que en Ecovita no se usan.
- **Cambios:** el bloque «Ecovita» al principio de `SKILL.md` (mandan las reglas del CRM y el kit; sin `--persist`) y
  las rutas del buscador (`${CLAUDE_PLUGIN_ROOT}/skills/ui-ux-pro-max/…` en vez de `.claude/skills/…`).
  Al actualizar desde el original, conservar el bloque y rehacer el cambio de rutas.

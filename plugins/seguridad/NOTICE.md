# ecovita-seguridad

Pedido de Carlos (25-nov-2026): skills para auditar Ecovita y, al final de la migración, para la prueba de ataque con IA
(Strix) y la revisión UI/UX clínica. **Solo se copiaron los textos** (`SKILL.md`, referencias y licencias); no scripts,
binarios ni hooks. Mandan las reglas de Ecovita-crm (`CLAUDE.md`, `docs/seguridad.md`).

| Origen | Licencia | Versión | Qué se tomó |
|---|---|---|---|
| [mukul975/Anthropic-Cybersecurity-Skills](https://github.com/mukul975/Anthropic-Cybersecurity-Skills) | Apache 2.0 | 54a7988 | 8 de 818: límites de peticiones (2), HIPAA, secretos con gitleaks, respaldos contra ransomware, pruebas de API, autorización por función y por propiedad |
| [usestrix/strix](https://github.com/usestrix/strix) | Apache 2.0 | 9ed84f9 | Sus 9 guías (`skills/`). La herramienta en sí (Python + Docker + llave de IA) **no** está instalada: ver `docs/pendientes-produccion.md` |
| [garrytan/gstack](https://github.com/garrytan/gstack) | MIT | 1145e80 | `cso`, `review`, `design-review`, `plan-design-review`, `qa-only`. Sus comandos que usan el navegador de gstack (`browse`) no funcionan sin instalarlo; el criterio sí |
| [awesome-skills/code-review-skill](https://github.com/awesome-skills/code-review-skill) | MIT | 4850184 | Toda (texto y referencias) |

Licencias completas en `licencias/`. Para actualizar: volver a copiar solo los textos y anotar aquí la versión.

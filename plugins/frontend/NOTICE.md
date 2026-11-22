# Procedencia

Copia parcial de https://github.com/JaimeJunr/claude-code-frontend-skills (commit en `UPSTREAM`), pedida por Carlos
(19-nov-2026). Se tomaron solo las skills útiles para un CRM web con kit propio, sin scripts ni hooks:

| Carpeta | Origen | Licencia |
|---|---|---|
| `skills/frontend-stack`, `agents/` | Frontend Stack, Jaime Basso | MIT (`LICENSE-frontend-stack`) |
| `skills/frontend-design` | Anthropic | Apache-2.0 (`LICENSE-frontend-design`) |
| `skills/animate`, `improve-animations`, `review-animations`, `animation-vocabulary`, `apple-design`, `prototype`, … | Emil Kowalski | MIT (`LICENSE-emil`) |
| `skills/user-research`, `research-synthesis`, `ux-copy` | Anthropic | Apache-2.0 (`LICENSE-ux-research`) |
| `skills/taste-skill` | Leonxlnx | MIT (`LICENSE-taste`) |

No se copiaron: UI UX Pro Max (depende de scripts de Python), Hallmark, Hyperframes, taste-imagegen, design-mobile-apps,
emil-native ni los hooks/scripts de Impeccable (Impeccable ya está en `plugins/diseno`). El bloque «Ecovita» al inicio de
`skills/frontend-stack/SKILL.md` es local: las reglas del repo Ecovita-crm mandan sobre las de estas skills.

## taste-skill 2.5.1 (22-nov-2026)

Carlos pidió instalar https://github.com/Leonxlnx/taste-skill (commit `f6b76575`, v2.5.1, MIT · `LICENSE-taste`). Reemplaza a la
v2 en `skills/taste-skill`: SKILL.md (con una nota «Ecovita» al inicio y sin el hook `Stop`), `references/`, `library/`,
`scripts/` y `assets/` **sin fotos, vídeos ni demos** (38 MB; se toman del original si una página pública los necesita).
Se conserva de la v2 `references/app-screens.md` (pantallas de trabajo: tableros, ajustes, bandejas), útil para el CRM.
En el CRM manda el kit: de esta skill se usa el criterio de movimiento, microinteracciones y anti-«hecho por IA».

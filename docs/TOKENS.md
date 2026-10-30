# Tokens de diseño

| Regla | Valor |
|---|---|
| Gap (máx. 3) | 8 · 16 · 24 px (`--gap-1/2/3`) |
| Pesos de fuente (máx. 3) | 400 · 600 · 800 (`--fw-regular/semibold/bold`) |
| Escala de 8 px | espaciados, radios, iconos y tamaños de fuente (16 · 24 · 32 · 40 · 48 px; interlineado = tamaño + 8) |
| Color primary | solo en botones de acción principal: `+1` del progreso, "Reproducir macro", "Abrir build en Questlog" y "Dame un consejo" |

`tokens.py` aplica estas reglas automáticamente al CSS y a los estilos en línea durante la construcción.

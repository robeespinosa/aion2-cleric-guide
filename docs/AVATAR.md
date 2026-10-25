# Avatar de BlackCrown — documentación

## Qué es
Un personaje 2.5D (títere por capas) hecho a partir de la imagen de referencia. **No es un modelo 3D ni tiene rig facial**: se anima con transformaciones CSS por capas, párpados y bocas dibujados en SVG y una máquina de estados en JavaScript. El archivo del motor es el bloque `avatar.js` dentro de `index.html`.

## Assets (todos existen en `assets/`)
| Carpeta | Contenido |
|---|---|
| `assets/avatar/` | `head.webp`, `torso.webp`, `legL.webp`, `legR.webp`: capas recortadas de la imagen original (a 0.45× de resolución) |
| `assets/face/` | 7 caras de la hoja de expresiones (neutral, sonrisa, risa, sorpresa, pensativo, guiño, triste), usadas en la burbuja |
| `assets/audio/` | 171 clips mp3 cortados del audio largo de ElevenLabs (`NNN.mp3`, NNN = nº de línea en `phrases.txt`) |
| `data/avatar.json` | posición/tamaño de cada capa y colores de piel y párpados |
| `data/phrases.json` | las 177 frases, su clip (`a`) y su duración (`d`); `a:null` = sin clip, usa la voz del navegador |

## Estados
`idle, walk, turn(sin uso aparte: el giro es el suavizado de dirección), wave, observe, hide, climb, interact, run, surprised, returnHome, sleep` + superposiciones `talk` (habla) y `blink` (parpadeo).
Prioridades: `idle 0 < walk/observe/wave/run/hide/climb/interact 1 < returnHome 2 < surprised 3`. Lo que inicia el usuario (clic) siempre prevalece: pilla al personaje si está escondido, trepando o empujando; si no, le pide un consejo.

## Añadir un movimiento nuevo
1. En `PR` pon su prioridad (`PR.miAccion=1`).
2. En `start(n)` añade `else if(n==="miAccion"){to("miAccion",{...})}` y su cooldown con `cooldown("miAccion",60)`.
3. En `tick(dt)` añade `else if(s==="miAccion"){...}`: mueve `A.x`, `A.y`, `A.spd` (velocidad de zancada), `A.lean`, `A.dir`, y cuando acabe llama a `to("idle")` o `home()`.
4. Añádelo a `chooseAction()` con su peso. Para frases, `say("categoria")` o `sayLine(find(/regex/))`.

## Frases y voz
- Categorías en `cats` (se calculan por el inicio de cada frase en `build5.py`).
- Audio: cada frase usa su clip; si no existe o falla, usa `speechSynthesis` (voz española del navegador). El texto personalizado (recomendaciones según tu GS) siempre usa la voz del navegador.
- **Los clips se cortaron automáticamente** alineando por silencios y duración esperada. No puedo oír el audio: si alguna frase suena con otra voz distinta a su texto, anota su número y se reasigna en `seg.json`.
- Lip-sync: las letras se convierten en 8 formas de boca (AE, O, U, MBP, FV, STD, RL, SIL) repartidas por palabra; con audio, la energía del sonido modula la abertura. Con voz del navegador se resincroniza con los eventos de palabra.
- Botones 🔊/🔇 (silencio) y 🙈 (ocultar) abajo a la izquierda; se guardan en el navegador.

## Accesibilidad y rendimiento
`prefers-reduced-motion`: el personaje no camina ni se esconde, se queda quieto y solo habla al hacer clic. Se detiene con la pestaña oculta. Solo el personaje y los botones capturan clics (`pointer-events` selectivo).

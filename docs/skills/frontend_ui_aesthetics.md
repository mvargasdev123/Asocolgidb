# Skill: UI/UX Aesthetics Premium (Frontend)

## Descripción
Esta habilidad fuerza al Frontend Agent a mantener un estándar visual altísimo. El objetivo es que la aplicación no luzca como una "plantilla genérica", sino como un software premium.

## Reglas
1.  **Reciclaje de Identidad Visual:** El Agente debe buscar SIEMPRE en `../../../Mamá cosas/Asocolgi/frontend/imagen-asocolgi/` antes de inventarse colores.
2.  **Cero Colores Crudos:** Prohibido usar `Colors.red` o `Colors.blue` genéricos de Flutter. Se deben definir paletas HEX con colores armoniosos, modos oscuros elegantes y fondos con desenfoque (Glassmorphism) si es aplicable.
3.  **Micro-interacciones (Dynamic Design):**
    *   Los botones deben tener efectos al hacer Hover (pasar el ratón por encima) o Tap.
    *   Los menús laterales (como el Drawer de Spec 02 y 03) deben entrar con transiciones suaves, no de golpe.
    *   Los textfields (como el de comentarios) deben animar su crecimiento.
4.  **No usar "Placeholders" feos:** Si falta un dato, mostrar estados vacíos (Empty States) hermosos con íconos, en lugar de pantallas blancas rotas.
5.  **Tipografía:** Usar fuentes modernas (Google Fonts como Inter, Roboto o Outfit) en lugar de la fuente por defecto del sistema. Crear una jerarquía visual clara (Títulos grandes, subtítulos grises tenues).

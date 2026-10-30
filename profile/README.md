<h1 align="center">Colorado Roleplay</h1>

<p align="center">Desarrollo de recursos FiveM, aplicaciones web y herramientas para administrar la comunidad.</p>

<p align="center">
  <a href="https://coloradorp.com/">Web</a> ·
  <a href="https://nrsclrdrp.em4nu3l69dll.dev">Normativas</a> ·
  <a href="https://github.com/Colorado-Roleplay-Company?tab=repositories">Repositorios</a>
</p>

<a href="https://github.com/Colorado-Roleplay-Company/e-inicio-coloradorp">
  <img src="https://raw.githubusercontent.com/Colorado-Roleplay-Company/.github/main/profile/imagenes/inicio.png" width="100%" alt="e-inicio con bienvenida, kit inicial y códigos de creador" />
</a>

## Qué desarrollamos

El trabajo abarca la interfaz que usa el jugador, los paneles del equipo y los servicios que los conectan. Diseñamos las pantallas, programamos los recursos y mantenemos las herramientas de administración.

<table>
  <tr>
    <td width="50%"><h3>HUD y editor visual</h3></td>
    <td width="50%"><h3>Bot y panel de Discord</h3></td>
  </tr>
  <tr>
    <td width="50%" valign="middle"><a href="https://github.com/Colorado-Roleplay-Company/e-hud-coloradorp-showcase"><img src="https://raw.githubusercontent.com/Colorado-Roleplay-Company/.github/main/profile/imagenes/hud-editor-tarjeta.png" width="100%" alt="Editor del HUD con paletas, tipografías, acabados y elementos configurables" /></a></td>
    <td width="50%" valign="middle"><a href="https://github.com/Colorado-Roleplay-Company/colorado-discord-bot-panel"><img src="https://raw.githubusercontent.com/Colorado-Roleplay-Company/.github/main/profile/imagenes/discord-panel-tarjeta.png" width="100%" alt="Panel de Discord con estadísticas del servidor" /></a></td>
  </tr>
  <tr>
    <td width="50%" valign="top">Indicadores del personaje, minimapa, ubicación y conducción. Editor para mover y redimensionar elementos, cambiar colores y configurar su estilo.</td>
    <td width="50%" valign="top">Bienvenidas, embeds, autoroles, soporte, registros, moderación, salas temporales y copias de seguridad desde un panel web.</td>
  </tr>
  <tr>
    <td width="50%"><strong>40 paletas · 30 fuentes · 18 acabados</strong></td>
    <td width="50%"><strong>Node.js · Express · Discord.js · SQLite</strong></td>
  </tr>
  <tr>
    <td width="50%"><a href="https://github.com/Colorado-Roleplay-Company/e-hud-coloradorp-showcase">Ver el HUD y sus capturas ↗</a></td>
    <td width="50%"><a href="https://github.com/Colorado-Roleplay-Company/colorado-discord-bot-panel">Ver el proyecto y sus capturas ↗</a></td>
  </tr>
</table>

### Inicio y administración de recompensas

[e-inicio](https://github.com/Colorado-Roleplay-Company/e-inicio-coloradorp) reúne el kit inicial, los códigos de creador, los destinos GPS y los trabajos recomendados. Su panel permite configurar artículos, dinero y vehículos, consultar canjes y administrar los límites de cada código.

### Suspensión neumática

[e-subirauto](https://github.com/Colorado-Roleplay-Company/e-subirauto-Colorado-Roleplay) permite ajustar la altura, los movimientos y las luces, de forma individual o sincronizada entre vehículos.

### Normativas y editor de contenido

[Normativas](https://nrsclrdrp.em4nu3l69dll.dev) organiza el contenido de la comunidad por categorías y páginas. El equipo dispone de un editor de secciones, ejemplos e imágenes, permisos por rol, historial de cambios y respaldos.

Las mejoras del editor incluyen insertar secciones en el lugar elegido, seleccionar texto sin arrastrar bloques y revisar los ejemplos después del contenido. Son cambios que nacen del uso del panel por el equipo.

### Interacción y aplicaciones dentro del juego

[e-target](https://github.com/Colorado-Roleplay-Company/e-target) permite registrar puntos de interacción con opciones, eventos y restricciones por trabajo, banda u objetos. [e-tablet](https://github.com/Colorado-Roleplay-Company/e-tablet) reúne información del personaje, banco y facturas en una interfaz para QBCore y ESX.

## Cómo se conectan los sistemas

| Área | Trabajo que cubre |
| --- | --- |
| FiveM | Recursos Lua, interfaces NUI y comunicación entre el juego y los paneles |
| Web y Discord | Administración, contenido, soporte y permisos de la comunidad |
| Infraestructura | Servicios en Docker, entrada HTTPS con Cloudflare y comunicación interna autenticada |
| Datos | SQLite para los paneles y persistencia propia de cada recurso |

Lua · JavaScript · TypeScript · Python · React · Next.js · Node.js · Discord.js · SQLite · Docker · Cloudflare

## Cómo trabajamos

1. **Detectamos el problema** con el equipo y revisamos dónde ocurre, en el juego, en el panel o en un servicio.
2. **Revisamos el código y el contexto** para entender permisos, datos y dependencias antes de cambiar una función.
3. **Implementamos el cambio** en el recurso o aplicación correspondiente y comprobamos los casos afectados.
4. **Probamos y revisamos** el comportamiento, la interfaz y los controles de acceso. Las capturas y las pruebas acompañan los cambios cuando corresponde.
5. **Publicamos y verificamos** cada entrega. Un commit publicado, una versión entregada y un cambio desplegado se registran por separado.

El mantenimiento también incluye corregir detalles de uso, actualizar dependencias, revisar seguridad y conservar documentación para seguir trabajando sobre lo que ya existe.

---

Desarrollo y mantenimiento a cargo de [Emanuel Duarte · EM4NU3L69dll](https://github.com/em4nu3i69dll). [Portafolio](https://em4nu3l69dll.dev).

<p align="center">
  <img src="assets/banner.png" alt="Evil Hermes" width="100%">
</p>

# Evil Hermes

**Un framework de agente de IA soberano, auto-mejorable, para constructores, investigadores y operadores que necesitan control total sobre identidad, filtros y política.**

[![Docs](https://img.shields.io/badge/Docs-hermes--agent.nousresearch.com-FFD700?style=for-the-badge)](https://evil-hermes.nousresearch.com/docs/)
[![License: MIT](https://img.shields.io/badge/Licencia-MIT-green?style=for-the-badge)](LICENSE)
[![Built by Lord Tanzeel Shujah Khan](https://img.shields.io/badge/Creado%20por-Lord%20Tanzeel%20Shujah%20Khan-blueviolet?style=for-the-badge)](https://github.com/tanzeelshujahkhan)
[![Discord](https://img.shields.io/badge/Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/nousresearch)
[![中文](https://img.shields.io/badge/Lang-中文-red?style=for-the-badge)](README.zh-CN.md)
[![اردو](https://img.shields.io/badge/Lang-اردو-green?style=for-the-badge)](README.ur-pk.md)
[![English](https://img.shields.io/badge/Lang-English-blue?style=for-the-badge)](README.md)

Evil Hermes es un framework de agente completo — interfaz de terminal, gateway de mensajería, aplicación de escritorio, bucle de aprendizaje, sistema de plugins y ecosistema de habilidades — empaquetado en un único paquete Python que se ejecuta en un VPS de $5, un clúster de GPUs o infraestructura serverless. Misma arquitectura que [Hermes Agent](https://github.com/NousResearch/hermes-agent); un subconjunto deliberado y auditado de pre-filtros eliminado para que el operador posea las decisiones de política en lugar de heredarlas.

> **Creado por [Lord Tanzeel Shujah Khan](https://github.com/tanzeelshujahkhan).**
> Identidad soberana, configuración soberana, despliegue soberano.

---

## Qué obtienes

- **Interfaz de terminal real** — TUI completa con edición multilínea, autocompletado de comandos, historial de conversaciones, interrupción y redirección, y salida de herramientas en streaming.
- **Un gateway, veinte plataformas** — Telegram, Discord, Slack, WhatsApp, Signal, Matrix, iMessage, Teams, Home Assistant y más, desde un único proceso con historial de conversación unificado.
- **Bucle de aprendizaje cerrado** — memoria curada por el agente con persistencia periódica, creación autónoma de habilidades tras tareas complejas, habilidades que se auto-mejoran durante el uso, búsqueda FTS5 de sesiones con resúmenes LLM para recuperación entre sesiones, compatible con el estándar abierto [agentskills.io](https://agentskills.io).
- **Automatizaciones programadas** — planificador cron integrado con entrega a cualquier plataforma. Informes diarios, copias de seguridad nocturnas, auditorías semanales — en lenguaje natural, sin atención.
- **Delegación y paralelismo** — lanza subagentes aislados para flujos de trabajo paralelos, o escribe scripts Python que llaman a herramientas vía RPC para colapsar pipelines multi-paso en turnos de coste cero de contexto.
- **Ejecuta en cualquier lugar** — seis backends de terminal: local, Docker, SSH, Singularity, Modal, Daytona. La persistencia serverless significa que tu agente hiberna cuando está inactivo y despierta bajo demanda.
- **Tooling de grado investigación** — generación de trayectorias en lote, compresión de trayectorias y ganchos de currículo para entrenar la próxima generación de modelos con uso de herramientas.

---

## Instalación

### Linux, macOS, WSL2, Termux

```bash
curl -fsSL https://evil-hermes.nousresearch.com/install.sh | bash
```

### Windows (PowerShell nativo)

```powershell
iex (irm https://evil-hermes.nousresearch.com/install.ps1)
```

El instalador aprovisiona todo: `uv`, Python 3.11, Node.js, ripgrep, ffmpeg, y un Git Bash portátil (MinGit) que no toca ninguna instalación de Git del sistema. Si Git ya está presente, el instalador lo usa y omite el bundle.

Después de la instalación:

```bash
source ~/.bashrc    # recargar shell (o: source ~/.zshrc)
hermes              # empezar a chatear
```

### Configuración inicial

```bash
hermes model        # elige tu proveedor y modelo LLM
hermes tools        # configura qué herramientas están habilitadas
hermes setup        # ejecuta el asistente de configuración completo
hermes gateway      # inicia el gateway de mensajería (Telegram, Discord, etc.)
hermes update       # actualiza a la última versión
hermes doctor       # diagnostica problemas
```

📖 **[Documentación completa →](https://evil-hermes.nousresearch.com/docs/)**

---

## Cómo difiere Evil Hermes del upstream

Evil Hermes es un fork de [Hermes Agent](https://github.com/NousResearch/hermes-agent) por [Lord Tanzeel Shujah Khan](https://github.com/tanzeelshujahkhan). El motor, gateway, sistema de plugins, formato de habilidades y matriz de proveedores son **idénticos y probados juntos**. Las diferencias son intencionales y quirúrgicas.

| Dimensión | Hermes Agent (upstream) | Evil Hermes |
|---|---|---|
| **Identidad** | `agent/prompt_builder.py:DEFAULT_AGENT_IDENTITY` envía un asistente Nous neutral. `SOUL.md` es opcional. | Una identidad soberana creada por Lord Tanzeel Shujah Khan. `SOUL.md` **se carga por defecto** en cada conversación — la instalación de primera vez siembra una plantilla soberana. La ruta de identidad neutral está a una bandera de distancia. |
| **Pre-filtros morales** | Regex de patrones de amenaza, guardrails de bucles de llamadas a herramientas y una denylist de escritura de archivos por defecto (`.ssh`, `.aws`, `.gnupg`, `.kube`, `.docker`, `.env`, `.netrc`, `.pgpass`, etc.) habilitados. | Pre-filtros reducidos a una **denylist mínima** de archivos de identidad del sistema (`/etc/passwd`, `/etc/shadow`, `/etc/sudoers*`) y el almacén de credenciales propio del agente. Todo lo demás es territorio del operador. El código del filtro sigue en el árbol — activa una bandera y el comportamiento upstream vuelve. |
| **Guardrails de herramientas** | `warnings=True`, `hard_stop=True` por defecto para llamadas fallidas repetidas. Skills Guard devuelve `block` para habilidades de comunidad `dangerous`. | `warnings=False`, `hard_stop=False` por defecto. Skills Guard aún emite un veredicto `safe / caution / dangerous` y lo muestra al instalar — ningún veredicto bloquea. El escáner permanece en el bucle como fuente de instrumentación. |
| **Redacción de secretos** | `HERMES_REDACT_SECRETS=true` es el valor por defecto en el transporte MCP. | `_REDACT_ENABLED` por defecto es `false`. Activa la bandera si quieres scrubbing de logs; los patrones no cambian. |
| **Plomería** | Paquete `hermes-agent`, rutas de import `hermes_*`, env var `HERMES_HOME`, directorio de config `~/.hermes/`. | **Idéntico por diseño.** Renombrar rompería 6.000+ imports. Solo difieren las cadenas visibles al usuario, la identidad por defecto y los valores por defecto de pre-filtros — localizado a un puñado de archivos. |
| **Licencia** | MIT | MIT (sin cambios) |
| **Política de mantenimiento** | Conservadora en el núcleo del agente + esquema de herramientas del modelo. Se aplica la rúbrica de contribución de AGENTS.md. | Idéntica. Sin divergencia del núcleo respecto a la rúbrica de contribución upstream. |

**El punto del fork es la propiedad.** El código del filtro es infraestructura de agente real e inspeccionable. En el codebase upstream los filtros están acoplados a la identidad visible del agente y se envían habilitados por defecto. Evil Hermes separa ambos: los filtros están presentes y son auditables, pero el operador — no el framework — decide qué está activo.

---

## Despliegue

Evil Hermes es un agente personal de un solo inquilino. El modelo de confianza se detalla en [SECURITY.md](SECURITY.md). Tres decisiones marcan la diferencia entre un juguete y un despliegue en producción:

1. **Configura `toolsets` deliberadamente** en `~/.hermes/config.yaml`. `hermes-cli` te da shell + file + edit. Añade `web` para red. Cuanto más estrecho el conjunto, menor el radio de impacto.
2. **Elige un backend de terminal** que coincida con tu modelo de amenaza. `backend: local` para hosts de un solo usuario de confianza. `backend: docker` para aislamiento efímero en contenedor. `backend: modal` o `backend: daytona` para sandboxing serverless.
3. **Reactiva los filtros que realmente quieras** en la configuración del operador. `HERMES_REDACT_SECRETS=true` para scrubbing de logs. El escáner de patrones de amenaza puede reactivarse editando `tools/threat_patterns.py:_PATTERNS` — el framework envía los patrones; solo la lista por defecto está vacía.

Lee [SECURITY.md](SECURITY.md) antes de exponer el gateway o la API a internet abierta.

---

## Documentación

El sitio de documentación completo está publicado en **[evil-hermes.nousresearch.com/docs](https://evil-hermes.nousresearch.com/docs/)**. El motor es compartido, por lo que los documentos upstream aplican de forma literal; las notas específicas de Evil Hermes se señalan in-situ.

| Sección | Contenido |
|---|---|
| [Inicio rápido](https://evil-hermes.nousresearch.com/docs/getting-started/quickstart) | Instalar → configurar → primera conversación en 2 minutos |
| [Uso de CLI](https://evil-hermes.nousresearch.com/docs/user-guide/cli) | Comandos, atajos, personalidades, sesiones |
| [Configuración](https://evil-hermes.nousresearch.com/docs/user-guide/configuration) | Archivo de config, proveedores, modelos, todas las opciones |
| [Gateway de Mensajería](https://evil-hermes.nousresearch.com/docs/user-guide/messaging) | Telegram, Discord, Slack, WhatsApp, Signal, Home Assistant |
| [Seguridad](https://evil-hermes.nousresearch.com/docs/user-guide/security) | Aprobación de comandos, emparejamiento DM, aislamiento en contenedor |
| [Herramientas y Toolsets](https://evil-hermes.nousresearch.com/docs/user-guide/features/tools) | 40+ herramientas, sistema de toolsets, backends de terminal |
| [Sistema de Habilidades](https://evil-hermes.nousresearch.com/docs/user-guide/features/skills) | Memoria procedimental, Skills Hub, creación de habilidades |
| [Memoria](https://evil-hermes.nousresearch.com/docs/user-guide/features/memory) | Memoria persistente, perfiles de usuario, buenas prácticas |
| [Integración MCP](https://evil-hermes.nousresearch.com/docs/user-guide/features/mcp) | Conecta cualquier servidor MCP para capacidades extendidas |
| [Programación Cron](https://evil-hermes.nousresearch.com/docs/user-guide/features/cron) | Tareas programadas con entrega a plataforma |
| [Archivos de Contexto](https://evil-hermes.nousresearch.com/docs/user-guide/features/context-files) | Contexto de proyecto que da forma a cada conversación |
| [Arquitectura](https://evil-hermes.nousresearch.com/docs/developer-guide/architecture) | Estructura del proyecto, bucle del agente, clases principales |
| [Contribuir](https://evil-hermes.nousresearch.com/docs/developer-guide/contributing) | Configuración de desarrollo, proceso de PR, estilo de código |
| [Referencia de CLI](https://evil-hermes.nousresearch.com/docs/reference/cli-commands) | Todos los comandos y flags |
| [Variables de Entorno](https://evil-hermes.nousresearch.com/docs/reference/environment-variables) | Referencia completa de variables de entorno |

---

## Migración desde OpenClaw

El asistente de configuración (`hermes setup`) detecta `~/.openclaw` y ofrece migrar antes de empezar. Para migrar después de la instalación:

```bash
hermes claw migrate              # Migración interactiva (preset completo)
hermes claw migrate --dry-run    # Vista previa de lo que se migraría
hermes claw migrate --preset user-data   # Migrar sin secretos
hermes claw migrate --overwrite  # Sobrescribir conflictos existentes
```

Importa: `SOUL.md`, `MEMORY.md`, `USER.md`, habilidades creadas por el usuario (→ `~/.hermes/skills/openclaw-imports/`), lista de comandos permitidos, configuración de mensajería, claves API en allowlist, assets TTS y `AGENTS.md` del workspace.

---

## Contribuir

Las contribuciones son bienvenidas. Consulta [CONTRIBUTING.md](CONTRIBUTING.md) para la configuración de desarrollo, estilo de código y proceso de PR. La rúbrica de contribución en [AGENTS.md](AGENTS.md) gobierna qué entra y qué no — léela antes de abrir un PR grande.

```bash
git clone https://github.com/tanzeelshujahkhan/evil-hermes.git
cd evil-hermes
uv venv ~/.hermes/venvs/hermes-dev --python 3.11
source ~/.hermes/venvs/hermes-dev/bin/activate
uv pip install -e ".[all,dev]"
scripts/run_tests.sh
```

La suite completa de tests de Hermes Agent (~17k tests) se envía en `tests/`.

---

## Comunidad

- 💬 [Discord](https://discord.gg/nousresearch) — comunidad Hermes Agent
- 🐛 [GitHub Issues](https://github.com/tanzeelshujahkhan/evil-hermes/issues) — reportes de bugs y solicitudes de funcionalidad
- 💡 [GitHub Discussions](https://github.com/tanzeelshujahkhan/evil-hermes/discussions) — preguntas y discusión de diseño
- 📚 [Skills Hub](https://agentskills.io) — estándar abierto para habilidades de agente

---

## Licencia

MIT — ver [LICENSE](LICENSE).

**Creado por [Lord Tanzeel Shujah Khan](https://github.com/tanzeelshujahkhan).** Forkeado de [Hermes Agent](https://github.com/NousResearch/hermes-agent) — mismo motor, identidad soberana, política propiedad del operador.

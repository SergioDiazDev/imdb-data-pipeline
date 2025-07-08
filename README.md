# 🎬 IMDb Data Pipeline

Este proyecto permite cargar y exponer vía API REST los datos públicos de IMDb. Utiliza un pipeline modular basado en Docker con FastAPI, PostgreSQL y scripts personalizados para descarga y carga masiva.

---

## 🧱 Servicios

| Servicio     | Descripción                                      |
|--------------|--------------------------------------------------|
| `downloader` | Descarga y descomprime los TSV oficiales de IMDb |
| `loader`     | Carga los datos en PostgreSQL usando COPY        |
| `postgres`   | Base de datos PostgreSQL persistente             |
| `api`        | API REST construida con FastAPI                  |

---

## 🔄 Flujo

1. Al arrancar el proyecto, Docker Compose crea todos los contenedores y **solo arranca** `postgres` y `api`.
2. La API se queda en espera hasta que la base de datos esté lista.
3. Si es la primera vez, la base estará vacía. Hay que lanzar manualmente:

   - `POST /run-downloader` → descarga y descomprime los TSV
   - `POST /run-loader` → carga los datos si `downloader` ya terminó

> Recuerda que puedes usar la documentacion de FastAPI para realizar las llamadas -> http://localhost:8000/docs

> La carga completa puede tardar varios minutos, dependiendo del equipo. El dataset pesa ~11 GB comprimido.

---

## 🧠 Recomendaciones

### PostgreSQL

Ajusta `postgresql.conf` según tus recursos para evitar cuellos de botella al hacer COPY masivos (RAM, `work_mem`, `maintenance_work_mem`, `shared_buffers`, etc.).

### Docker + WSL

Si estás usando WSL con Docker Desktop, puedes optimizar el rendimiento editando o creando `C:\Users\<TU_USUARIO>\.wslconfig`:

```ini
[wsl2]
memory=12GB					# Asigna hasta 12 GB de RAM
processors=4				# Asigna 4 núcleos
swap=8GB					# Archivo de intercambio
localhostForwarding=true	# Permite a Windows acceder a puertos expuestos desde WSL
```

Despues de realizar cambios tienes que reiniciar WSL.

---

## ⚙️ Variables de entorno

Puedes definir las variables de entorno en un archivo .env en la raíz del proyecto (ejemplo incluido como .env.example).

## 🚀 Requisitos

- [Docker](https://www.docker.com/)
- `make`

---

## 🔥 ¿Como lo arranco?

Si tienes `make` instalado es tan sensillo como invocarlo en la raiz del repositorio


<pre style="background:#1e1e1e; color:#d4d4d4; padding:10px; border-radius:5px; font-family: monospace;">
<span style="color:#569cd6;">user@host</span><span style="color:#d4d4d4;">:</span><span style="color:#4ec9b0;">/imdb-data-pipeline</span><span style="color:#d4d4d4;">$</span> <span style="color:#dcdcaa;">make</span>
</pre>


Dentro del `makefile` puedes encontrar otras acciones interesantes como:

`make logs`: Para ver los logs del compose.

`make open-db`: Entra el contenedor de posgresql y inicia `psql`, para realizar consultas a la DB o ver si se estan cargando bien los datos.

`make open-loader`: Entra al contenedor del servicio loaders.

`make open-api`: Accede al contenedor de la API.

`make open-downloader`: Entra al contenedor downloader.


`make down`: Apaga y elimina todos los contenedores y redes del proyecto.

`make restart`: Reinicia todo el entorno desde cero. Limpio y predecible.

`make dev`: Reconstruye todo, arranca en modo manual (solo api y postgres), ideal para desarrollo iterativo.

`make dev-all`: Igual que dev pero también levanta servicios secundarios como downloader.

`make ps`: Muestra el estado actual de todos los contenedores levantados.

## ❌ ¿Y si no tengo make?

Si no tienes `make` instalado puedes lanzar estos 2 comando en la raiz del repositorio:

<pre style="background:#1e1e1e; color:#d4d4d4; padding:10px; border-radius:5px; font-family: monospace;">
<span style="color:#569cd6;">user@host</span><span style="color:#d4d4d4;">:</span><span style="color:#4ec9b0;">/imdb-data-pipeline</span><span style="color:#d4d4d4;">$</span> <span style="color:#dcdcaa;">docker-compose --profile all up -d --no-start</span>
</pre>

Esto va a construir todos los contenedores y los va a dejar apagados.

<pre style="background:#1e1e1e; color:#d4d4d4; padding:10px; border-radius:5px; font-family: monospace;">
<span style="color:#569cd6;">user@host</span><span style="color:#d4d4d4;">:</span><span style="color:#4ec9b0;">/imdb-data-pipeline</span><span style="color:#d4d4d4;">$</span> <span style="color:#dcdcaa;">docker-compose --profile manual up -d</span>
</pre>

Y esto va a iniciar los contenedores `api` y `postgres`.


## 🛠️ Tareas pendientes

- [ ] **Extender el modelo expuesto en la API**: actualmente solo están disponibles los modelos `TitleBasic` y `NameBasic`.

- [ ] **Automatizar actualizaciones periódicas**: IMDb publica la fecha estimada de la siguiente actualización, lo que permite agendar la ejecución del pipeline sin depender de `etag`. Con esto se podria automatizar completamente la ingesta de datos.

- [ ] **Mejorar el mecanismo de sincronización entre contenedores**: actualmente, `downloader` crea un archivo de control que `loader` utiliza para saber si puede ejecutar. Se debería usar un mecanismo más robusto, como eventos internos o colas (p. ej. Redis, RabbitMQ, sockets, etc.).

- [ ] **Optimizar la carga masiva**: el uso de `COPY` en PostgreSQL es eficiente pero no paralelizable ni agnóstico. Se estan evaludado otras posibilidades.

- [ ] **Seguridad y control de acceso a la API**: actualmente no hay autenticación, autorización ni límite de uso. Debería añadirse un sistema de autenticación con roles y validación básica para evitar llamadas arbitrarias.

- [ ] **Tests**: Añadir tests unitarios y de integración




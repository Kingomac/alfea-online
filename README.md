<h1 style="text-align:center;">Alfea Online</h1>



Se puede jugar en http://5.250.186.182:8000

## Desarrollo

Se requiere el siguiente software:

- Python 3.12
- Node.js 20
- Redis

Se recomienda utilizar Docker con la siguiente configuración:

- Redis: ejecutar un contenedor con la [imagen oficial de Redis](https://hub.docker.com/_/redis). Recuerda que debes crear una red y añadir tanto este contenedor como el del devcontainer para poder acceder mediante el nombre.

```shell
$ docker network create als
$ docker run -d --name redis --network als redis:latest
```

- Devcontainer: ejecutar el IDE en un contenedor de desarrollo permite trabajar con las versiones adecuadas sin necesidad de instalar nada más que Docker en tu equipo. Su configuración se encuentra en `.devcontainer/devcontainer.json` y se pueden usar con Visual Studio Code o editor de código que los soporte. En este caso, contiene Node.js y Python y se deben ejecutar los siguientes comandos, en dos terminales separadas, para iniciar el servidor de [Tailwind](https://tailwindcss.com/) (framework de CSS) y la aplicación Flask.

Para agregar el devcontainer a la red creada anteriormente:
```shell
$ docker ps
$ docker network connect als <devcontainer>
```

Ejecutar entorno de desarollo:

```shell
$ npm install # Instalar dependencias de Node.js
$ pip install -r requirements.txt # Instalar dependencias de Python
$ npm run dev # Generar CSS de Tailwind
$ python main.py # Servidor de desarrollo en 127.0.0.1:5000
```

Importante: la configuración de conexión de la base de datos se encuentra en `db/db.py` y actualmente se conecta a un contenedor llamado `redis`, por tanto si utilizas otro método de instalación de Redis u otra configuración, los datos conexión podrían cambiar.

## Producción

Se incluye un fichero  `docker-compose.yml` que inicia un contenedor con Redis y otro con la aplicación en modo producción con el servidor Gurnicorn, uno de los [recomendado en la documentación de Flask](https://flask.palletsprojects.com/en/3.0.x/deploying/). La web sería accesible desde el puerto 8000.

```shell
$ docker-compose up -d
```

Se requiere que el CSS de Tailwind haya sido generado en modo producción desde el entorno de desarrollo con el comando `npm run build`.

> En el zip se incluye el CSS generado, por tanto se puede iniciar directamente con Docker

# Diagrama de clases

![](docs/diagrama-clases.svg)



# Diagramas de secuencia

## Lobby de combate

![](docs/diagrama-secuencia-lobby-raid.svg)

## Combate

![](docs/diagrama-secuencia-combate.svg)

# Diagrama de flujo

Se decidió incluir un diagrama de flujo adicional, puesto que, se adecua a la funcionalidad de combate implementada en el proyecto.

![](docs/diagrama-flujo-combate.svg)
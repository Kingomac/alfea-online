# Alfea Online

Alfea Online es un juego de combate por turnos multijugador basado en el mundo de la serie Winx Club.

## Desarrollo

Se requiere el siguiente software:

- Python 3.12
- Node.js 20
- Redis

Se recomienda utilizar Docker con la siguiente configuración:

- Redis: ejecutar un contenedor con la [imagen oficial de Redis](https://hub.docker.com/_/redis).

```shell
$ docker run -d --name redis redis:latest
```

- Devcontainer: ejecutar el IDE en un contenedor de desarrollo permite trabajar con las versiones adecuadas sin necesidad de instalar nada más que Docker en tu equipo. Su configuración se encuentra en `.devcontainer/devcontainer.json` y se pueden usar con Visual Studio Code o editor de código que los soporte. En este caso, contiene Node.js y Python y se deben ejecutar los siguientes comandos, en dos terminales separadas, para iniciar el servidor de [Tailwind](https://tailwindcss.com/) (framework de CSS) y la aplicación Flask.

```shell
$ npm install # Instalar dependencias de Node.js
$ pip install -r requirements.txt # Instalar dependencias de Python
$ npm run dev # Generar CSS de Tailwind
$ python main.py # Servidor de desarrollo en 127.0.0.1:5000
```

## Producción

Se incluye un fichero  `docker-compose.yml` que inicia un contenedor con Redis y otro con la aplicación en modo producción con el servidor Gurnicorn, uno de los [recomendado en la documentación de Flask](https://flask.palletsprojects.com/en/3.0.x/deploying/). La web sería accesible desde el puerto 8000.

```shell
$ docker-compose up -d
```

Se requiere que el CSS de Tailwind haya sido generado en modo producción desde el entorno de desarrollo con el comando `npm run build`.

> En el zip se incluye el CSS generado, por tanto se puede iniciar directamente con Docker

# Diagrama de clases

![](docs/diagrama-clases.svg)



# Combate

## Diagrama de secuencia	

```mermaid
sequenceDiagram
	actor Jugador 1
	actor Jugador 2
	participant U as UI
	participant S as Servidor
	participant R as Redis
	
	U->>S: empezarCombate()
	
	loop Hasta que todos los jugadores de héroes o villanos mueran
        S->>U: nuevoTurno()
        activate S
        par Mostrar selector de ataques
            U->>Jugador 1: mostrarSelectorAtaques(ataquesJ1)
            activate U
            U->>Jugador 2: mostrarSelectorAtaques(ataquesJ2)
        and Jugador 1 elige su ataque
            Jugador 1-->>U: ataqueJ1
            U-->>S: J1 selecciona ataqueJ1
            S->>R: guardarAtaqueTurno(J1,ataqueJ1)
            S->>S: comprobarTodosHanAtacado() -> False
        and Jugador 2 elige su ataque
            Jugador 2-->>U: ataqueJ2
            deactivate U
            U-->>S: J2 selecciona ataqueJ2
            deactivate S
            S->>R: guardarAtaqueTurno(J2,ataqueJ2)
            S->>S: comprobarTodosHanAtacado() -> True
        end
      
        S->>R: obtenerCombate(idCombate)
        activate R
        R-->>S: estadoCombate
        deactivate R
        loop Para cada ataque
        	S->>S: calcularEscudos(ataque)
        	S->>S: calcularDaño(ataque)
        end
        S->>R: guardarCombate(idCombate,estadoCombate)
        S->>U: mostrarTurno(estadoCombate)

        par Mostrar resultado del turno
        U->>Jugador 1: mostrarTurno(estadoCombate)
        U->>Jugador 2: mostrarTurno(estadoCombate)
        end
       end
	S->>S: determinarBandoGanador()
	S->>U: mostrarGanador(bando)
	par Mostrar resultado
		U->>Jugador 1: mostrarGanador(bando)
		U->>Jugador 2: mostrarGanador(bando)
	end
	S->>S: determinarRecompensas()
	S->>R: guardarRecompensas(recompensas)
	S->>R: borrarCombate(combate)
	
```

## Diagrama de flujo

![](docs/diagrama-flujo-combate.svg)
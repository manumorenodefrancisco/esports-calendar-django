# Proyecto
La idea es la siguiente:
En la entidad Usuario se guardan los datos de los usuarios registrados y el token necesario para recibir notificaciones.
Una vez autenticado, puede consultar los Eventos, que se almacenan en la base de datos (en Events) tras obtenerse de la API externa de esports PandaScore.
Cuando el usuario se suscribe a un evento, se crea un registro en la entidad Suscripción, que relaciona al Usuario con el Evento y guarda el tipo de recordatorio seleccionado.
A partir de sus suscripciones, el sistema puede generar o actualizar sus Preferencias, calculando automáticamente qué videojuegos o tipos de eventos le interesan más.
En segundo plano, un proceso automático (cron, Celery, scheduler…) revisa periódicamente los eventos que empiezan en 1 hora. Busca usuarios suscritos a esos eventos y si los 
detecta, les envía una push notification utilizando la información almacenada en la entidad Usuario.

## API PandaScore

La API de PandaScore te da un access_token para poder acceder a los datos, ese token lo enviamos en cada petición configurando en ella un header HTTP de autorización con el 
valor ‘Bearer <token>’, aunque también podríamos pasárselo a la API en un parámetro en la propia url del GET.

- Hay un endpoint en PandaScore que obtiene las últimas incorporaciones y que solo muestra objetos sin cambios (url/additions), otro para los ultimos cambios de un objeto 
    (/changes), otro para datos eliminados (/deletions) y otro para incidentes, que este es el que vamos a usar porque con un get listas los 3 juntos, (todos los cambios,
    adiciones o borrados). Así solo haces 1 petición y luego detectas el tipo de incidente y actualizas tu entidad Evento. Endpoint: https://api.pandascore.co/incidents.
- El endpoint que usaremos para traernos los partidos será: 'https://api.pandascore.co/matches?filter[status]=running,not_started&sort=begin_at'
      Este endpoint trae todos los partidos en directo o que se acercan a empezar ordenándolos por fecha de inicio cercana, e ignorara los que ya han terminado ya que 
    sobrecargaría la petición y PandaScore solo te trae 50-100 elementos por petición.
- Otra peticion que haremos es al endpoint 'https://api.pandascore.co/matches/past?range[end_at]=one_hour_ago,NOW' donde esas dos variables las calcularemos 
    desde django con datetime y timedelta, siendo NOW la hora actual y one_hour_ago igual a NOW-60min.
- Por último, se hará una petición a 'https://api.pandascore.co/matches/{id}' para traer el estado de un partido en particular.

## Interfaz de Usuario y Visualización

La idea es mostrar los matches en el calendario de forma que al pinchar en un día del calendario se abra un recyclerview con todos los matches de ese día, cada uno con el 
nombre completo del match, tournament, league y serie al que pertenece. Al pinchar en el match, se abrirá un pequeño popup o un AlertDialog de detalle que mostrará la misma 
tarjeta pero con un poco más de información llamando al endpoint endpoint 'GET url/matches/{id}' que a continuación pongo.

### Datos de la tarjeta (RecyclerView)
Los datos que se mostrarán en cada tarjetita de match del recyclerview al pinchar en un día del calendar serán:
- scheduled_at
- league.name
- tournament.name
- serie.full_name
- opponents[].name
- opponents[].image_url
- match_type
- number_of_games
- status
- videogame.name

### Datos del detalle (Popup/AlertDialog) -> 'GET url/matches/{id}'
Los datos que se mostrarán en el detalle de match al pinchar en una tarjetita de match del recyclerview serán los mismos que antes (se pueden reutilizar de la bbdd), pero además habrá:
- results[] (donde cada elemento del array es un diccionario con team_id y winner_id de claves)
- winner_id
- streams_list[] (donde nos interesa su raw_url, mostraremos los 5 primeros enlaces -> streams_list[0].raw_url…….. streams_list[4].raw_url)

> **Nota:** Algunos datos como opponents[] o results[] pueden llegar vacíos, y otros como winner_id pueden llegar null. Hay que saber manejar esos casos.

## Ejemplo de Estructura JSON (Match)

Estos son los datos que nos interesan que vienen de un match de ejemplo (https://api.pandascore.co/matches/636351) traído de la api, cada match tiene muchos más datos en su estructura json 
pero solo nos interesan estos:

```json
{
    "scheduled_at": "2022-06-24T22:00:00Z",
    "league": {
        "name": "LEC"
    },
    "tournament": {
        "name": "Regular Season"
    },
    "serie": {
        "full_name": "Summer 2022"
    },
    "opponents": [
        {
            "opponent": {
                "id": 126536,
                "name": "Movistar KOI",
                "image_url": "https://cdn-api.pandascore.co/images/team/image/126536/movistar_ko_ilogo_square.png"
            }
        },
        {
            "opponent": {
                "id": 394,
                "name": "Fnatic",
                "image_url": "https://cdn-api.pandascore.co/images/team/image/394/220px_fnaticlogo_square.png"
            }
        }
    ],
    "match_type": "best_of",
    "number_of_games": 1,
    "status": "finished",
    "results": [
        {
            "team_id": 126536,
            "score": 1
        },
        {
            "team_id": 394,
            "score": 0
        }
    ],
    "videogame": {
        "name": "LoL",
    },
    "winner_id": 126536,
    "streams_list": [
        {
            "language": "en",
            "raw_url": "https://www.twitch.tv/lec"
        }
    ]
}

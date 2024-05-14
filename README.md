# Trabajo Práctico 3

1. [Kafka + Druid + Superset](#Kafka + Druid + Superset)

## Kafka + Druid + Superset

Lo primera que vamos a hacer es crear un script en Python [visualize.py](./visualize.py) que nos permita, usando pyarrow, obtener el esquema del fichero Flights.parquet y entender su contenido.
```bash
$ ./visualize.py
Esquema del archivo Parquet:
FL_DATE: date32[day]
DEP_DELAY: int16
ARR_DELAY: int16
AIR_TIME: int16
DISTANCE: int16
DEP_TIME: float
ARR_TIME: float

Primeras filas del contenido del archivo Parquet:
      FL_DATE  DEP_DELAY  ARR_DELAY  AIR_TIME  DISTANCE   DEP_TIME   ARR_TIME
0  2006-01-01          5         19       350      2475   9.083333  12.483334
1  2006-01-02        167        216       343      2475  11.783334  15.766666
2  2006-01-03         -7         -2       344      2475   8.883333  12.133333
3  2006-01-04         -5        -13       331      2475   8.916667  11.950000
4  2006-01-05         -3        -17       321      2475   8.950000  11.883333
```

Transformamos el fichero Flights.parquet a un fichero Flights.json con el script [parq2json.py](./parq2json.py)

Se ha creado un fichero compose único [docker-compose.yaml](./docker-compose.yaml) que define un clúster Kafka (bitnami/kafka y bitnami/zookeeper), un productor que genera eventos de topic "My_Topic" extraídos de Flights.json, un servidor Druid y un servidor Superset, todos ellos conectados a una red llamada kafka-net. El productor se construye a partir del fichero [Dockerfile](./Dockerfile), el cual instala las librerías necesarias para ejecutar el script [event_generator.py](./event_generator.py) que envía eventos al topic "My_Topic", utilizando la información del fichero [config.yaml](./config.yaml) para conectarse al servidor Kafka.

![alt text](image.png)


Una vez lanzados los servicios `docker compose up -d`, nos conectamos al contenedor productor y ejecutamos el script [event_generator.py](./event_generator.py) para enviar mensajes al topic flights.
```bash
docker exec -it ipmd-practica3-kafka-python-productor-1 /bin/bash
root@62475ba7b318:/kafka_python# python event_generator.py
```

En este momento, el productor está enviando eventos al topic "My_Topic". Para que estos eventos sean ingeridos por el servidor Druid, nos conectamos al webUI de Druid en http://localhost:8888 y cargamos datos desde kafka:

Seleccionamos la opción "Kafka" y rellenamos los campos con la información necesaria para conectarnos al servidor Kafka y al topic "My_Topic":

![alt text](connect2Druid.png)

![alt text](parse.png)

![alt text](indexacion.png)

![alt text](useearlyoffset.png)

![alt text](statusPending.png)

Una vez cargados los datos, podemos consultarlos en la pestaña "Query" de la tabla "My_Topic" en el datasource "My_Topic", podemos ver como el número de eventos va aumentando:

![alt text](query1.png)

![alt text](query2.png)




Para visualizar los datos en Superset, nos conectamos al webUI de Superset en http://localhost:8088 y creamos un nuevo datasource de tipo "Druid":

![alt text](connexionSuperset.png)

Ahora podemos crear un nuevo dashboard y añadir un gráfico de tipo "Time Series" con los datos de nuestro datasource, tendremos que usar _time como campo temporal y ARR_DELAY como métrica, calculando la media y maximo:

![alt text](supersetchart.png)
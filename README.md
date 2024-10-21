## Monitor JMX

Proyecto para registrar los parametros de memoria de la JVM

### Dependencias del proyecto
- Python 3

### Requisitos para el despliegue
- Docker Compose >=1.29
- Timescale DB >=2.8.1

### Timescale DB

Crear la base de datos
```sql
create user u_monitor_jmx;

CREATE DATABASE monitor_jmx WITH OWNER = u_monitor_jmx;
```
Dentro de la base crear los objetos
```sql
CREATE TABLE htb_memory (
    time TIMESTAMPTZ NOT NULL,
    name VARCHAR NOT NULL,
    value BIGINT NOT NULL
);

ALTER TABLE IF EXISTS htb_memory OWNER to u_monitor_jmx;
-- Convertirla en una hypertabla para particionar por tiempo
SELECT create_hypertable('htb_memory', 'time');
--Politica de retencion
SELECT add_retention_policy('htb_memory', INTERVAL '5 weeks');

--Crear usuario de consulta para Grafana
CREATE ROLE g_monitor_consulta NOSUPERUSER INHERIT NOCREATEDB NOCREATEROLE NOREPLICATION;
GRANT USAGE ON SCHEMA  public TO g_monitor_consulta;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO g_monitor_consulta;

create user u_monitor_consulta with password '***' IN GROUP g_monitor_consulta;
```



### Variables de Entorno
<style>
.table {
    width:100%;
}
.nuevo{
    font-weight: bold;
}
</style>
<table class="table">
  <tr>
    <th>Clave</th>
    <th>Valor</th>
    <th>Ejemplo</th>
  </tr>
  <tr>
    <td>DB_HOST</td>
    <td>Ip de la base de datos Origen</td>
    <td>localhost</td>
  </tr>
  <tr>
    <td>DB_PORT</td>
    <td>Puerto de la base de datos Origen</td>
    <td>50000</td>
  </tr>
  <tr>
    <td>DB_USER</td>
    <td>Nombre de usuario Administrador de la base de datos Origen</td>
    <td>postgres</td>
  </tr>
  <tr>
    <td>DB_PASS</td>
    <td>Contraseña de base de datos Origen</td>
    <td>password</td>
  </tr>
  <tr>
    <td>DB_NAME</td>
    <td>Nombre de la base de datos Origen</td>
    <td>kill_session</td>
  </tr>
</table>


### Complilacion y despliegue

* Crear base de datos en el servidor Origen segun el script origin.sql
* Crear base de datos en el servidor de Monitoreo segun el script monitor.sql
* Clonar este repositorio en un servidor de aplicacion
* Configurar las variables de entorno con el archivo .env
* Configuracion para ejecutar como contenedores:
```
cd app
docker-compose build
#Configurar crontabs para cada monitor y killer:
* * * * ?   cd $PATH  &&  docker-compose run
```

* Configuracion para ejecutar como servicio:
```
mkdir -p /opt/session_manager
cp app  /opt/session_manager
cp .env.example  /opt/session_manager/.env
cd /opt/session_manager && python3.11 -m venv venv
. venv/bin/activate
pip3 install -r requeriments.txt
pip3 list
deactivate
vi /etc/systemd/system/monitor_session.service
[Unit]
Description=Monitor Session service
[Service]
User=carlos
WorkingDirectory=/opt/session_manager/app
EnvironmentFile=/opt/session_manager/.env
ExecStart=/opt/session_manager/venv/bin/python3.11 /opt/session_manager/app/main.py monitor --delay 10 --daemon
# Agrega la siguiente línea para detener el servicio con SIGTERM
ExecStop=/bin/kill -15 $MAINPID
[Install]
WantedBy=multi-user.target

systemctl daemon-reload
```
<img src="documentation/gestor_sesiones.png" width="80%" height="80%">
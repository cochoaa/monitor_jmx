## Monitor JMX

Proyecto para registrar los parametros de memoria de la JVM

### Dependencias del proyecto
- Python 3

### Requisitos para el despliegue
- Docker Compose >=1.29
- Timescale DB >=2.8.1

### Timescale DB

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
    <td>Nombre de la base de datos</td>
    <td>monitor_jmx</td>
  </tr>
    <tr>
    <td>JMX_HOST</td>
    <td>Ip de la base de datos Origen</td>
    <td>chancay.unmsm.edu.pe</td>
  </tr>
  <tr>
    <td>JMX_PORT</td>
    <td>Puerto de la base de datos Origen</td>
    <td>9999</td>
  </tr>
</table>


### Complilacion y despliegue

* Crear la base de datos
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
* Configurar las variables de entorno con el archivo .env
* Crear un usuario en el sistema operativo
```bash
useradd monitor_jmx
```
* Clonar este repositorio en un servidor
```bash
git clone https://github.com/cochoaa/monitor_jmx.git
```
* Configurar para ejecutar como servicio:
```bash
mkdir -p /opt/monitor_jmx
cp -r app  /opt/monitor_jmx
cat <<EOL > /opt/monitor_jmx/.env
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASS=postgres
DB_NAME=monitor_jmx
JMX_HOST=chancay.unmsm.edu.pe
JMX_PORT=9999
EOL
cd /opt/monitor_jmx && python3.11 -m venv venv
cp .credentials.yml.example  credentials.yml
. venv/bin/activate
pip3 install -r app/requirements.txt
pip3 list
deactivate
cat <<EOL > /etc/systemd/system/monitor_jmx.service
[Unit]
Description=Monitor Memory JMX Q20
[Service]
User=monitor_jmx
WorkingDirectory=/opt/monitor_jmx/app
EnvironmentFile=/opt/monitor_jmx/.env
ExecStart=/opt/monitor_jmx/venv/bin/python3.11 /opt/monitor_jmx/app/main.py --daemon
# Agrega la siguiente línea para detener el servicio con SIGTERM
ExecStop=/bin/kill -15 $MAINPID
[Install]
WantedBy=multi-user.target
EOL
chown -R monitor_jmx:monitor_jmx /opt/monitor_jmx
systemctl daemon-reload

```

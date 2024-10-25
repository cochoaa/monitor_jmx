import config.log_config as log_config
import config.parser_config as parser_config
import signal
from config.container import Container
from apscheduler.schedulers.blocking import BlockingScheduler

logger = log_config.getLogger()
container = Container()


def main():
    container.config.from_yaml("./credentials.yml")
    container.wire(modules=[__name__])
    parser = parser_config.getParser()
    args = parser.parse_args()
    logger.info(args)
    if args.check:
        logger.info(f"Revision de configuracion")
        check()
    elif args.daemon:
        interval = args.interval
        print(interval)
        logger.info(f"Iniciando modo daemon")
        daemon(interval)
    else:
        logger.error(f"Comando desconocido")


def check():
    monitor = container.monitor()
    monitor.check()


def daemon(interval: int):
    monitor = container.monitor()
    scheduler = BlockingScheduler()
    scheduler.add_job(monitor.migrate, 'interval', seconds=interval)
    scheduler.start()


def handle_sigterm(signum, frame):
    logger.info(f"Se recibió la señal SIGTERM. Deteniendo el servicio...")
    exit(0)


if __name__ == "__main__":
    main()
    signal.signal(signal.SIGTERM, handle_sigterm)

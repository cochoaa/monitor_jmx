import config.log_config as log_config
import config.parser_config as parser_config
import signal
from config.container import Container

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
    elif args.daemon:
        logger.info(f"Iniciando modo daemon")
    else:
        logger.error(f"Comando desconocido")

def handle_sigterm(signum, frame):
    logger.info(f"Se recibió la señal SIGTERM. Deteniendo el servicio...")
    exit(0)


if __name__ == "__main__":
    main()
    signal.signal(signal.SIGTERM, handle_sigterm)

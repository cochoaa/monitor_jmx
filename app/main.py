import config.log_config as log_config
import config.parser_config as parser_config
from config.container import Container


logger = log_config.getLogger()
container = Container()
def main():
    container.config.from_yaml("./credentials.yml")
    container.wire(modules=[__name__])
    parser = parser_config.getParser()
    args = parser.parse_args()
    logger.info(args)
    if args.check and args.command is None:
        logger.info(f"Revision de configuracion")

    else:
        logger.error(f"Comando desconocido")
if __name__ == "__main__":
    main()

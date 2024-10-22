import argparse
def getParser():
    parser = argparse.ArgumentParser(prog='Session Manager')
    parser.add_argument('--check',action='store_true', help='Revisa la configuracion de los servicios')
    parser.add_argument('--delay', nargs='?', default=5, choices=range(5, 21),
                        help='Definir el intervalo en seguntos entre cada ejecucion del servicio durante 1 minuto',
                        required=True,
                        type=int)
    parser.add_argument('-D', '--daemon', action='store_true', help='Activar ejecucion en segundo plano')
    #__create_base_parser(parser)
    return parser

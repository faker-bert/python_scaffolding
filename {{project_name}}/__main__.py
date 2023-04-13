import argcomplete
import importlib.util
if importlib.util.find_spec('{{project_name}}') is None:
    import sys
    # todo Determine whether the current can be loaded to woflow,
    #  can be packaged into pip packages, there is no need for this
    sys.path.append('../{{project_name}}')

from {{project_name}}.cli.cli_parser import get_parser


def main():
    """Main executable function"""
    parser = get_parser()
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()


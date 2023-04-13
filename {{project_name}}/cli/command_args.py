import argparse
# from {{project_name}}.configuration import conf
# from {{project_name}}.utils.net import getfqdn


class Arg:
    """
    Class to keep information about command line argument

    Encapsulating command line parameters
    """
    def __init__(
            self,
            flags=None,
            action=None,
            help=None,
            nargs=None,
            dest=None,
            type=None,
            default=None,
            choices=None,
            required=None,
            metavar=None,
    ):
        self.flags = flags
        self.kwargs = {}
        for key, value in locals().items():
            if key in ('self', 'flags'):
                continue
            if value:
                self.kwargs[key] = value

    def add_to_parser(self, parser: argparse.ArgumentParser):
        """Add this argument to an ArgumentParser"""
        parser.add_argument(*self.flags, **self.kwargs)
# common
# ARG_DAEMON = Arg(
#     ("-D", "--daemon"), help="Daemonize instead of running in the foreground", action="store_true"
# )
# ARG_LOCAL = Arg(("-l", "--local"), help="Run the task using the LocalExecutor", action="store_true")
# ARG_PID = Arg(("--pid",), help="PID file location", nargs='?')
# ARG_STDERR = Arg(("--stderr",), help="Redirect stderr to this file")
# ARG_STDOUT = Arg(("--stdout",), help="Redirect stdout to this file")
# ARG_LOG_FILE = Arg(("-l", "--log-file"), help="Location of the log file")
# ARG_SKIP_SERVE_LOGS = Arg(
#     ("-s", "--skip-serve-logs"),
#     default=False,
#     help="Don't start the serve celery_logs process along with the workers",
#     action="store_true",
# )
# ARG_DAG_ID = Arg(("dag_id",), help="The id of the dag")
# # webserver
# ARG_PORT = Arg(
#     ("-p", "--port"),
#     default=conf.getint('webserver', 'web_server_port', fallback=8080),
#     type=int,
#     help="The port on which to run the server",
# )
# ARG_HOSTNAME = Arg(
#     ("-H", "--host"),
#     default='0.0.0.0',
#     type=str,
#     help="Set the hostname on which to run the web server",
# )
# # scheduler
# # worker
# ARG_QUEUES = Arg(
#     ("-q", "--queues"),
#     help="Comma delimited list of queues to serve",
#     default=conf.get('celery', 'DEFAULT_QUEUE'),
# )
# ARG_CONCURRENCY = Arg(
#     ("-c", "--concurrency"),
#     type=int,
#     help="The number of worker processes",
#     default=conf.get('celery', 'worker_concurrency'),
# )
# ARG_CELERY_HOSTNAME = Arg(
#     ("-H", "--celery-hostname"),
#     default=getfqdn(),
#     help="Set the hostname of celery worker if you have multiple workers on a single machine",
# )
# # config
# ARG_SECTION = Arg(
#     ("section",),
#     help="The section name",
# )
# ARG_OPTION = Arg(
#     ("option",),
#     help="The option name",
# )
#
# # test
# TEST_ARGS = Arg(('-t', '--test'), help='test args', action='store_true')

from typing import NamedTuple, Iterable, Callable, Union, List, Dict, AnyStr
from {{project_name}}.utils.module_importer import import_string
from argparse import RawTextHelpFormatter
from {{project_name}}.cli.command_args import *


def load_command_action(import_path: str) -> Callable:
    _, _, name = import_path.rpartition('.')

    # 方便给函数命名
    def command_action(*args, **kwargs):
        func = import_string(import_path)
        return func(*args, **kwargs)

    command_action.__name__ = name

    return command_action


class DefaultHelpParser(argparse.ArgumentParser):
    """CustomParser to display help message"""

    def error(self, message):
        """Override error and use print_instead of print_usage"""
        self.print_help()
        self.exit(2, f'\n{self.prog} command error: {message}, see help above.\n')


class GroupCommand(NamedTuple):
    """ClI command with subcommands"""
    name: str
    help: str
    subcommands: Iterable
    description: str or None = None
    epilog: str or None = None


class ActionCommand(NamedTuple):
    """Single CLI command"""

    name: str
    help: str
    func: Callable
    args: Iterable[Arg]
    description: str or None = None
    epilog: str or None = None


CLICommand = Union[ActionCommand, GroupCommand]


CELERY_COMMANDS = [
    ActionCommand(
        name='worker',
        help="Start a Celery worker node",
        func=load_command_action('{{project_name}}.cli.commands.celery_command.worker'),
        args=(
            ARG_QUEUES,
            ARG_CONCURRENCY,
            ARG_CELERY_HOSTNAME,
            ARG_PID,
            ARG_STDOUT,
            ARG_STDERR,
            ARG_LOG_FILE,
            ARG_SKIP_SERVE_LOGS,
            ARG_DAEMON
        )
    ),
    # todo: flower, prometheus, grafana
    ActionCommand(
        name='stop',
        help="Stop the Celery worker gracefully",
        func=load_command_action('{{project_name}}.cli.commands.celery_command.stop_worker'),
        args=(ARG_PID,),
    ),
]


DAG_COMMANDS = [
    ActionCommand(
        name='run',
        help='Run the special dag',
        func=load_command_action('{{project_name}}.cli.commands.dag_command.dag_backfill'),
        args=(
            ARG_DAG_ID,
            ARG_LOCAL
        )
    )
]


CONFIG_COMMANDS = [
    ActionCommand(
        name='get-value',
        help='Print the value of the configuration',
        func=load_command_action('{{project_name}}.cli.commands.config_command.get_config'),
        args=(
            ARG_SECTION,
            ARG_OPTION,
        ),
    ),
]


{{project_name}}_commands: List[CLICommand] = [
    ActionCommand(
        name='webserver',
        help='start webserver instance',
        func=load_command_action('{{project_name}}.cli.commands.webserver_command.webserver'),
        args=(ARG_PORT, ARG_HOSTNAME),
    ),
    ActionCommand(
        name='scheduler',
        help='start scheduler instance',
        func=load_command_action('{{project_name}}.cli.commands.scheduler_command.scheduler'),  # 还需要补充一个属性
        args=(ARG_DAEMON,),
    ),
    # ActionCommand(
    #     name='trigger',
    #     help='start trigger instance',
    #     func=load_command_action('{{project_name}}.cli.commands.trigger_command.demo'),
    #     args=(),
    # ),
    ActionCommand(
        name='standalone',
        help='webserver, scheduler, trigger and worker all-in-one',
        func=load_command_action('{{project_name}}.cli.commands.standalone_command.standalone'),
        args=(),
    ),
    GroupCommand(
        name="celery",
        help='Celery components',
        description=(
            'Start celery components. Works only when using CeleryExecutor. For more information, see '
            'https://airflow.apache.org/docs/apache-airflow/stable/executor/celery.html'
        ),
        subcommands=CELERY_COMMANDS,
    ),
    GroupCommand(name="config", help='View configuration', subcommands=CONFIG_COMMANDS),
    GroupCommand(name='dag', help='Dag support(just for dev)', subcommands=DAG_COMMANDS)
]


ALL_COMMANDS: Dict[AnyStr, CLICommand] = {sp.name: sp for sp in {{project_name}}_commands}


def get_parser() -> argparse.ArgumentParser:
    """
    Takes all references to func by default,
    but only triggers the necessary namespace
    """

    parser = DefaultHelpParser(prog='Woflow', usage='%(prog)s [options]')
    subparsers = parser.add_subparsers(title='subcommands', dest='subcommand')
    subparsers.required = True

    for subprocess, subcommand in ALL_COMMANDS.items():
        subcommand: CLICommand
        # add subcommand to subparser
        _add_command(subparsers, subcommand)

    return parser


def _add_command(subparsers: argparse._SubParsersAction, subcommand: CLICommand) -> None:
    # https://docs.python.org/zh-cn/3/library/argparse.htm
    sub_proc = subparsers.add_parser(
        subcommand.name,
        help=subcommand.help,
        description=subcommand.description or subcommand.help,
        epilog=subcommand.epilog
    )
    sub_proc.formatter_class = RawTextHelpFormatter
    if isinstance(subcommand, GroupCommand):
        _add_group_command(subcommand, sub_proc)
    elif isinstance(subcommand, ActionCommand):
        _add_action_command(subcommand, sub_proc)
    else:
        # raise AirflowException("Invalid command definition.")
        raise Exception


def _add_group_command(sub: GroupCommand, sub_proc: argparse.ArgumentParser):
    subcommands = sub.subcommands
    sub_subparsers = sub_proc.add_subparsers(dest="subcommand", metavar="COMMAND")
    sub_subparsers.required = True

    for command in subcommands:
        _add_command(sub_subparsers, command)


def _add_action_command(sub: ActionCommand, sub_proc: argparse.ArgumentParser):
    for arg in sub.args:
        arg: Arg
        arg.add_to_parser(sub_proc)
        ...
        # todo
    sub_proc.set_defaults(func=sub.func)

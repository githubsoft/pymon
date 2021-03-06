import sys
import os
import argparse
import textwrap
from six.moves import configparser


def parse_settings(argv):
    global settings

    # Read config file
    config = configparser.ConfigParser()
    config_file = os.path.join(os.path.dirname(__file__), "config/settings.cfg")
    config.read(config_file)
    
    # Initiate settings
    settings = dict(config.items("pymon"))

    # Setup command-line parser
    parser = argparse.ArgumentParser(
            sys.argv[0],
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=textwrap.dedent('''\
                    Pymon %s
                    --------------------------------
                    Created by Curtis Li
                    ''' % config.get("pymon", "version")))

    # Version
    parser.add_argument(
            "-v", "--version", 
            action="version", 
            version=config.get("pymon", "version"))
    
    # Verbose mode
    parser.add_argument(
            "-d", "--debug", "--verbose",
            action="store_true",
            help="start in verbose mode")

    # Directory recursion
    parser.add_argument(
            "-r", "-R", "--recursive", 
            action="store_true",
            default=True,
            help="recursively monitor directories (Default)")
    parser.add_argument(
            "--no-recursive",
            action="store_false",
            help="do not recursively monitor directories")

    # Root path to monitor
    parser.add_argument(
            "-p", "--path",
            action="store",
            default=".",
            help="file system path to monitor")

    # Program to execute
    parser.add_argument(
            "--exec",
            action="store",
            metavar="PROG",
            dest="prog",
            default="python",
            help="program to execute application (Default: %s)" % config.get("pymon", "prog"))

    # Regex options
    parser.add_argument(
            "--match",
            action="append",
            metavar="REGEX",
            dest="regexes",
            default=[".*[.]py"],
            help="regex to match monitored files (Default: .py)")
    parser.add_argument(
            "--ignore",
            action="append",
            metavar="REGEX",
            dest="ignores",
            default=[".*[.]pyc"],
            help="regex to filter monitored files (Default: .pyc)")

    # Other options
    parser.add_argument(
            "args",
            nargs="+")

    # Parse the arguments
    args = vars(parser.parse_args(argv))
    args["app_args"] = " ".join(args["args"])

    # Add the arguments to settings dict
    settings.update(args)

    env_settings()

    return settings


def env_settings():
    global settings
    
    if "PYMON_DEBUG" in os.environ and os.environ["PYMON_DEBUG"] != "0":
        settings["debug"] = True

def get_settings():
    global settings

    # If no settings, create a default settings
    if "settings" not in globals():
        settings = parse_settings(['pymon', 'test'])

    # Return settings
    return settings

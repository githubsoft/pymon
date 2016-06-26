#!/usr/bin/env python

import sys
from watchdog.observers import Observer
from lib.cli import parseCli
from lib.watch import PymonEventHandler
from lib.transport import Transport
from lib.debug import *

def run():
    cli = parseCli(sys.argv)

    event_handler = PymonEventHandler(
            cli["regexes"], 
            cli["ignores"], 
            True, False)

    observer = Observer()
    observer.schedule(event_handler, cli["path"], recursive=True)
    observer.start()

    transport = Transport()

    try:
        while True:
            user_input = raw_input("")
            if user_input == "rs":
                transport.emit("restart")
            elif user_input == "stop":
                raise Exception
    except (KeyboardInterrupt, Exception) as e:
        transport.emit("stop")
        observer.stop()
        observer.join()

if __name__ == "__main__":
    run()
else:
    warn("Non-CLI usage has not been supported yet")
    sys.exit(0)

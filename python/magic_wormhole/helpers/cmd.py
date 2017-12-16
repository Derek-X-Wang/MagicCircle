import os
import time
start = time.time()
import six
from textwrap import fill, dedent
from sys import stdout, stderr
from wormhole.timing import DebugTiming
from wormhole.errors import (WrongPasswordError, WelcomeError, KeyFormatError,
                      TransferError, NoTorError, UnsendableFileError,
                      ServerConnectionError)
from twisted.internet.defer import inlineCallbacks, maybeDeferred
from twisted.python.failure import Failure
from twisted.internet.task import react
top_import_finish = time.time()

@inlineCallbacks
def _dispatch_command(reactor, cfg, command):
    """
    Internal helper. This calls the given command (a no-argument
    callable) with the Config instance in cfg and interprets any
    errors for the user.
    """
    cfg.timing.add("command dispatch")
    cfg.timing.add("import", when=start, which="top").finish(when=top_import_finish)

    try:
        yield maybeDeferred(command)
    except (WrongPasswordError, NoTorError) as e:
        msg = fill("ERROR: " + dedent(e.__doc__))
        print(msg, file=cfg.stderr)
        raise SystemExit(1)
    except (WelcomeError, UnsendableFileError, KeyFormatError) as e:
        msg = fill("ERROR: " + dedent(e.__doc__))
        print(msg, file=cfg.stderr)
        print(six.u(""), file=cfg.stderr)
        print(six.text_type(e), file=cfg.stderr)
        raise SystemExit(1)
    except TransferError as e:
        print(u"TransferError: %s" % six.text_type(e), file=cfg.stderr)
        raise SystemExit(1)
    except ServerConnectionError as e:
        msg = fill("ERROR: " + dedent(e.__doc__)) + "\n"
        msg += "(relay URL was %s)\n" % e.url
        msg += six.text_type(e)
        print(msg, file=cfg.stderr)
        raise SystemExit(1)
    except Exception as e:
        # this prints a proper traceback, whereas
        # traceback.print_exc() just prints a TB to the "yield"
        # line above ...
        Failure().printTraceback(file=cfg.stderr)
        print(u"ERROR:", six.text_type(e), file=cfg.stderr)
        raise SystemExit(1)

    cfg.timing.add("exit")
    if cfg.dump_timing:
        cfg.timing.write(cfg.dump_timing, cfg.stderr)

def go(f, cfg):
    # note: react() does not return
    return react(_dispatch_command, (cfg, lambda: f(cfg)))

def send(cfg, **kwargs):
    """Send a text message, file, or directory"""
    for name, value in kwargs.items():
        setattr(cfg, name, value)
    with cfg.timing.add("import", which="cmd_send"):
        # from wormhole.cli import cmd_send
        import helpers.cmd_send as cmd_send

    return go(cmd_send.send, cfg)

def receive(cfg, **kwargs):
    """
    Receive a text message, file, or directory (from 'wormhole send')
    """
    for name, value in kwargs.items():
        setattr(cfg, name, value)
    with cfg.timing.add("import", which="cmd_receive"):
        # from wormhole.cli import cmd_receive
        import helpers.cmd_receive as cmd_receive

    return go(cmd_receive.receive, cfg)
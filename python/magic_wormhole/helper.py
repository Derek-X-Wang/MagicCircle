from __future__ import print_function
from twisted.internet import defer, reactor
import wormhole

app_id = "derekxinzhewang.com/circle"
relay_url = "ws://relay.magic-wormhole.io:4000/v1"

@defer.inlineCallbacks
def sendFile(path):
    w = wormhole.create(app_id, relay_url, reactor)
    w.allocate_code()
    code = yield w.get_code()
    yield w.get_unverified_key()
    print("path is {}".format(path))
    print("code is {}".format(code))
    w.send_message(b"outbound data")
    print("tttttt1")
    yield w.close()
    print("tttttt")
    #defer.returnValue("file sent! {}".format(code))

@defer.inlineCallbacks
def receiveFile(code):
    w = wormhole.create(app_id, relay_url, reactor)
    w.set_code(code)
    inbound = yield w.get_message()
    yield w.close()
    defer.returnValue("file received")
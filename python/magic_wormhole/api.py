from __future__ import print_function
from twisted.internet import defer, reactor
import wormhole
import sys, os
import zerorpc
# from helpers.cmd_send import send as cmd_send
# from helpers.cmd_receive import receive as cmd_receive
from helpers.cmd import send, receive

app_id = "derekxinzhewang.com/circle"
relay_url = "ws://relay.magic-wormhole.io:4000/v1"
RENDEZVOUS_RELAY = "ws://relay.magic-wormhole.io:4000/v1"
TRANSIT_RELAY = "tcp:transit.magic-wormhole.io:4001"
js_server = "tcp://127.0.0.1:4243"

# @defer.inlineCallbacks
# def sendFile(path):
#     w = wormhole.create(app_id, relay_url, reactor)
#     w.allocate_code()
#     code = yield w.get_code()
#     yield w.get_unverified_key()
#     print("path is {}".format(path))
#     print("code is {}".format(code))
#     w.send_message(b"outbound data")
#     print("tttttt1")
#     yield w.close()
#     print("tttttt")
#     #defer.returnValue("file sent! {}".format(code))

# @defer.inlineCallbacks
# def receiveFile(code):
#     w = wormhole.create(app_id, relay_url, reactor)
#     w.set_code(code)
#     inbound = yield w.get_message()
#     yield w.close()
#     defer.returnValue("file received")

# class WormholeDelegate(object):
#     def wormhole_got_code(self, code):
#         print("code: %s" % code)
#     def wormhole_got_message(self, msg): # called for each message
#         print("got data, %d bytes" % len(msg))

class WormholeConfig(object):
    def __init__(self, code=None):
        self.appid = app_id
        self.relay_url = RENDEZVOUS_RELAY
        self.code = code
        self.code_length = 2
        self.text = None
        self.what = None
        self.dump_timing = None
        self.zeromode = False
        self.verify = False
        self.transit_helper = TRANSIT_RELAY
        self.listen = True
        self.output_file = ""
        self.accept_file = True
        self.tor = None
        self.launch_tor = False
        self.tor_control_port = ""
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        self.ignore_unsendable_files = False
        self.hide_progress = False
        self.timing = wormhole.timing.DebugTiming()
        self.cwd = os.getcwd()
        self.js_client = None

class WormholeAPI(object):
    def __init__(self):
        pass
    def on_js_server_ready(self, url):
        client = zerorpc.Client()
        client.connect(url)
        client.echo("py-js client connected")
        self.client = client
        return True
    def send(self, path):
        arg = WormholeConfig()
        dirname = os.path.dirname(path)
        filename = os.path.basename(path)
        arg.what = filename
        arg.cwd = dirname
        arg.js_client = self.client
        res = send(arg)
        return res
    def receive(self, code):
        args = WormholeConfig(code)
        res = receive(args)
        return "received"
    def update_code(self, code):
        print("update code is {}".format(code))
        # self.client.updateCode(code)
    def echo(self, text):
        """echo any text"""
        return text

def parse_port():
    port = 4242
    try:
        port = int(sys.argv[1])
    except Exception as e:
        pass
    return '{}'.format(port)

def main(port):
    addr = 'tcp://127.0.0.1:' + port
    s = zerorpc.Server(WormholeAPI())
    s.bind(addr)
    print('start running on {}'.format(addr))
    s.run()

if __name__ == '__main__':
    main(parse_port())
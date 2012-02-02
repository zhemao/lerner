#!/usr/bin/env python

import redisd
import socket
import settings
from collections import defaultdict

AUTH = getattr(settings, 'AUTH', '')

class Notifier:
    def __init__(self):
        self.channels = defaultdict(dict)
        self.clients = {}
        self.authenticated = defaultdict(bool)
        self.commands = {
            'connect': self.on_connect,
            'auth': self.auth,
            'subscribe': self.subscribe,
            'publish': self.publish,
            'close': self.on_close
        }

    def subscribe(self, sock, *channames):
        if not self.authenticated[sock.sock.fileno()]:
            sock.rep_error('Not Authenticated')
            return
        for i, name in enumerate(channames):
            self.channels[name][sock.sock.fileno()] = sock
            sock.rep_multibulk(['subscribe', name, i+1])
        
        self.clients[sock.sock.fileno()] = list(channames)

    def publish(self, sock, channame, message):
        if not self.authenticated[sock.sock.fileno()]:
            sock.rep_error('Not Authenticated')
            return
        chan = self.channels.get(channame)
        if chan is None:
            self.channels[channame] = {}
            sock.rep_integer(0)
        else:
            for fileno in chan:
                try:
                    chan[fileno].rep_multibulk(['message', channame, message])
                except socket.error, e:
                    self.remove_client(fileno)
                    raise e
                except IOError, e:
                    self.remove_client(fileno)
                    raise e
            sock.rep_integer(len(chan))

    def auth(self, sock, key):
        if key == AUTH:
            self.authenticated[sock.sock.fileno()] = True
            sock.rep_line('OK')
        else:
            sock.rep_error('Incorrect Auth Key')

    def remove_client(self, fileno):
        if fileno in self.clients:
            for channame in self.clients[fileno]:
                del self.channels[channame][fileno]
            del self.clients[fileno]

    def on_close(self, sock):
        fileno = sock.fileno()
        self.remove_client(fileno)
    
    def on_connect(self, sock):
        if len(AUTH) == 0:
            self.authenticated[sock.sock.fileno()] = True

if __name__ == '__main__':
    notifier = Notifier()
    
    port = getattr(settings, 'PUBSUB_PORT', 6379)
    server = redisd.RedisServer(('0.0.0.0', port), notifier.commands)
    server.serve_forever()

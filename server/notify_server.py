#!/usr/bin/env python

import redisd
import socket
import settings
from collections import defaultdict

AUTH = getattr(settings, 'AUTH', '')

class Notifier:
    def __init__(self):
        # channels is a dict of dicts mapping channel names
        # and socket filenos to socket objects
        self.channels = defaultdict(dict)
        # clients is a dict of lists mapping a socket fileno
        # to the list of channels to which the client is subscribing
        self.clients = {}
        # authenticated is a dict of socket filenos to booleans
        # indicating whether the client is authenticated yet
        self.authenticated = defaultdict(bool)
        self.commands = {
            'connect': self.on_connect,
            'auth': self.auth,
            'subscribe': self.subscribe,
            'publish': self.publish,
            'close': self.on_close
        }

    def subscribe(self, sock, *channames):
        '''Subscribe a client if they are authenticated'''
        if not self.authenticated[sock.sock.fileno()]:
            sock.rep_error('Not Authenticated')
            return
        for i, name in enumerate(channames):
            self.channels[name][sock.sock.fileno()] = sock
            sock.rep_multibulk(['subscribe', name, i+1])
        
        self.clients[sock.sock.fileno()] = list(channames)

    def publish(self, sock, channame, message):
        '''Publish a message to connected clients'''
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
        '''Take authentication from a client'''
        if key == AUTH:
            self.authenticated[sock.sock.fileno()] = True
            sock.rep_line('OK')
        else:
            sock.rep_error('Incorrect Auth Key')

    def remove_client(self, fileno):
        '''Remove a client from this server'''
        if fileno in self.clients:
            for channame in self.clients[fileno]:
                del self.channels[channame][fileno]
            del self.clients[fileno]

    def on_close(self, sock):
        fileno = sock.sock.fileno()
        self.remove_client(fileno)
    
    def on_connect(self, sock):
        if len(AUTH) == 0:
            self.authenticated[sock.sock.fileno()] = True

def start_server():
    notifier = Notifier()
    
    port = getattr(settings, 'PUBSUB_PORT', 6379)
    server = redisd.RedisServer(('0.0.0.0', port), notifier.commands)
    server.serve_forever()

if __name__ == '__main__':
    start_server()

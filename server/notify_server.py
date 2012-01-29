#!/usr/bin/env python

import redisd
import settings

class Notifier:
    def __init__(self):
        self.channels = {}
        self.clients = {}
        self.commands = {'subscribe': self.subscribe,
                         'publish': self.publish,
                         'close': self.close}

    def subscribe(self, sock, *channames):
        for i, name in enumerate(channames):
            chan = self.channels.get(name)
            if chan is None:
                self.channels[name] = {sock.sock.fileno(): sock}
            else:
                chan[sock.sock.fileno()] = sock

            sock.rep_multibulk(['subscribe', name, i+1])
        
        
        chan_list = self.clients.get(sock.sock.fileno())
        if chan_list is None:
            self.clients[sock.sock.fileno()] = list(channames)
        else:
            chan_list.extend(channels)

    def publish(self, sock, channame, message):
        chan = self.channels.get(channame)
        if chan is None:
            self.channels[channame] = {}
            sock.rep_integer(0)
        else:
            for fileno in chan:
                chan[fileno].rep_multibulk(['message', channame, message])
            sock.rep_integer(len(chan))

    def close(self, sock):
        fileno = sock.fileno()
        chan_list = self.clients.get(fileno)
        if chan_list is not None:
            for channame in chan_list:
                del self.channels[channame][fileno]
            del self.clients[fileno]

if __name__ == '__main__':
    notifier = Notifier()
    
    port = settings.PUBSUB_PORT if hasattr(settings, 'PUBSUB_PORT') else 6379
    server = redisd.RedisServer(('0.0.0.0', port), notifier.commands)
    server.serve_forever()

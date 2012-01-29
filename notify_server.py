#!/usr/bin/env python

import redisd
#import pymongo

class Notifier:
    def __init__(self):
        self.channels = {}
        #self.db = pymongo.Connection().notistream
        self.commands = {'subscribe': self.subscribe,
                         'publish': self.publish}

 #   def login(self, sock, name, key):
  #      user = self.db.users.find({'name': name})

   #     if user is None:
    #        sock.rep_error('No such user')
     #   elif user.key != key:
      #      sock.rep_error('Wrong key')
       # else:
        #    sock.rep_line('OK')

    def subscribe(self, sock, *channames):
        for i, name in enumerate(channames):
            chan = self.channels.get(name)
            if chan is None:
                self.channels[name] = {sock.sock.fileno(): sock}
            else:
                chan[sock.sock.fileno()] = sock
            sock.rep_multibulk(['subscribe', name, i+1])

    def publish(self, sock, channame, message):
        chan = self.channels.get(channame)
        if chan is None:
            self.channels[channame] = {}
            sock.rep_integer(0)
        else:
            for fileno in chan:
                chan[fileno].rep_multibulk(['message', channame, message])
            sock.rep_integer(len(chan))


if __name__ == '__main__':
    notifier = Notifier()
    server = redisd.RedisServer(('127.0.0.1', 6379), notifier.commands)
    server.serve_forever()

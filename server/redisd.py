from gevent.server import StreamServer

BUFSIZE=1024
CRLF = '\r\n'

def sock_readlines(socket):
    remainder = ''
    while True:
        data = socket.recv(BUFSIZE)
        if len(data) == 0:
            break
        if CRLF in data:
            lines = data.split(CRLF)
            yield remainder + lines[0]
            for line in lines[1:-1]:
                yield line
            if data.endswith(CRLF):
                yield lines[-1]
                remainder = ''
            else:
                remainder = lines[-1]


class RedisSocket:
    def __init__(self, sock):
        self.sock = sock
        return

    def rep_line(self, line):
        self.sock.send('+' + line + CRLF)
        return

    def rep_integer(self, num):
        self.sock.send(':' + str(num) + CRLF)

    def rep_error(self, errmsg):
        self.sock.send('-ERR ' + errmsg + CRLF)

    def rep_bulk(self, data):
        self.sock.send('$' + str(len(data)) + CRLF + data + CRLF)

    def rep_multibulk(self, lst):
        self.sock.send('*' + str(len(lst)) + CRLF)
        for data in lst:
            if isinstance(data, int):
                self.sock.send(':' + str(data) + CRLF)
            else:
                self.sock.send('$' + str(len(data)) + CRLF)
                self.sock.send(data + CRLF)

class RedisServer(StreamServer):
    def __init__(self, addr, commands):
        StreamServer.__init__(self, addr, self.handle_connection)
        self.commands = commands

    def handle_connection(self, sock, addr):
        cmdargs = []
        ncmds = 0
        nbytes = 0
        rdsock = RedisSocket(sock)

        if 'connect' in self.commands:
            self.commands['connect'](rdsock)

        for line in sock_readlines(sock):
            if len(line) == 0:
                continue
            elif line[0] == '*' and ncmds == 0:
                ncmds = int(line[1:])
            elif line[0] == '$' and nbytes == 0:
                nbytes = int(line[1:])
            else:
                cmdargs.append(line)
                nbytes = 0
                if len(cmdargs) == ncmds:
                    ncmds = 0
                    command = self.commands.get(cmdargs[0].lower())
                    if command is None:
                        rdsock.rep_error('No such command')
                    else:
                        command(rdsock, *cmdargs[1:])
                    cmdargs = []
        closecmd = self.commands.get('close')
        if closecmd is not None:
            closecmd(rdsock)
        sock.close()
        


import pwn, socket, basesock
from consts import *

_DEFAULT_REMOTE_TIMEOUT = 10

class remote(basesock.basesock):
    def __init__(self, host, port = 1337, fam = None, typ = socket.SOCK_STREAM, proto = 0, **kwargs):
        self.target = (host, port)
        if fam is None:
            if host.find(':') <> -1:
                self.family = socket.AF_INET6
            else:
                self.family = socket.AF_INET
        self.type = typ
        self.proto = proto
        self.sock = None
        self.debug = pwn.DEBUG
        self.timeout = kwargs.get('timeout', _DEFAULT_REMOTE_TIMEOUT)
        self.checked = kwargs.get('checked', True)
        self.connect()

    def connect(self):
        self.close()
        self.sock = socket.socket(self.family, self.type, self.proto)
        if self.timeout is not None:
            self.sock.settimeout(self.timeout)
        if self.checked:
            try:
                self.sock.connect(self.target)
            except socket.error, e:
                if e.errno == 111:
                    pwn.trace(' [-] Connection to %s on port %d refused\n' % self.target)
                    exit(PWN_UNAVAILABLE)
                else:
                    raise
            except socket.timeout:
                pwn.trace(' [-] Timed out while connecting to %s on port %d\n' % self.target)
                exit(PWN_UNAVAILABLE)
        else:
            self.sock.connect(self.target)
        pwn.trace(' [+] Opened connection to %s on port %d\n' % self.target)
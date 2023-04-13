import socket
import getpass


def getfqdn(name=''):
    """Get fully qualified domain name from name.
    An empty argument is interpreted as meaning the local host.
    """
    name = name.strip()
    if not name or name == '0.0.0.0':
        name = socket.gethostname()
    try:
        addrs = socket.getaddrinfo(name, None, 0, socket.SOCK_DGRAM, 0, socket.AI_CANONNAME)
    except OSError:
        pass
    else:
        for addr in addrs:
            # (<AddressFamily.AF_INET6: 23>, <SocketKind.SOCK_DGRAM: 2>, 0, 'QuestionCat', ('fe80::5850:7994:f21b:200e', 0, 0, 36))
            # (<AddressFamily.AF_INET: 2>, <SocketKind.SOCK_DGRAM: 2>, 0, '', ('198.18.0.1', 0))
            # (<AddressFamily.AF_INET: 2>, <SocketKind.SOCK_DGRAM: 2>, 0, '', ('192.168.103.47', 0))
            # (<AddressFamily.AF_INET: 2>, <SocketKind.SOCK_DGRAM: 2>, 0, '', ('192.168.145.1', 0))
            # (<AddressFamily.AF_INET: 2>, <SocketKind.SOCK_DGRAM: 2>, 0, '', ('192.168.89.1', 0))
            # (<AddressFamily.AF_INET: 2>, <SocketKind.SOCK_DGRAM: 2>, 0, '', ('172.20.160.1', 0))
            if addr[3]:
                name = addr[3]
                break
    return name


def getuser():
    return getpass.getuser()


if __name__ == '__main__':
    print(getfqdn())
    print(getuser())

from typing import override
from twisted.internet import reactor, protocol, endpoints
from twisted.protocols import basic


class PubProtocol(basic.LineReceiver):
    def __init__(self, factory):
        self.factory = factory

    @override
    def connectionMade(self):
        self.factory.clients.add(self)

    @override
    def connectionLost(self, reason):
        self.factory.clients.remove(self)

    @override
    def lineReceived(self, line):
        for c in self.factory.clients:
            source = "<{}> ".format(self.transport.getHost()).encode("ascii")
            c.sendLine(source + line)


class PubFactory(protocol.Factory):
    def __init__(self):
        self.clients = set()

    @override
    def buildProtocol(self, addr):
        return PubProtocol(self)


if __name__ == "__main__":
    endpoints.serverFromString(reactor, "tcp:1025").listen(PubFactory())
    reactor.run()

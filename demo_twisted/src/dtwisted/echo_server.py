from typing import override
from twisted.internet import reactor, protocol, endpoints


class Echo(protocol.Protocol):
    @override
    def dataReceived(self, data):
        self.transport.write(data)


class EchoFactory(protocol.Factory):
    @override
    def buildProtocol(self, addr):
        return Echo()


def run_server():
    (endpoints.serverFromString(reactor, "tcp:1025").listen(EchoFactory()))

    reactor.run()


if __name__ == "__main__":
    import argparse

    print("Starting echo server...")
    run_server()

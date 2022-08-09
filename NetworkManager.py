from socket import *
import select
import lz4.frame


class NetworkManager(object):
    """
    This class controls networking.
    This is a singleton class.
    """

    __species = None
    __first_init = True

    # UDP Networking
    host = '127.0.0.1'
    serverIP = '18.167.110.29'
    pktLen = 20480

    # Ports
    receivePort = 1250

    # Sockets
    sendSock = socket(AF_INET, SOCK_DGRAM)
    receiveSock = socket(AF_INET, SOCK_DGRAM)

    # Client socket
    local = (host, 14043)
    server = (serverIP, 1234)

    def __new__(cls, *args, **kwargs):
        if cls.__species is None:
            cls.__species = object.__new__(cls)
        return cls.__species

    def __init__(self, host='127.0.0.1', serverIP='18.167.110.29', pktLen=20480, receivePort=1250):
        if self.__first_init:
            self.host = host
            self.serverIP = serverIP
            self.pktLen = pktLen

            self.receivePort = receivePort

            self.sendSock = socket(AF_INET, SOCK_DGRAM)

            self.receiveSock = socket(AF_INET, SOCK_DGRAM)
            self.receiveSock.bind((self.host, self.receivePort))

            self.local = (self.host, 14043)
            self.server = (self.serverIP, 1234)

            self.__class__.__first_init = False

    def Receive(self):
        data = None
        ready = select.select([self.receiveSock], [], [], 1.0)
        if ready[0]:
            # incoming message from remote server
            data = self.receiveSock.recvfrom(self.pktLen)
        return data

    def Send(self, data):
        # print(data)
        data = lz4.frame.compress(data)
        # print(data)
        # print(len(data))
        self.sendSock.sendto(data, self.local)
        self.sendSock.sendto(data, self.server)

    def Terminate(self):
        # Close the sockets
        self.sendSock.close()
        print("Closed Send Socket")
        self.receiveSock.close()
        print("Closed Receive Socket")

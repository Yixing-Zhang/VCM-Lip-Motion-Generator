from socket import *


class NetworkManager(object):
    """
    This class controls networking.
    This is a singleton class.
    """

    __species = None
    __first_init = True

    # UDP Networking
    host = '127.0.0.1'
    pktlen = 2048

    # Ports
    sendPort = 1251
    receivePort = 1250

    # Sockets
    sendSock = socket(AF_INET, SOCK_DGRAM)
    receiveSock = socket(AF_INET, SOCK_DGRAM)

    # Client socket
    local = (host, 14043)

    def __new__(cls, *args, **kwargs):
        if cls.__species is None:
            cls.__species = object.__new__(cls)
        return cls.__species

    def __init__(self, host, pktlen, sendPort, receivePort):
        if self.__first_init:
            self.host = host
            self.pktlen = pktlen

            self.sendPort = sendPort
            self.receivePort = receivePort

            self.sendSock = socket(AF_INET, SOCK_DGRAM)
            self.sendSock.bind((host, sendPort))

            self.receiveSock = socket(AF_INET, SOCK_DGRAM)
            self.receiveSock.bind((host, receivePort))

            self.__class__.__first_init = False

    def Receive(self):
        return self.receiveSock.recvfrom(self.pktlen)

    def Send(self, data):
        self.sendSock.sendto(data, self.local)

    def Terminate(self):
        # Close the sockets
        self.sendSock.close()
        print("Closed Send Socket")
        self.receiveSock.close()
        print("Closed Receive Socket")


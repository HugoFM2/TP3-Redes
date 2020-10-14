from threading import Thread
import socket

BUFSZ = 1024

class ServerThread(Thread):
    def __init__ (self, addr,PORT):
          Thread.__init__(self)
          self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
          self.udp.bind((addr,PORT))

    def run(self):
        while True:
            msg, (ipRecebido, portaRecebida) = self.udp.recvfrom(BUFSZ)
            print("Recebeu do IP:",ipRecebido, "- Mensagem Recebida:" , msg.decode())

        print('Finalizando conexao do cliente')
        self.udp.close()

from threading import Thread
import socket

BUFSZ = 1024

class ServerThread(Thread):

    def __init__ (self, addr,PORT):
          Thread.__init__(self)
          self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
          self.udp.bind((addr,PORT))
          self.myIP = addr
          self.myRouteTable = {}

    def run(self):
        while True:
            msg, (ipRecebido, portaRecebida) = self.udp.recvfrom(BUFSZ)
            print("Recebeu do IP:",ipRecebido, "- Mensagem Recebida:" , msg.decode())

        print('Finalizando conexao do cliente')
        self.udp.close()

    def AddFromTable(self,ip,weight):
        print("adicionado")
        if(ip in self.myRouteTable):
            print("ip ja adicionado, incorporando ao existente")
            self.myRouteTable[ip].append([int(weight), self.myIP])
        else:
            self.myRouteTable[ip] = [[int(weight), self.myIP]]

    def DelFromTable(self,ip):
        if (ip in self.myRouteTable):
            for conexao in self.myRouteTable[ip]: #Passa por todas as conexoes desse ip
                print("CONEXAO:", conexao)
                if(conexao[1] == self.myIP): # Se a conexao foi feita desse enlace, remover conexao
                    self.myRouteTable[ip].remove(conexao)
            if(len(self.myRouteTable[ip]) == 0): # Se após essa remoção, a lista estiver vazia, remover a key da lista
                self.myRouteTable.pop(ip)

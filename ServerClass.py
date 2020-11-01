from threading import Thread
import socket
import json
import FuncoesApoio
import JSON

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
            print()
            print("MENSAGEM RECEBIDA:",msg.decode())
            msgload = json.loads(msg.decode())
            if(msgload["type"] == "trace"):
                self.traceRoute(msg.decode())
            else:
                if(FuncoesApoio.MessageForMe(self.myIP,msgload)):
                    print("MENSAGEM PARA MIM:",msg.decode())
                else:


                    if(msgload["type"] == "data"): #Repassar mensagem se for do tipo data
                        proxServ = FuncoesApoio.GetMenorRota(self.myIP,msgload["destination"],self.myRouteTable) # retorna o proximo servidor a repassar a mensagem
                        if(proxServ == 0):
                            print("Rota não disponivel para",msgload["destination"])
                        else:
                            print("Enviar entao essa mensagem para:",proxServ) #

            # print("Recebeu do IP:",ipRecebido, "- Mensagem Recebida:" , msg.decode())

        print('Finalizando conexao do cliente')
        self.udp.close()

    def SendMsgTo(self,msg,ipDest):
        dest = (ipDest, 55151)
        self.udp.sendto(msg.encode(), dest)

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

    def TraceCommand(self,ipDest): # Formata o 1o trace e envia para o proximo servidor
        msg = JSON.Trace(self.myIP,ipDest,[self.myIP])
        proxServ = FuncoesApoio.GetMenorRota(self.myIP,ipDest,self.myRouteTable) # retorna o proximo servidor a repassar a mensagem
        self.SendMsgTo(msg,ipDest)
        print("Enviar 1o Trace:",msg)

    def traceRoute(self,JSONmsg): # Funcao a se usar quando recebe uma mensagem do tipo trace
        msg = json.loads(JSONmsg)
        msg["hops"].append(self.myIP)
        resultJSON = json.dumps(msg)
        if(self.myIP == msg["destination"]):
            dataMsg = JSON.Data(self.myIP,msg["source"],resultJSON)
            self.SendMsgTo(dataMsg,msg["source"])# Aqui eles se invertem uma vez q o ultimo trace q recebeu e chegou ao destino precisa repassar ao de origem
            print("Enviar Data:",dataMsg,"para:",msg["source"]) # Enviar mensagem como data aqui
        else:
            print("Enviar trace:",resultJSON) #enviar mensagem como trace aqui

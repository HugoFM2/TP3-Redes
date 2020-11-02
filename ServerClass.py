from threading import Thread
import threading
import socket
import json
import FuncoesApoio
import JSON

BUFSZ = 1024

class ServerThread(Thread):

    def __init__ (self, addr,PORT, TimeToSend):
          Thread.__init__(self)
          self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
          self.udp.bind((addr,PORT))
          self.myIP = addr
          # self.myRouteTable = {"127.0.0.1": [[18, "127.0.0.1"]], "127.0.0.4": [[10, "127.0.0.4"]]}
          self.myRouteTable = {self.myIP : [[0,self.myIP]]}
          #AAA ips temporarios para verificar a questao do update
          self.timeToSend = TimeToSend

    def run(self):
        self.sendPeriodicThread()
        while True:
            msg, (ipRecebido, portaRecebida) = self.udp.recvfrom(BUFSZ)
            # print()
            # print("MENSAGEM RECEBIDA:",msg.decode())
            msgload = json.loads(msg.decode())
            if(msgload["type"] == "trace"):
                self.traceRoute(msg.decode())
            elif(msgload["type"] == "update"):
                self.ReceiveUpdate(msg.decode())
            else:
                if(FuncoesApoio.MessageForMe(self.myIP,msgload)): # se a mensagem for para mim,
                                                                  # imprimir na tela
                    print("Payload: ",msgload["payload"])
                else: # Se a mensagem nao for para mim, repassar
                    if(msgload["type"] == "data"): #Repassar mensagem se for do tipo data
                        proxServ = FuncoesApoio.GetMenorRota(self.myIP,msgload["destination"],self.myRouteTable) # retorna o proximo
                                                                                                                 # proximo servidor a
                                                                                                                 # repassar a mensagem
                        if(proxServ == 0):
                            print("Rota nao disponivel para",msgload["destination"])
                        else:
                            self.SendMsgTo(msg.decode(),proxServ)
                            print("Enviar entao essa mensagem para:",proxServ) #


        print('Finalizando conexao do cliente')
        self.udp.close()

    def SendMsgTo(self,msg,ipDest):
        if(ipDest in self.myRouteTable):
            proxServ = FuncoesApoio.GetMenorRota(self.myIP,ipDest,self.myRouteTable) # retorna o proximo servidor a repassar a mensagem
            dest = (proxServ, 55151)
            self.udp.sendto(msg.encode(), dest)
        else:
            print("ERROR - nao eh possivel enviar esse dado pois a rota nao eh conhecida")

    def AddFromTable(self,ipDest,ipFrom,weight): #ipFrom -> de onde a conexao vem
        # print("Adicionado!")
        if(str(ipDest) in self.myRouteTable):
            for conexao in (self.myRouteTable[str(ipDest)]):
                # print("ROTA:", conexao)
                if(conexao[1] == ipFrom):
                    self.myRouteTable[str(ipDest)].remove(conexao)
                    # print("Essa rota ja existe,removendo rota para sobescreve-la ")

            # print("ip ja adicionado no dicionario, incorporando a conexao a chave existente")
            self.myRouteTable[str(ipDest)].append([int(weight), str(ipFrom)])
        else:
            self.myRouteTable[str(ipDest)] = [[int(weight), ipFrom]]

    def DelFromTable(self,ip):
        if (ip in self.myRouteTable):
            for conexao in self.myRouteTable[ip]: #Passa por todas as conexoes desse ip
                if(conexao[1] == self.myIP): # Se a conexao foi feita desse enlace, remover conexao
                    self.myRouteTable[ip].remove(conexao)
            if(len(self.myRouteTable[ip]) == 0): # Se apos essa remocao, a lista estiver vazia, remover a key da lista
                self.myRouteTable.pop(ip)

    def TraceCommand(self,ipDest): # Formata o 1o trace e envia para o proximo servidor
        msg = JSON.Trace(self.myIP,ipDest,[self.myIP])
        proxServ = FuncoesApoio.GetMenorRota(self.myIP,ipDest,self.myRouteTable) # retorna o proximo servidor a repassar a mensagem
        # print("PROXSERVTRACE:",proxServ)
        if(proxServ !=0):
            self.SendMsgTo(msg,proxServ)
            # print("Enviar 1o Trace:",msg)
        else:
            print("ERROR - Server nao esta na lista, aguarde os updates, ou adicione uma rota")

    def traceRoute(self,JSONmsg): # Funcao a se usar quando recebe uma mensagem do tipo trace
        msg = json.loads(JSONmsg)
        msg["hops"].append(self.myIP)
        resultJSON = json.dumps(msg)
        if(self.myIP == msg["destination"]):
            dataMsg = JSON.Data(self.myIP,msg["source"],resultJSON)
            self.SendMsgTo(dataMsg,msg["source"])# Aqui eles se invertem uma vez q o ultimo trace q recebeu e chegou ao destino precisa repassar ao de origem
            # print("Enviar Data:",dataMsg,"para:",msg["source"]) # Enviar mensagem como data aqui
        else:
            proxServ = FuncoesApoio.GetMenorRota(self.myIP,msg["destination"],self.myRouteTable) # retorna o proximo servidor a repassar a mensagem
            self.SendMsgTo(resultJSON,proxServ) # Caso nao seja o ultimo, repassar para o prox serv
            # print("Enviar trace:",resultJSON) #enviar mensagem como trace aqui


    def sendPeriodicThread(self):
        # print("COMECO ENVIO PERIODICO")
        for i in self.myRouteTable:
            if(i == self.myRouteTable[i][0][1] and i != self.myIP): # Checar se eh um roteador vizinho e se nao eh ele mesmo
                # print("ENVIANDO UPDATE para:",i)
                self.sendPeriodic(i)
        # print("TERMINO ENVIO PERIODICO")
        threading.Timer(self.timeToSend, self.sendPeriodicThread).start()

    #Funcao responsavel pela mensagem de update
    def sendPeriodic(self, ipDest):
        dicAux = {}
        for i in self.myRouteTable:
            aux1 = FuncoesApoio.GetMenorPesoRota(self.myIP, i, self.myRouteTable)
            aux2 = FuncoesApoio.GetMenorPesoRota(self.myIP, ipDest, self.myRouteTable)
            if (i != self.myIP and i == aux1[1]): # Não enviar a rota do meu ip e de rotas aprendidas
                if(aux1 != aux2):
                    pesoDist = aux1[0] + aux2[0]
                    dicAux[i] = pesoDist
                else:
                    dicAux[self.myIP] = aux1[0]
        msg = JSON.Update(self.myIP, ipDest, dicAux)

        self.SendMsgTo(msg, ipDest)
        # print("ENVIANDO UPDATE:,",msg)
        # print()

    def ReceiveUpdate(self,JSONmsg):
        msg = json.loads(JSONmsg)
        dicAux = msg["distances"]
        for i in dicAux:
            self.AddFromTable(i,msg["source"], dicAux[i])
        # print("TABELA ROTEADOR RECV:",self.myRouteTable)
        # print()

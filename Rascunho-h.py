import json

def JSONMessageData(source,destination,payload):
    if (not isinstance(source, str) or not isinstance(destination, str) or not isinstance(payload, str)):
        raise TypeError("Tipo Não suportado para a função")

    message = {
    "type"          : "data",
    "source"        : source,
    "destination"   : destination,
    "payload"       : payload,
    }
    message = json.dumps(message)
    return message

def JSONMessageTrace(source,destination,hops):
    if (not isinstance(source, str) or not isinstance(destination, str) or not isinstance(hops, list)):
        raise TypeError("Tipo Não suportado para a função")
    message = {
    "type" : "trace",
    "destination" : destination,
    "hops" : hops
    }
    message = json.dumps(message)
    return message


hops =  ["127.0.1.5"]
mensagem = JSONMessageTrace("abb","abb",hops)
print(type(hops))
print(mensagem)

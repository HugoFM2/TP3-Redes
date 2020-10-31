import json

def Data(source,destination,payload):
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

def Update(source,destination,distances):
    if (not isinstance(source, str) or not isinstance(destination, str) or not isinstance(distances, dict)):
        raise TypeError("Tipo Não suportado para a função")
    message = {
    "type"              : "update",
    "source"            : source,
    "destination"       : destination,
    "distances"         : distances,
    }
    message = json.dumps(message)
    return message

def Trace(source,destination,hops):
    if (not isinstance(source, str) or not isinstance(destination, str) or not isinstance(hops, list)):
        raise TypeError("Tipo Não suportado para a função")
    message = {
    "type" : "trace",
    "source" : source,
    "destination" : destination,
    "hops" : hops
    }
    message = json.dumps(message)
    return message

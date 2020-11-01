import JSON
import Regex
import json


dics  = [1,2,3]

dis = [{"ipFinal" : "127.0.1.5", "pesoTotal": "10", "atravesDeQualRota": "127.0.1.5"} for k in range(len(dics))]

def checkDicAndChangePeso(a,b,c,d):
  for i in range(len(a)):
    if (a[i]["ipFinal"] == b):
        a[i]["pesoTotal"] = c
        a[i]["atravesDeQualRota"] = d

distance =  {
"127.0.1.4": 10,
"127.0.1.5": 0,
"127.0.1.2": 10,
"127.0.1.3": 10
}
mensagem = JSON.Update("abb","abb",distance)
print(type(distance))
print(mensagem)
print("\n\n")
parsed_json = (json.loads(mensagem))
print(parsed_json['type'])
if (parsed_json['type'] == "update"):
  checkDicAndChangePeso(dis, "127.0.1.5", "20", "127.0.1.5")
  for key in dis:
    print(key)
  
else:
  print ("no")

if Regex.CheckADD("add 192.168.15.5 0"):
  print("YES! We have a match!")
else:
  print("No match")

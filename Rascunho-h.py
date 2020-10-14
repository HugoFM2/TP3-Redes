import JSON
import Regex


distance =  {
"127.0.1.4": 10,
"127.0.1.5": 0,
"127.0.1.2": 10,
"127.0.1.3": 10
}
mensagem = JSON.Update("abb","abb",distance)
print(type(distance))
print(mensagem)

if Regex.CheckADD("add 192.168.15.5 0"):
  print("YES! We have a match!")
else:
  print("No match")

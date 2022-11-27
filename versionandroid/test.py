from pytapo import Tapo

user = "tapoadmin" # user you set in Advanced Settings -> Camera Account
password = "tapoadmin" # password you set in Advanced Settings -> Camera Account
host = "192.168.1.127" # ip of the camera, example: 192.168.1.52

tapo = Tapo(host, user, password)

print(tapo.getBasicInfo())
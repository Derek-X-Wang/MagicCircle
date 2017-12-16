from api import WormholeAPI

w = WormholeAPI()

res = w.receive("5-finicky-aardvark")
print(res)
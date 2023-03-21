
import sunfish
'''
print("Python version")
print (sys.version)
print("Version info.")
print (sys.version_info)
'''
print ("here")
position = sunfish.Position(sunfish.initial, 0, (True,True), (True,True), 0, 0)
print ("her")
move = sunfish.parse("e2e4")
position = position.move(move)
depth = 4 # search depth
move, score = sunfish.search(position, depth)
print (move)
print (score)
exit
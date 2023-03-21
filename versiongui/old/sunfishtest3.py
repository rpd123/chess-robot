import CBstate
import subprocess
import sys

def sget():
    
    # using the 'isready' command (engine has to answer 'readyok')
    # to indicate current last line of stdout
    stx=""
    engine.stdin.write('isready\n')
    engine.stdin.flush()
    print('\nengine:')
    while True :
        text = engine.stdout.readline().strip()
        print (text)
        #if text == 'readyok':
         #   break
        if text !='':   
            print('\t'+text)
            text = text
        if text[0:8] == 'bestmove':
            mtext=text
            return mtext


engine = subprocess.Popen(
    [sys.executable, "-u", CBstate.myfish],
    universal_newlines=True,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    #shell=True
    )

print (engine.stdout.readline())
text = sget()
print (text)
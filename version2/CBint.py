#
#This program plays chess using Stockfish the open source chess engine, using the ChessBoard library to manage the board.
#Credit to www.chess.fortherapy.co.uk for much of the code here


# initiate chessboard
from stockfish import Stockfish
from ChessBoard import ChessBoard
import subprocess, time
import CBstate
chessboard = ChessBoard()
import robotmove as RD
import playermove_rpd as RDpm
import logging

if CBstate.windowsos:    
    stockfish = Stockfish(CBstate.stockfishexe, parameters=CBstate.stockfishparams)
else:
    #stockfish = Stockfish(parameters=CBstate.stockfishparams)
    stockfish = Stockfish()
mydir = CBstate.mydir

#stockfish.update_engine_parameters({"Threads": 4})   
#stockparams = stockfish.get_parameters()
#for key, value in stockparams.items():
#    print(key, ' : ', value)
'''
Stockfish 14 Windows, stockfish module 3.24.0

Debug Log File  :  
Contempt  :  0
Min Split Depth  :  0
Ponder  :  false
MultiPV  :  1
Skill Level  :  20
Move Overhead  :  10
Minimum Thinking Time  :  20
Slow Mover  :  100
UCI_Chess960  :  false
UCI_LimitStrength  :  false
UCI_Elo  :  1350
Threads  :  4
Hash  :  1024
'''
# depth 15

RD.speaker("Hello! Let's play chess!")
logging.debug("Start")
dummy = "" 
movelist = []

reasons = (
    "No reason",
    "Invalid move",
    "Invalid colour",
    "Invalid 'from' location",
    "Invalid 'to' location",
    "Must set promotion",
    "Game is over",
    "Ambiguousmove")
    

lastmovetype = (
    "Normal",
    "En passant available",
    "Capture en passant",
    "Pawn promoted",
    "Castle on king's side",
    "Castle on queen's side")
    
gameresult = (
    "No result",
    "Checkmate. You won!",
    "Checkmate I win!",
    "Stalemate Game over.",
    "Draw by 50 moves rule",
    "Draw by threefold repetition")
    
chessboard.setPromotion(chessboard.QUEEN)
    
# initiate stockfish chess engine
'''
engine = subprocess.Popen(
    '/usr/games/stockfish',
    universal_newlines=True,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,)
'''
    
def checkvarious(): 
    
    if chessboard.getLastMoveType() != -1 and chessboard.getLastMoveType() != 0:
        print((lastmovetype[chessboard.getLastMoveType()]))
    if chessboard.isCheck():
        print ("Check!")
        RD.speaker("Check!")
    if chessboard.isGameOver():
        print((gameresult[chessboard.getGameResult()]))
        RD.speaker(gameresult[chessboard.getGameResult()])
        RD.quitter()
    return()

def get():
    return stockfish.get_best_move()
    # using the 'isready' command (engine has to answer 'readyok')
    # to indicate current last line of stdout
    stx=""
    engine.stdin.write('isready\n')
    print('\nengine:')
    while True :
        text = engine.stdout.readline().strip()
        if text == 'readyok':
            break
        if text !='':   
            print(('\t'+text))
        if text[0:8] == 'bestmove':
        
            return text
'''
def sget():
    
    # using the 'isready' command (engine has to answer 'readyok')
    # to indicate current last line of stdout
    stx=""
    engine.stdin.write('isready\n')
    print('\nengine:')
    while True :
        text = engine.stdout.readline().strip()
        #if text == 'readyok':
         #   break
        if text !='':   
            #print('\t'+text)
            text = text
        if text[0:8] == 'bestmove':
            mtext=text
            return mtext
'''
def getboard():
    """ gets a text string from the board """
    #btxt = raw_input("\nYour move: ").lower()
    kpress = input ("Now play your move, then press enter")
    if kpress == "s":
        RD.nudgespecial()  # nudge up/down during game
        input ("Now play your move, then press enter")

    validkingmoves = chessboard.getValidMoves((4,7))
    btxt = RDpm.getplayermove(chessboard.getBoard(), validkingmoves)
    return btxt
    
def sendboard(stxt):
    """ sends a text string to the board """
    print ("Computer move:")
    print(("\n" +stxt))

def newgame():
    global movelist

    chessboard.resetBoard()
    fmove=""
    movelist = []
    return fmove


def bmove(fmove):
    global movelist, kingcheck
    boardbefore = chessboard.getBoard()
    """ assume we get a command of the form ma1a2 from board"""    
    fmove=fmove
    # Get a move from the board
    brdmove = bmessage[1:5].lower()
    #brdmove = bmessage[1:6]    # allow for O-O-O, etc
    # Code added here make computer play white by sending null message "ma9a9" to Stockfish
    if brdmove =="a9a9":
        fmove = ""
        print ("Me First")
        put(fmove)
        # send move to engine & get engines move

        
        ##put("go movetime " +movetime)
        # time.sleep(6)
        # text = get()
        # put('stop')
        text = sget()
        print (text)
        smove = text[9:13]
        hint = text[21:25]
        if chessboard.addTextMove(smove) != True :
            stxt = "e"+ str(chessboard.getReason())+move
            chessboard.printBoard()
            sendboard(stxt)

        else:
            temp=fmove
            fmove =temp+" " +smove
            stx = smove+hint      
            sendboard(stx)
            chessboard.printBoard()
            # maxfen = chessboard.getFEN()
            print(("Computer move: " +smove))
            computermove = smove
            return fmove
        return fmove
    # end of section that allows computer to play white
    
    # now validate move
    # if invalid, get reason & send back to board
      #  chessboard.addTextMove(move)
    if chessboard.addTextMove(brdmove) == False :
        ### rpd
        if CBstate.kingincheck:
            CBstate.kingincheck = False
            whiteincheck = "Your king is in check. "
        else:
            whiteincheck = ""
        etxt = whiteincheck + "Error: "+ reasons[(chessboard.getReason())] + " in move " + brdmove
        RD.speaker(whiteincheck + "Error "+ reasons[(chessboard.getReason())] + " in move " + brdmove)
        chessboard.printBoard()
        sendboard(etxt)
        smove = ""
        return fmove
                       
#  elif valid  make the move and send Fen to board
    
    else:
        chessboard.printBoard()        
        # maxfen = chessboard.getFEN()
        # sendboard(maxfen)
       # remove line below when working
        #_input("\n\nPress the enter key to continue")
        print ("fmove")
        print(fmove)
        print ("brdmove")
        print(brdmove)
        checkvarious()
        #RD.movepiece(brdmove[0:2], brdmove[2:4], boardbefore)
        
        boardbefore = RD.updateboard(brdmove[0:2], brdmove[2:4], boardbefore)
        if fmove[-1:].isnumeric():
            movelist.append (fmove[-4:])
        else:
            movelist.append (fmove[-5:])
        #movelist.append (fmove[1:])
        fmove =fmove+" " +brdmove
        movelist.append (brdmove)
        print ("movelist")
        print (movelist)
        cmove = "position startpos moves"+fmove
        print (cmove)

            #        if fmove == True :
            #                move = "position startpos moves "+move
            #        else:
            #               move ="position fen "+maxfen

        # put('ucinewgame')
        # get()
       
        ##put(cmove)
        put(movelist)   # 3
        # send move to engine & get engines move
        
        ##put("go movetime " +movetime)
        # time.sleep(6)
        # text = get()
        # put('stop')
        
        text = get()
        ##print(("text: " + text))
        ##smove = text[9:13]
        smove = text
        hint = text[21:25]
        if chessboard.addTextMove(smove) != True :
            stxt = "Error: " + reasons[chessboard.getReason()] + " in move " + smove
            chessboard.printBoard()
            sendboard(stxt)
            computermove = ""

        else:
            temp=fmove
            fmove =temp+" " +smove
            stx = smove+hint      
            sendboard(stx)
            chessboard.printBoard()
            # maxfen = chessboard.getFEN()
            
            print(("Computer move: " +smove)) 
            CBstate.cbstate = chessboard.getLastMoveType()                       
            RD.movepiece(smove[0:2], smove[2:4], boardbefore)
            checkvarious()
            return fmove
        

def put(command):
    print(command)
    #engine.stdin.write(command+'\n')
    #stockfish.make_moves_from_current_position([command])
    stockfish.set_position(command)

# assume new game
print ("\nChess Program \n")
#print ("Stockfish " + str(stockfish.get_stockfish_major_version()))

skill = "10"
movetime = "6000"
fmove = newgame()


try:
    calcam = input("Calibrate camera? (y/n):")
    if calcam == "y":
        RDpm.calibratecamera(chessboard.getBoard())
    RDpm.dummymove(chessboard.getBoard())
    RD.init()
    #RD.quitter()   
    while True:         
        # Get  message from board
        bmessage = getboard()        
        # Message options   Move, Newgame, level, style
        if bmessage:
            code = bmessage[0]
        else:
            code = ""
        
        # decide which function to call based on first letter of txt
        fmove=fmove
        if code == 'm':
            fmove = bmove(fmove)                                
                        
        elif code == 'n': newgame()
        elif code == 'l': level()
        elif code == 's': style()
        else:
            sendboard('error at option')
except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    RD.quitter()       # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.

RD.quitter()


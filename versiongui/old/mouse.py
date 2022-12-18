import cv2

def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:                  
        
        # displaying the coordinates
        # on the Shell
        print(x, ' ', y)

cv2.setMouseCallback('image', click_event)

# wait for a key to be pressed to exit
cv2.waitKey(0)
cv2.destroyAllWindows()
    

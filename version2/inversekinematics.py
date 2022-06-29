# Only required if motors are servos. Arduino code is different too!

def inversekinematics(x, y, z, g, wa, wr):
    # length, height, angle, gripper, wrist angle, wrist rotate
	# Initialize variables

	Elbow = 0
	Shoulder = 0
	Wrist = 0
	
	# Get distance
	floatM = sqrt((y * y) + (x * x))
#	print("floatM        = " + str(floatM))
	
	# Check X position for error
	if(floatM <= 0):
		return 1
	
	# Get first angle (radians)
	floatA1 = atan(y / x)
#	print("floatA1       = " + str(floatA1))
#	print("x             = " + str(x))
	
	# Check X position for error
	if(x <= 0):
		return 2
	
	# Get 2nd angle (radians)
	floatA2 = acos((A * A - B * B + floatM * floatM) / ((A * 2) * floatM))
#	print("floatA2       = " + str(floatA2))
	
	# Calculate elbow angle (radians)
	floatElbow = acos((A * A + B * B - floatM * floatM) / ((A * 2) * B))
#	print("floatElbow    = " + str(floatElbow))
	
	# Calculate shoulder angle (radians)
	floatShoulder = floatA1 + floatA2
#	print("floatShoulder = " + str(floatShoulder))
	
	# Obtain angles for shoulder / elbow
	Elbow = floatElbow * rtod
#	print("Elbow         = " + str(floatA2))
	Shoulder = floatShoulder * rtod
#	print("Shoulder      = " + str(Shoulder))
	
	# Check elbow/shoulder angle for error
	if((Elbow <= 0) or (Shoulder <= 0)):
		return 3
	Wrist = fabs(wa - Elbow - Shoulder) - 90
	
	# Return the new values
	motors_SEWBZWrG = (Shoulder, Elbow, Wrist, z, g, wr)
	
	# <<< debug <<<
	#print("SHOULDER\tELBOW   \tWRIST-A \tBASE-ROT\tGRIPPER \tWRIST-R \t")
	#print(str(Shoulder) + "\t" + str((180 - Elbow)) + "\t" + str((180 - Wrist)) + "\t" + str(z) + "\t" + str(g) + "\t" + str(wr) + "\t")
	#print(str(getPulseFromAngle(Shoulder)) + "\t" + str(getPulseFromAngle(180 - Elbow)) + "\t" + str(getPulseFromAngle(180 - Wrist)) + "\t" + str(getPulseFromAngle(z)) + "\t" + str(getPulseFromAngle(g)) + "\t" + str(getPulseFromAngle(wr)) + "\t")
	# >>> debug >>>
	
	return (motors_SEWBZWrG)
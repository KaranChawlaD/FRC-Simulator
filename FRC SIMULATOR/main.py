#Initializing Libraries
import pygame

#Pygame Initialize Function
pygame.init()

#Pygame Window Name
pygame.display.set_caption('      FRC Simulator') #Spaces to center

#Pygame Window Logo
logo = pygame.image.load('logo.png') #Load logo image
pygame.display.set_icon(logo)

#Text Font
font = pygame.font.Font('freesansbold.ttf', 30)

#Screen Dimensions
scale = 1.4
width, height = 316*scale, 640*scale
screen = pygame.display.set_mode((width, height))

#Background Colour
gray = (65, 66, 66)
lightgray = (145,153,166)
darkgray = (40, 40, 40)
blue = (13,13,254)
red = (255,13,16)
white = (255, 255, 255)
black = (0, 0, 0)

#Robot
robotImage = pygame.image.load('robot.png')
robotScaleOld = pygame.transform.rotozoom(robotImage, 0.0, 0.22)
robotScale = robotScaleOld
robot = robotScale.get_rect()
robot.center = (width/2, height/2)
robotCurrentAngle = 0
lastX = 0
lastY = 0

#Charge Station
stationImage = pygame.image.load('station.png')
stationScaleBlue = pygame.transform.rotozoom(stationImage, -90, 0.60)
stationScaleRed = pygame.transform.rotozoom(stationImage, 90, 0.60)
stationBlue = stationScaleBlue.get_rect()
stationRed = stationScaleBlue.get_rect()
stationBlue.center = (145, 200)
stationRed.center = (145, 695)

#Cube/Cone
cubeImage = pygame.image.load('cube.png')
coneImage = pygame.image.load('cone.png')
cubeScale = pygame.transform.rotozoom(cubeImage, 0, 0.50)
coneScale = pygame.transform.rotozoom(coneImage, 0, 0.50)

#Cargo Positions for Loading Station
groundRed = (300*scale, 75*scale)
top1Red = (225*scale, 10*scale)
top2Red = (265*scale, 10*scale)
groundBlue = (300*scale, 555*scale)
top1Blue= (225*scale, 620*scale)
top2Blue = (265*scale, 620*scale)
cargoSwitch = "cube"

#Cargo Position For Grid
a1 = 0
b1 = 0
c1 = 0
d1 = 0
e1 = 0
f1 = 0
g1 = 0
h1 = 0
i1 = 0
a2 = 0
b2 = 0
c2 = 0
d2 = 0
e2 = 0
f2 = 0
g2 = 0
h2 = 0
i2 = 0
a3 = 0
b3 = 0
c3 = 0
d3 = 0
e3 = 0
f3 = 0
g3 = 0
h3 = 0
i3 = 0

#Welcome Message
print("\n\n\nWelcome to FRC Simulator! This is designed for the drive team of FRC teams to get a virtual simulated idea of how the game design works.")
print("\nYou will be able to control a robot with personalized customations to fit to your own liking.")
print("\nThe controls are simple! Stand near cargo to intake it. WASD to strafe in all directions, and the left and right arrow keys to turn the robot.")
print("\nThe Up and Down arrows change the cargo at the loading station. To score HIGH be right in front of the target and click Q! For MID click E! For Hybrid click R. That's it! Enjoy!")

#Acceleration and Deacceleration
accelY = 0
accelX = 0
yChange = 0
xChange = 0
maxSpeed = float(input("\nPlease enter the max speed of the robot in terms of pixels per frame (80 fps-usual speed is 3.5): "))
chargeStationSlow = 1.0

#Pygame Clock
clock = pygame.time.Clock()
timer = 135

#Loading Station Time
loadingTimer = 0
loadingLimit = 80*float(input("\nPlease enter the time (seconds) it takes at the loading station to recieve a cargo: "))
loadingIntake = False

#Grid Time
outtakeLimit = float(input("\nPlease enter the time (seconds) it takes to outtake cargo at the grid: "))

#Key Dictionary
pressedKeys = {"Slide Up": False, "Slide Down": False, "Slide Left": False, "Slide Right": False, "Turn Left": False, "Turn Right": False}

#Running Variable
running = True

#Rotate Function
def rotCenter(image, angle, currentAngle, x, y):
    
    rotatedImage = pygame.transform.rotate(image, angle+currentAngle) #Rotating image onto surface
    currentAngle = angle+currentAngle #Tracking current robot angle
    newRect = rotatedImage.get_rect(center = image.get_rect(center = (x, y)).center) #Creating new rect for robot

    return rotatedImage, currentAngle, newRect #Returning important variables

#While True Statement to Run Code
while running:

  #Event Sequences
  for event in pygame.event.get():
    
    if event.type == pygame.QUIT: #If Press Quit, Then Shut Down Window
            running = False

  keysPressed = pygame.key.get_pressed() #Detecting Pressed Keys

  if keysPressed[pygame.K_UP]: #Switching Cargo Pieces
    cargoSwitch = "cone"

  if keysPressed[pygame.K_DOWN]: #Switching Cargo Pieces
    cargoSwitch = "cube"

  if keysPressed[pygame.K_w] and not keysPressed[pygame.K_s]: #If W Pressed
    accelY = -0.2 #Y - Acceleration set to -0.2

  elif keysPressed[pygame.K_s] and not keysPressed[pygame.K_w]: #If S Pressed
    accelY = 0.2 #Y - Acceleration set to 0.2
  
  else:
    accelY = 0 #Otherwise no acceleration
  
  if keysPressed[pygame.K_a] and not keysPressed[pygame.K_d]: #If A Pressed
    accelX = -0.2 #X - Acceleration set to -0.2
  
  elif keysPressed[pygame.K_d] and not keysPressed[pygame.K_a]: #If D Pressed
    accelX = 0.2 #X - Acceleration set to 0.2
  
  else:
    accelX = 0 #Otherwise no acceleration
  
  if keysPressed[pygame.K_LEFT]: #If Left Arrow Pressed
    pressedKeys["Turn Left"] = True
  else:
    pressedKeys["Turn Left"] = False #Else if Left Arrow Released

  if keysPressed[pygame.K_RIGHT]: #If Right Arrow Pressed
    pressedKeys["Turn Right"] = True
  else:
    pressedKeys["Turn Right"] = False #Else if Right Arrow Released

  #Robot Movement
  yChange += accelY #Adding acceleration to speed
  xChange += accelX #Adding acceleration to speed

  if (robot.center[0] < 219 and robot.center[0] > 73) and (robot.center[1] < 265 and robot.center[1]>132):
    chargeStationSlow=1/2.25

  else:
    chargeStationSlow=1
  
  if abs(yChange) >= maxSpeed*chargeStationSlow:  # If maxSpeed is exceeded.
    # Normalize the yChange and multiply it with the maxSpeed.
    yChange = yChange/abs(yChange) * maxSpeed * chargeStationSlow
  
  if abs(xChange) >= maxSpeed*chargeStationSlow:  # If maxSpeed is exceeded.
    # Normalize the xChange and multiply it with the maxSpeed.
    xChange = xChange/abs(xChange) * maxSpeed * chargeStationSlow
  
  if accelY == 0:
    yChange *= 0.92 #If no movement, deaccelerate speed
  
  if accelX == 0:
    xChange *= 0.92 #If no movement, deaccelerate speed

  if pressedKeys["Turn Right"]:
    robotScale, robotCurrentAngle, robot = rotCenter(robotScaleOld, -2, robotCurrentAngle, robot.centerx, robot.centery) #Rotate right 2 degrees while Turn Right true
  if pressedKeys["Turn Left"]:
    robotScale, robotCurrentAngle, robot = rotCenter(robotScaleOld, 2, robotCurrentAngle, robot.centerx, robot.centery) #Rotate left 2 degrees while Turn Left true
  
  if (robot.center[1]+yChange>111 and robot.center[1]+yChange<870 and robot.center[0]+xChange>23 and robot.center[0]+xChange<419):
    if (robot.center[1]+yChange<196):
      if (robot.center[0]+xChange<265):
        robot.move_ip(xChange, yChange) #Move robot (xChange, yChange) coordinates
    else:
      robot.move_ip(xChange, yChange) #Move robot (xChange, yChange) coordinates

  # if keysPressed[pygame.K_v]:
  #   print(robot.center)

  #Cargo Detection
  if (robot.center[0]-22) < groundBlue[0]+20 and groundBlue[0]-2 < (robot.center[0]+22) and (robot.center[1]-28) < groundBlue[1]+20 and groundBlue[1]-2 < (robot.center[1]+28):
    loadingTimer+=1
    if (loadingTimer==loadingLimit):
      loadingIntake = True
  
  if (robot.center[0]-22) < top1Blue[0]+20 and top1Blue[0]-2 < (robot.center[0]+22) and (robot.center[1]-28) < top1Blue[1]+20 and top1Blue[1]-2 < (robot.center[1]+28):
    loadingTimer+=1
    if (loadingTimer==loadingLimit):
      loadingIntake = True

  if (robot.center[0]-22) < top2Blue[0]+20 and top2Blue[0]-2 < (robot.center[0]+22) and (robot.center[1]-28) < top2Blue[1]+20 and top2Blue[1]-2 < (robot.center[1]+28):
    loadingTimer+=1
    if (loadingTimer==loadingLimit):
      loadingIntake = True

  #Background Colour
  screen.fill(gray)

  #Field Lines
  pygame.draw.line(screen, white, (0, 320*scale), (316*scale, 320*scale), 4) #Middle Line
  pygame.draw.line(screen, blue, ((316-50)*scale, (320+61)*scale), (316*scale, (320+61)*scale), 4) #Loading Station - BLUE
  pygame.draw.line(screen, blue, ((316-50)*scale, (320+61)*scale), ((316-50)*scale, (640-118)*scale), 4) #Loading Station - BLUE
  pygame.draw.line(screen, blue, ((316-50-59)*scale, (640-118)*scale), ((316-50)*scale, (640-118)*scale), 4) #Loading Station - BLUE
  pygame.draw.line(screen, red, ((316-50)*scale, (320-61)*scale), (316*scale, (320-61)*scale), 4) #Loading Station - RED
  pygame.draw.line(screen, red, ((316-50)*scale, (320-61)*scale), ((316-50)*scale, (118)*scale), 4) #Loading Station - RED
  pygame.draw.line(screen, red, ((316-50-59)*scale, (118)*scale), ((316-50)*scale, (118)*scale), 4) #Loading Station - RED
  pygame.draw.line(screen, red, ((316-50-59-59)*scale, (640-118)*scale), ((316-50-59)*scale, (640-118)*scale), 4) #Community - RED
  pygame.draw.line(screen, red, ((316-50-59-59)*scale, (640-118)*scale), ((316-50-59-59)*scale, (640-118-62)*scale), 4) #Community - RED
  pygame.draw.line(screen, red, ((316-50-59-59)*scale, (640-118-62)*scale), ((0)*scale, (640-118-62)*scale), 4) #Community - RED
  pygame.draw.line(screen, blue, ((316-50-59-59)*scale, (118)*scale), ((316-50-59)*scale, (118)*scale), 4) #Community - BLUE
  pygame.draw.line(screen, blue, ((316-50-59-59)*scale, (118)*scale), ((316-50-59-59)*scale, (118+62)*scale), 4) #Community - BLUE
  pygame.draw.line(screen, blue, ((316-50-59-59)*scale, (118+62)*scale), ((0)*scale, (118+62)*scale), 4) #Community - BLUE
  pygame.draw.line(screen, black, ((316-50-59)*scale, (118+2)*scale), ((316-50-59)*scale, (0)*scale), 5) #Barrier BLUE SIDE
  pygame.draw.line(screen, white, ((316-50-59+4)*scale, (118+2)*scale), ((316-50-59+4)*scale, (118-42)*scale), 6) #Barrier BLUE SIDE
  pygame.draw.line(screen, white, ((316-50-59-5)*scale, (118+2)*scale), ((316-50-59-5)*scale, (118-42)*scale), 6) #Barrier BLUE SIDE
  pygame.draw.line(screen, black, ((316-50-59)*scale, (640-118-2)*scale), ((316-50-59)*scale, (640)*scale), 5) #Barrier RED SIDE
  pygame.draw.line(screen, white, ((316-50-59+4)*scale, (640-118-2)*scale), ((316-50-59+4)*scale, (640-118+42)*scale), 6) #Barrier RED SIDE
  pygame.draw.line(screen, white, ((316-50-59-5)*scale, (640-118-2)*scale), ((316-50-59-5)*scale, (640-118+42)*scale), 6) #Barrier RED SIDE

  pygame.draw.rect(screen, lightgray, pygame.Rect(0, 0, (206)*scale, 6*scale)) #Grid BLUE SIDE
  pygame.draw.rect(screen, blue, pygame.Rect(0, 6*scale, (31)*scale, 40*scale)) #Grid BLUE SIDE
  pygame.draw.rect(screen, lightgray, pygame.Rect(31*scale, 6*scale, (17)*scale, 40*scale)) #Grid BLUE SIDE
  pygame.draw.rect(screen, blue, pygame.Rect(48*scale, 6*scale, (23)*scale, 40*scale)) #Grid BLUE SIDE
  pygame.draw.rect(screen, darkgray, pygame.Rect(71*scale, 6*scale, (23)*scale, 40*scale)) #Grid BLUE SIDE
  pygame.draw.rect(screen, lightgray, pygame.Rect(94*scale, 6*scale, (17)*scale, 40*scale)) #Grid BLUE SIDE
  pygame.draw.rect(screen, darkgray, pygame.Rect(111*scale, 6*scale, (23)*scale, 40*scale)) #Grid BLUE SIDE
  pygame.draw.rect(screen, blue, pygame.Rect(134*scale, 6*scale, (23)*scale, 40*scale)) #Grid BLUE SIDE
  pygame.draw.rect(screen, lightgray, pygame.Rect(157*scale, 6*scale, (17)*scale, 40*scale)) #Grid BLUE SIDE
  pygame.draw.rect(screen, blue, pygame.Rect(174*scale, 6*scale, (32)*scale, 40*scale)) #Grid BLUE SIDE
  pygame.draw.line(screen, black, (31*scale, 6*scale), (48*scale, 6*scale), 4) #Cube node BLUE SIDE
  pygame.draw.line(screen, black, (31*scale, 25*scale), (48*scale, 25*scale), 4) #Cube node BLUE SIDE
  pygame.draw.line(screen, black, (94*scale, 6*scale), (111*scale, 6*scale), 4) #Cube node BLUE SIDE
  pygame.draw.line(screen, black, (94*scale, 25*scale), (111*scale, 25*scale), 4) #Cube node BLUE SIDE
  pygame.draw.line(screen, black, (157*scale, 6*scale), (174*scale, 6*scale), 4) #Cube node BLUE SIDE
  pygame.draw.line(screen, black, (157*scale, 25*scale), (174*scale, 25*scale), 4) #Cube node BLUE SIDE
  pygame.draw.circle(screen, black, (19*scale,16*scale), 5) #Cone node BLUE SIDE
  pygame.draw.circle(screen, black, (19*scale,33*scale), 5) #Cone node BLUE SIDE
  pygame.draw.circle(screen, black, (60*scale,16*scale), 5) #Cone node BLUE SIDE
  pygame.draw.circle(screen, black, (60*scale,33*scale), 5) #Cone node BLUE SIDE
  pygame.draw.circle(screen, black, (82*scale,16*scale), 5) #Cone node BLUE SIDE
  pygame.draw.circle(screen, black, (82*scale,33*scale), 5) #Cone node BLUE SIDE
  pygame.draw.circle(screen, black, (123*scale,16*scale), 5) #Cone node BLUE SIDE
  pygame.draw.circle(screen, black, (123*scale,33*scale), 5) #Cone node BLUE SIDE
  pygame.draw.circle(screen, black, (145*scale,16*scale), 5) #Cone node BLUE SIDE
  pygame.draw.circle(screen, black, (145*scale,33*scale), 5) #Cone node BLUE SIDE
  pygame.draw.circle(screen, black, (186*scale,16*scale), 5) #Cone node BLUE SIDE
  pygame.draw.circle(screen, black, (186*scale,33*scale), 5) #Cone node BLUE SIDE
  pygame.draw.line(screen, white, (0, 46*scale), (0, 60*scale), 3) #Hybrid node BLUE SIDE
  pygame.draw.line(screen, white, (31*scale, 46*scale), (31*scale, 60*scale), 3) #Hybrid node BLUE SIDE
  pygame.draw.line(screen, white, (48*scale, 46*scale), (48*scale, 60*scale), 3) #Hybrid node BLUE SIDE
  pygame.draw.line(screen, white, (71*scale, 46*scale), (71*scale, 60*scale), 3) #Hybrid node BLUE SIDE
  pygame.draw.line(screen, white, (94*scale, 46*scale), (94*scale, 60*scale), 3) #Hybrid node BLUE SIDE
  pygame.draw.line(screen, white, (111*scale, 46*scale), (111*scale, 60*scale), 3) #Hybrid node BLUE SIDE
  pygame.draw.line(screen, white, (134*scale, 46*scale), (134*scale, 60*scale), 3) #Hybrid node BLUE SIDE
  pygame.draw.line(screen, white, (157*scale, 46*scale), (157*scale, 60*scale), 3) #Hybrid node BLUE SIDE
  pygame.draw.line(screen, white, (174*scale, 46*scale), (174*scale, 60*scale), 3) #Hybrid node BLUE SIDE
  pygame.draw.line(screen, white, (204*scale, 46*scale), (204*scale, 60*scale), 3) #Hybrid node BLUE SIDE
  pygame.draw.line(screen, blue, (0, 60*scale), (205*scale, 60*scale), 4) #Hybrid node BLUE SIDE

  pygame.draw.rect(screen, lightgray, pygame.Rect(0, 634*scale, (206)*scale, 6*scale)) #Grid Red SIDE
  pygame.draw.rect(screen, red, pygame.Rect(0, 594*scale, (31)*scale, 40*scale)) #Grid Red SIDE
  pygame.draw.rect(screen, lightgray, pygame.Rect(31*scale, 594*scale, (17)*scale, 40*scale)) #Grid Red SIDE
  pygame.draw.rect(screen, red, pygame.Rect(48*scale, 594*scale, (23)*scale, 40*scale)) #Grid Red SIDE
  pygame.draw.rect(screen, darkgray, pygame.Rect(71*scale, 594*scale, (23)*scale, 40*scale)) #Grid Red SIDE
  pygame.draw.rect(screen, lightgray, pygame.Rect(94*scale, 594*scale, (17)*scale, 40*scale)) #Grid Red SIDE
  pygame.draw.rect(screen, darkgray, pygame.Rect(111*scale, 594*scale, (23)*scale, 40*scale)) #Grid Red SIDE
  pygame.draw.rect(screen, red, pygame.Rect(134*scale, 594*scale, (23)*scale, 40*scale)) #Grid Red SIDE
  pygame.draw.rect(screen, lightgray, pygame.Rect(157*scale, 594*scale, (17)*scale, 40*scale)) #Grid Red SIDE
  pygame.draw.rect(screen, red, pygame.Rect(174*scale, 594*scale, (32)*scale, 40*scale)) #Grid Red SIDE
  pygame.draw.line(screen, black, (31*scale, 633*scale), (48*scale, 633*scale), 4) #Cube node RED SIDE
  pygame.draw.line(screen, black, (31*scale, 614*scale), (48*scale, 614*scale), 4) #Cube node RED SIDE
  pygame.draw.line(screen, black, (94*scale, 633*scale), (111*scale, 633*scale), 4) #Cube node RED SIDE
  pygame.draw.line(screen, black, (94*scale, 614*scale), (111*scale, 614*scale), 4) #Cube node RED SIDE
  pygame.draw.line(screen, black, (157*scale, 633*scale), (174*scale, 633*scale), 4) #Cube node RED SIDE
  pygame.draw.line(screen, black, (157*scale, 614*scale), (174*scale, 614*scale), 4) #Cube node RED SIDE
  pygame.draw.circle(screen, black, (19*scale,624*scale), 5) #Cone node RED SIDE
  pygame.draw.circle(screen, black, (19*scale,607*scale), 5) #Cone node RED SIDE
  pygame.draw.circle(screen, black, (60*scale,624*scale), 5) #Cone node RED SIDE
  pygame.draw.circle(screen, black, (60*scale,607*scale), 5) #Cone node RED SIDE
  pygame.draw.circle(screen, black, (82*scale,624*scale), 5) #Cone node RED SIDE
  pygame.draw.circle(screen, black, (82*scale,607*scale), 5) #Cone node RED SIDE
  pygame.draw.circle(screen, black, (123*scale,624*scale), 5) #Cone node RED SIDE
  pygame.draw.circle(screen, black, (123*scale,607*scale), 5) #Cone node RED SIDE
  pygame.draw.circle(screen, black, (145*scale,624*scale), 5) #Cone node RED SIDE
  pygame.draw.circle(screen, black, (145*scale,607*scale), 5) #Cone node RED SIDE
  pygame.draw.circle(screen, black, (186*scale,624*scale), 5) #Cone node RED SIDE
  pygame.draw.circle(screen, black, (186*scale,607*scale), 5) #Cone node RED SIDE
  pygame.draw.line(screen, white, (0, 580*scale), (0, 594*scale), 3) #Hybrid node RED SIDE
  pygame.draw.line(screen, white, (31*scale, 580*scale), (31*scale, 594*scale), 3) #Hybrid node RED SIDE
  pygame.draw.line(screen, white, (48*scale, 580*scale), (48*scale, 594*scale), 3) #Hybrid node RED SIDE
  pygame.draw.line(screen, white, (71*scale, 580*scale), (71*scale, 594*scale), 3) #Hybrid node RED SIDE
  pygame.draw.line(screen, white, (94*scale, 580*scale), (94*scale, 594*scale), 3) #Hybrid node RED SIDE
  pygame.draw.line(screen, white, (111*scale, 580*scale), (111*scale, 594*scale), 3) #Hybrid node RED SIDE
  pygame.draw.line(screen, white, (134*scale, 580*scale), (134*scale, 594*scale), 3) #Hybrid node RED SIDE
  pygame.draw.line(screen, white, (157*scale, 580*scale), (157*scale, 594*scale), 3) #Hybrid node RED SIDE
  pygame.draw.line(screen, white, (174*scale, 580*scale), (174*scale, 594*scale), 3) #Hybrid node RED SIDE
  pygame.draw.line(screen, white, (204*scale, 580*scale), (204*scale, 594*scale), 3) #Hybrid node RED SIDE
  pygame.draw.line(screen, red, (0, 579*scale), (205*scale, 579*scale), 4) #Hybrid node RED SIDE

  #Display Stations
  screen.blit(stationScaleBlue, stationBlue)
  screen.blit(stationScaleRed, stationRed)

  #Display Cargo
  if (cargoSwitch == "cube"):
    screen.blit(cubeScale, groundBlue)
    screen.blit(cubeScale, top1Blue)
    screen.blit(cubeScale, top2Blue)
  
  if (cargoSwitch == "cone"):
    screen.blit(coneScale, groundBlue)
    screen.blit(coneScale, top1Blue)
    screen.blit(coneScale, top2Blue)

  if (robot.center[0] < 267 and robot.center[0] > 255):
    if (keysPressed[pygame.K_r]): #Grid Scoring Hybrid
      if i3==0:
        if cargoSwitch == "cube":
          i3 = 2
        else:
          i3 = 1
        loadingIntake=False
        loadingTimer=0
        timer-=outtakeLimit
    if (keysPressed[pygame.K_e]): #Grid Scoring Mid
      if i2==0:
        if cargoSwitch == "cube":
          i2 = 0
        else:
          i2 = 1
          loadingIntake=False
          loadingTimer=0
          timer-=outtakeLimit
    if (keysPressed[pygame.K_q]): #Grid Scoring High
      if i1==0:
        if cargoSwitch == "cube":
          i1 = 0
        else:
          i1 = 1
          loadingIntake=False
          loadingTimer=0
          timer-=outtakeLimit

  if (robot.center[0] < 235 and robot.center[0] > 225):
    if (keysPressed[pygame.K_r]): #Grid Scoring Hybrid 
      if h3==0:
        if cargoSwitch == "cube":
          h3 = 2
        else:
          h3 = 1
        loadingIntake=False
        loadingTimer=0
        timer-=outtakeLimit

    if (keysPressed[pygame.K_e]): #Grid Scoring Mid
      if h2==0:
        if cargoSwitch == "cone":
          h2 = 0
        else:
          h2 = 2
          loadingIntake=False
          loadingTimer=0
          timer-=outtakeLimit

    if (keysPressed[pygame.K_q]): #Grid Scoring High
      if h1==0:
        if cargoSwitch == "cone":
          h1 = 0
        else:
          h1 = 2
          loadingIntake=False
          loadingTimer=0
          timer-=outtakeLimit

  if (robot.center[0] < 211 and robot.center[0] > 194):
    if (keysPressed[pygame.K_r]): #Grid Scoring Hybrid 
      if g3==0:
        if cargoSwitch == "cube":
          g3 = 2
        else:
          g3 = 1
        loadingIntake=False
        loadingTimer=0
        timer-=outtakeLimit

    if (keysPressed[pygame.K_e]): #Grid Scoring Mid
      if g2==0:
        if cargoSwitch == "cube":
          g2 = 0
        else:
          g2 = 1
          loadingIntake=False
          loadingTimer=0
          timer-=outtakeLimit

    if (keysPressed[pygame.K_q]): #Grid Scoring High
      if g1==0:
        if cargoSwitch == "cube":
          g1 = 0
        else:
          g1 = 1
          loadingIntake=False
          loadingTimer=0
          timer-=outtakeLimit

  if (robot.center[0] < 181 and robot.center[0] > 164):
    if (keysPressed[pygame.K_r]): #Grid Scoring Hybrid 
      if f3==0:
        if cargoSwitch == "cube":
          f3 = 2
        else:
          f3 = 1
        loadingIntake=False
        loadingTimer=0
        timer-=outtakeLimit

    if (keysPressed[pygame.K_e]): #Grid Scoring Mid
      if f2==0:
        if cargoSwitch == "cube":
          f2 = 0
        else:
          f2 = 1
          loadingIntake=False
          loadingTimer=0
          timer-=outtakeLimit

    if (keysPressed[pygame.K_q]): #Grid Scoring High
      if f1==0:
        if cargoSwitch == "cube":
          f1 = 0
        else:
          f1 = 1
          loadingIntake=False
          loadingTimer=0
          timer-=outtakeLimit

  if (robot.center[0] < 152 and robot.center[0] > 135):
    if (keysPressed[pygame.K_r]): #Grid Scoring Hybrid 
      if e3==0:
        if cargoSwitch == "cube":
          e3 = 2
        else:
          e3 = 1
        loadingIntake=False
        loadingTimer=0
        timer-=outtakeLimit
      
    if (keysPressed[pygame.K_e]): #Grid Scoring Mid
      if e2==0:
        if cargoSwitch == "cone":
          e2 = 0
        else:
          e2 = 2
          loadingIntake=False
          loadingTimer=0
          timer-=outtakeLimit

    if (keysPressed[pygame.K_q]): #Grid Scoring High
      if e1==0:
        if cargoSwitch == "cone":
          e1 = 0
        else:
          e1 = 2
          loadingIntake=False
          loadingTimer=0
          timer-=outtakeLimit

  if (robot.center[0] < 127 and robot.center[0] > 105):
    if (keysPressed[pygame.K_r]): #Grid Scoring Hybrid 
      if d3==0:
        if cargoSwitch == "cube":
          d3 = 2
        else:
          d3 = 1
        loadingIntake=False
        loadingTimer=0
        timer-=outtakeLimit

    if (keysPressed[pygame.K_e]): #Grid Scoring Mid
      if d2==0:
        if cargoSwitch == "cube":
          d2 = 0
        else:
          d2 = 1
          loadingIntake=False
          loadingTimer=0
          timer-=outtakeLimit

    if (keysPressed[pygame.K_q]): #Grid Scoring High
      if d1==0:
        if cargoSwitch == "cube":
          d1 = 0
        else:
          d1 = 1
          loadingIntake=False
          loadingTimer=0
          timer-=outtakeLimit

  if (robot.center[0] < 96 and robot.center[0] > 75):
    if (keysPressed[pygame.K_r]): #Grid Scoring Hybrid 
      if c3==0:
        if cargoSwitch == "cube":
          c3 = 2
        else:
          c3 = 1
        loadingIntake=False
        loadingTimer=0
        timer-=outtakeLimit

    if (keysPressed[pygame.K_e]): #Grid Scoring Mid
      if c2==0:
        if cargoSwitch == "cube":
          c2 = 0
        else:
          c2 = 1
          loadingIntake=False
          loadingTimer=0
          timer-=outtakeLimit

    if (keysPressed[pygame.K_q]): #Grid Scoring High
      if c1==0:
        if cargoSwitch == "cube":
          c1 = 0
        else:
          c1 = 1
          loadingIntake=False
          loadingTimer=0
          timer-=outtakeLimit

  if (robot.center[0] < 63 and robot.center[0] > 49):
    if (keysPressed[pygame.K_r]): #Grid Scoring Hybrid 
      if b3==0:
        if cargoSwitch == "cube":
          b3 = 2
        else:
          b3 = 1
        loadingIntake=False
        loadingTimer=0
        timer-=outtakeLimit
        
    if (keysPressed[pygame.K_e]): #Grid Scoring Mid
      if b2==0:
        if cargoSwitch == "cone":
          b2 = 0
        else:
          b2 = 2
          loadingIntake=False
          loadingTimer=0
          timer-=outtakeLimit

    if (keysPressed[pygame.K_q]): #Grid Scoring High
      if b1==0:
        if cargoSwitch == "cone":
          b1 = 0
        else:
          b1 = 2
          loadingIntake=False
          loadingTimer=0
          timer-=outtakeLimit

  if (robot.center[0] < 37 and robot.center[0] > 23):
    if (keysPressed[pygame.K_r]): #Grid Scoring Hybrid
      if a3==0:
        if cargoSwitch == "cube":
          a3 = 2
        else:
          a3 = 1
        loadingIntake=False
        loadingTimer=0
        timer-=outtakeLimit

    if (keysPressed[pygame.K_e]): #Grid Scoring Mid
      if a2==0:
        if cargoSwitch == "cube":
          a2 = 0
        else:
          a2 = 1
          loadingIntake=False
          loadingTimer=0
          timer-=outtakeLimit

    if (keysPressed[pygame.K_q]): #Grid Scoring High
      if a1==0:
        if cargoSwitch == "cube":
          a1 = 0
        else:
          a1 = 1
          loadingIntake=False
          loadingTimer=0
          timer-=outtakeLimit

  timer -= 1/80

  #Display Time
  if (timer>0):
    screen.blit(font.render(str(round(timer, 2)), True, white), (41, 755))
    #Display Robot
    screen.blit(robotScale, robot)
    lastX = robot[0]
    lastY = robot[1]

  else:
    screen.blit(font.render("Match Over", True, white), (41, 755))
    screen.blit(robotScale, (lastX, lastY))

  if (timer<-15):
    running = False
  
  #Display Cargo on Robot
  if (loadingIntake and cargoSwitch=="cube"):
    screen.blit(cubeScale, (robot.center[0]-8, robot.center[1]-8))
  elif(loadingIntake and cargoSwitch=="cone"):
      screen.blit(coneScale, (robot.center[0]-8, robot.center[1]-8))

  #Placing Cargo On Grid
  if (i3 == 2):
    screen.blit(cubeScale, (256, 65))
  if (i3 == 1):
    screen.blit(coneScale, (256, 65))

  if (i2 == 2):
    screen.blit(cubeScale, (256, 38))
  if (i2 == 1):
    screen.blit(coneScale, (256, 38))

  if (i1 == 2):
    screen.blit(cubeScale, (256, 13))
  if (i1 == 1):
    screen.blit(coneScale, (256, 13))

  if (h3 == 2):
    screen.blit(cubeScale, (223, 65))
  if (h3 == 1):
    screen.blit(coneScale, (223, 65))

  if (h2 == 2):
    screen.blit(cubeScale, (223, 38))
  if (h2 == 1):
    screen.blit(coneScale, (223, 38))

  if (h1 == 2):
    screen.blit(cubeScale, (223, 13))
  if (h1 == 1):
    screen.blit(coneScale, (223, 13))

  if (g3 == 2):
    screen.blit(cubeScale, (195, 65))
  if (g3 == 1):
    screen.blit(coneScale, (195, 65))

  if (g2 == 2):
    screen.blit(cubeScale, (195, 38))
  if (g2 == 1):
    screen.blit(coneScale, (195, 38))

  if (g1 == 2):
    screen.blit(cubeScale, (195, 13))
  if (g1 == 1):
    screen.blit(coneScale, (195, 13))

  if (f3 == 2):
    screen.blit(cubeScale, (158, 65))
  if (f3 == 1):
    screen.blit(coneScale, (158, 65))

  if (f2 == 2):
    screen.blit(cubeScale, (158, 38))
  if (f2 == 1):
    screen.blit(coneScale, (158, 38))

  if (f1 == 2):
    screen.blit(cubeScale, (158, 13))
  if (f1 == 1):
    screen.blit(coneScale, (158, 13))

  if (e3 == 2):
    screen.blit(cubeScale, (133, 65))
  if (e3 == 1):
    screen.blit(coneScale, (133, 65))

  if (e2 == 2):
    screen.blit(cubeScale, (133, 38))
  if (e2 == 1):
    screen.blit(coneScale, (133, 38))

  if (e1 == 2):
    screen.blit(cubeScale, (133, 13))
  if (e1 == 1):
    screen.blit(coneScale, (133, 13))

  if (d3 == 2):
    screen.blit(cubeScale, (104, 65))
  if (d3 == 1):
    screen.blit(coneScale, (104, 65))

  if (d2 == 2):
    screen.blit(cubeScale, (104, 38))
  if (d2 == 1):
    screen.blit(coneScale, (104, 38))

  if (d1 == 2):
    screen.blit(cubeScale, (104, 13))
  if (d1 == 1):
    screen.blit(coneScale, (104, 13))

  if (c3 == 2):
    screen.blit(cubeScale, (74, 65))
  if (c3 == 1):
    screen.blit(coneScale, (74, 65))

  if (c2 == 2):
    screen.blit(cubeScale, (74, 38))
  if (c2 == 1):
    screen.blit(coneScale, (74, 38))

  if (c1 == 2):
    screen.blit(cubeScale, (74, 13))
  if (c1 == 1):
    screen.blit(coneScale, (74, 13))

  if (b3 == 2):
    screen.blit(cubeScale, (48, 65))
  if (b3 == 1):
    screen.blit(coneScale, (48, 65))

  if (b2 == 2):
    screen.blit(cubeScale, (48, 38))
  if (b2 == 1):
    screen.blit(coneScale, (48, 38))

  if (b1 == 2):
    screen.blit(cubeScale, (48, 13))
  if (b1 == 1):
    screen.blit(coneScale, (48, 13))

  if (a3 == 2):
    screen.blit(cubeScale, (21, 65))
  if (a3 == 1):
    screen.blit(coneScale, (21, 65))

  if (a2 == 2):
    screen.blit(cubeScale, (21, 38))
  if (a2 == 1):
    screen.blit(coneScale, (21, 38))

  if (a1 == 2):
    screen.blit(cubeScale, (21, 13))
  if (a1 == 1):
    screen.blit(coneScale, (21, 13))

  #Update Display
  pygame.display.flip()
  
  #Set to 80 FPS
  clock.tick(80)

#Pygame Quit
pygame.quit()
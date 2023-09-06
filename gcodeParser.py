import re
import math
def ParseFile(file):
    RapidFeedX = 500
    RapidFeedY = 500
    RapidFeedZ = 500
    lastpos = [0, 0, 0]
    Feedrate = 100
    time = 0
    XTarget, YTarget, ZTarget = None, None, None
    RTarget = None
    ITarget, JTarget, KTarget = None, None, None
    for line in file:
        line =line.upper().strip(' ')
        if line.startswith('('):
            continue
        elif line.startswith(';'):
            continue
        Commands = re.findall(r'[A-Za-z]*-?\d+\.\d+|-?\d+\.\d+|-?[A-Za-z]+\d+|-?\d+', line)
        Commands.reverse()
        for Item in Commands:
            try:
                if Item.startswith('F'):
                    Feedrate = float(Item.removeprefix('F'))
                elif Item.startswith('X'):
                    XTarget = float(Item.removeprefix('X'))
                elif Item.startswith('Y'):
                    YTarget = float(Item.removeprefix('Y'))
                elif Item.startswith('Z'):
                    ZTarget = float(Item.removeprefix('Z'))
                elif Item.startswith('I'):
                    ITarget = float(Item.removeprefix('I'))
                elif Item.startswith('J'):
                    JTarget = float(Item.removeprefix('J'))
                elif Item.startswith('K'):
                    KTarget = float(Item.removeprefix('K'))
                elif Item.startswith('R'):
                    RTarget = float(Item.removeprefix('R'))
                elif Item.startswith('P'):
                    PTarget = float(Item.removeprefix('P'))
                elif Item == 'G0':
                    XTarget, YTarget, ZTarget = (XTarget if XTarget else lastpos[0]), (YTarget if YTarget else lastpos[1]), (ZTarget if ZTarget else lastpos[2])
                    operationTime = math.sqrt(
                        ((XTarget - lastpos[0]) / RapidFeedX) ** 2 +
                        ((YTarget - lastpos[1]) / RapidFeedY) ** 2 +
                        ((ZTarget - lastpos[2]) / RapidFeedZ) ** 2)
                    lastpos = [(XTarget if XTarget else lastpos[0]), (YTarget if YTarget else lastpos[1]), (ZTarget if ZTarget else lastpos[2])]
                    time += operationTime
                    XTarget, YTarget, ZTarget = None, None, None
                elif Item == 'G1':
                    XTarget, YTarget, ZTarget = (XTarget if XTarget else lastpos[0]), (YTarget if YTarget else lastpos[1]), (ZTarget if ZTarget else lastpos[2])
                    operationTime = math.sqrt(
                        (XTarget - lastpos[0]) ** 2 +
                        (YTarget - lastpos[1]) ** 2 +
                        (ZTarget - lastpos[2]) ** 2)
                    lastpos = [(XTarget if XTarget else lastpos[0]), (YTarget if YTarget else lastpos[1]), (ZTarget if ZTarget else lastpos[2])]
                    time += operationTime
                    XTarget, YTarget, ZTarget = None, None, None
                elif Item == 'G2':
                    XTarget, YTarget, ZTarget = (XTarget if XTarget else lastpos[0]), (YTarget if YTarget else lastpos[1]), (ZTarget if ZTarget else lastpos[2])
                    Distance = math.sqrt(
                        (XTarget - lastpos[0]) ** 2 +
                        (YTarget - lastpos[1]) ** 2 +
                        (ZTarget - lastpos[2]) ** 2)
                    if RTarget:
                        radius = RTarget
                    else:
                        ITarget, JTarget, KTarget = (ITarget if ITarget else lastpos[0]), (JTarget if JTarget else lastpos[1]), (KTarget if KTarget else lastpos[2])
                        A = math.sqrt((lastpos[0] - ITarget)**2 + (lastpos[1] - JTarget)**2 + (lastpos[2] - KTarget)**2)
                        B = math.sqrt((ITarget - XTarget)**2 + (JTarget - YTarget)**2 + (KTarget - ZTarget)**2)
                        C = math.sqrt((XTarget - lastpos[0])**2 + (YTarget - lastpos[1])**2 + (ZTarget - lastpos[2])**2)
                        radius = (A * B * C) / math.sqrt((2 * A**2 * B**2 + 2 * B**2 * C**2 + 2 * C**2 * A**2) - (A**4 + B**4 + C**4)) 
                    angle = 2.0 * math.asin(Distance / ((2.0 * radius)+0.001))

                    # Convert the feedrate to angular speed in radians per second
                    angular_speed = (Feedrate / 60.0) / radius

                    # Calculate the time in seconds
                    time += angle / angular_speed
                    ITarget, JTarget, KTarget = None, None, None
                    lastpos = [XTarget, YTarget, ZTarget]
                    XTarget, YTarget, ZTarget = None, None, None
                    RTarget = None
                elif Item == 'G3':
                    XTarget, YTarget, ZTarget = (XTarget if XTarget else lastpos[0]), (YTarget if YTarget else lastpos[1]), (ZTarget if ZTarget else lastpos[2])
                    Distance = math.sqrt(
                        (XTarget - lastpos[0]) ** 2 +
                        (YTarget - lastpos[1]) ** 2 +
                        (ZTarget - lastpos[2]) ** 2)
                    if RTarget:
                        radius = RTarget
                    else:
                        ITarget, JTarget, KTarget = (ITarget if ITarget else lastpos[0]), (JTarget if JTarget else lastpos[1]), (KTarget if KTarget else lastpos[2])
                        A = math.sqrt((lastpos[0] - ITarget)**2 + (lastpos[1] - JTarget)**2 + (lastpos[2] - KTarget)**2)
                        B = math.sqrt((ITarget - XTarget)**2 + (JTarget - YTarget)**2 + (KTarget - ZTarget)**2)
                        C = math.sqrt((XTarget - lastpos[0])**2 + (YTarget - lastpos[1])**2 + (ZTarget - lastpos[2])**2)
                        radius = (A * B * C) / math.sqrt((2 * A**2 * B**2 + 2 * B**2 * C**2 + 2 * C**2 * A**2) - (A**4 + B**4 + C**4))
                    angle = 2.0 * math.asin(Distance / ((2.0 * radius)+0.001))

                    # Convert the feedrate to angular speed in radians per second
                    angular_speed = (Feedrate / 60.0) / radius

                    # Calculate the time in seconds
                    time += angle / angular_speed
                    ITarget, JTarget, KTarget = None, None, None
                    lastpos = [XTarget, YTarget, ZTarget]
                    XTarget, YTarget, ZTarget = None, None, None
                    RTarget = None
                elif Item == 'G4':
                    time += PTarget
                    PTarget = 0
                elif Item == 'G28':
                    time += 8 # Adds some time for movment
                elif Item == 'G30':
                    time += 8 # Adds some time for movment
            except Exception as error:
                print(error)
    return time
def seconds_to_mixed_units(seconds):
    # Calculate the number of days, hours, minutes, and remaining seconds
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)

    return f"{round(days)} days, {round(hours)} hours, {round(minutes)} minutes, {round(seconds)} seconds"
with open('./OperationFiles/1005.nc') as file:
    print(seconds_to_mixed_units(ParseFile(file)))
    
    
    
#3:19
    

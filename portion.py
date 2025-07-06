import pandas as pd

fullQun = 3
NAMES   = ['red', 'yellow', 'green', 'cyan', 'blue', 'purble', 'red', 'white', 'black']
RGB     = [(255, 0, 0), (255, 255, 0), (0, 255, 0), (0, 255, 255), (0, 0, 255), (255, 0, 255), (255, 0, 0)]
Hue     = [0, 60, 120, 180, 240, 300, 360]
df      = pd.DataFrame(columns = NAMES)
portion_values = [0, 0, 0, 0, 0, 0, 0, 0, 0]# 7 is white, 8 is black

def formula(maximum, t, dif):
    return (maximum - t) / 6 / dif + .5

def RGB2HSV( R, G, B ):
    R = R / 255
    G = G / 255
    B = B / 255
    
    maximum     = max(R, G, B)
    dif         = maximum - min(R, G, B)
    color       = 0
    saturation  = 0
    
    if not dif == 0:
        saturation = dif / maximum
        r = formula(maximum, R, dif)
        g = formula(maximum, G, dif)
        b = formula(maximum, B, dif)
        if maximum == R:
            color = b - g
        elif maximum == G:
            color = 1 / 3 + r - b
        elif maximum == B:
            color = 2 / 3 + g - r
    if color < 0:
        color = color + 1
    elif color > 1:
        color = color - 1
    return (round(360 * color), round(100 * saturation), round(100 * maximum))


def getRange(value):
    for i in range(0, len(Hue)):
        if value == Hue[i]:
            return -1, i 
        elif value < Hue[i]:
            return i-1, i 

def scale( val, mini, maxi ):
    return (val - mini)/(maxi - mini)

def colorsPortion(value):
    c1, c2 = getRange(value) 
    parts  = 1
    if not c1 == -1:
        h              = 0
        l              = []
        percentage     = round(scale( value, Hue[c1], Hue[c2] ), 1)
        inv_percentage = 1 - percentage
        if percentage == 0:
            return [[c1, 1]],parts
        
        if percentage > inv_percentage:
            parts = round( 1 / inv_percentage )
            h     = percentage / inv_percentage
            l.append([c2,h])
            l.append([c1,parts - h])
        else:
            parts = round( 1 / percentage )
            h     = inv_percentage /percentage
            l.append([c2,parts - h])
            l.append([c1,h])    
        return l,parts
    else:
        return [[c2, 1]],parts
    
def whitePortion(percentage, parts):
    inv_percentage = 1 - percentage
    return (inv_percentage * parts) / percentage

def blackPortion(percentage, parts):
    inv_percentage = 1 - percentage
    return (inv_percentage * parts) / percentage

def edit(colors):
    minqun = 1000000
    for color in colors:
        index, qun = color
        if qun < 0:
            qun = 0
        if (not qun == 0) and (qun < minqun):
            minqun = qun
    if minqun == 1000000:
        return
    
    multiple = round( 1 / minqun )
    for color in colors:
        index, qun = color
        color[1] = round(qun * multiple)
        portion_values[index] = color[1]

def percentage(colors, liter):
    sum = 0
    for color in colors:
        index, qun  = color
        sum         = sum + qun
    for color in colors:
        index, qun  = color
        color[1]    = (liter * qun)/sum
        portion_values[index] = color[1]

def editPortions():
    i = 0
    for v in portion_values:
        portion_values[i] = 0
        i = i + 1

def printPortions():
    i = 0
    for v in portion_values:
        print('{}: {}'.format(NAMES[i],v))
        i = i + 1
        
def addToDF():
    df.loc[len(df.index)] = portion_values

def addToExcel():
    df.to_excel('colors.xlsx', sheet_name='sheet')


def getColorsPortion( R, G, B ):
    editPortions()
    hue,saturation, value   = RGB2HSV( R, G, B )
    saturation              = scale(saturation, 0, 100)
    value                   = scale(value, 0, 100)
    print('h:{} s:{} v:{}'.format(hue,saturation, value) )
    colors                  = []
    if R == G == B == 255:#white
        portion_values[7] = 1
        colors.append([7,1])
    elif R == G == B == 0:#balck
        portion_values[8] = 1
        colors.append([8,1])
    else:
        colors, colorsPumbs     = colorsPortion(hue)
        whitePumbs              = whitePortion(saturation, colorsPumbs)
        colors.append([7,whitePumbs])
        blackPumbs              = blackPortion(value, colorsPumbs)
        colors.append([8,blackPumbs])
        edit(colors)
    printPortions()
    percentage(colors, fullQun)
    addToDF()
    addToExcel()
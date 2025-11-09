from __future__ import print_function, division
from math import sin

def applyTax(price=0.00,taxRate=0.0825):
    return formatCurrency(price + (price * taxRate))

def formatCurrency(price=0.00):
    return '{0:.2f}'.format(round(price*100.0)/100.0)

def padString(sToPad, padChar=' ', width=80, align='LEFT'):
    align = align.upper()
    if align == "RIGHT":
        padding = (max(width - len(sToPad),0))*padChar
        return sToPad+padding
    elif align == "CENTER":
        paddingL = (max(width - len(sToPad),0)//2)*padChar
        paddingR = (max(width - (len(sToPad) + len(paddingL)),0))*padChar
        return paddingL+sToPad+paddingR
    else:
        padding = (max(width - len(sToPad),0))*padChar
        return padding+sToPad

def tempToRGB(temp=0, minT=50, maxT=100):
    slope=(255/(maxT-minT))
    yInt=-slope*(maxT) + 255
    rVal = slope*temp + yInt
    gVal = sin((temp-minT)/((maxT - minT)/3.14159265))*255
    bVal = -slope*temp - yInt
    return (rVal,gVal,bVal)

def wrap(sToWrap, lWidth=80):
    words=sToWrap.split(' ')
    wrapped=""
    line=""
    for w in words:
        lineLen=len(line)+len(w)
        if lineLen > lWidth:
            wrapped+=line[:-1]+"\n"
        line+=w+" "
    wrapped+=line
    return wrapped

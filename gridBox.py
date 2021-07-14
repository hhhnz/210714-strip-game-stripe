import cv2
from PySide6 import QtGui
from PySide6.QtGui import QBrush

from gScene import GText


class GridBox:

    def __init__(self,topLX, topLY, bottomRX, bottomRY):
        self.topLeftX = topLX
        self.topLeftY = topLY
        self.bottomRightX = bottomRX
        self.bottomRightY = bottomRY
        self.matBox = None
        self.row =0
        self.column=0
        self.flagPatternFound=False
        self.canvasView = None
        self.canvasScene = None
        self.textCode = None
        self.samePatternAs = None
        self.mainWindow = None
    def clearPattern(self):
        self.flagPatternFound=False
        self.canvasScene.removeItem(self.textCode)
        self.canvasView.update()
    def showCode(self):
        w= self.bottomRightX-self.topLeftX
        h= self.bottomRightY-self.topLeftY
        if w<=h:
            textSize = round(w/4)
        else:
            textSize = round(h/4)
        if self.canvasScene is not None or self.canvasView is not None:
            self.textCode = GText(self.samePatternAs)
            self.textCode.setCode(self.samePatternAs)
            self.textCode.setScale(0.5)
            self.textCode.setMainWindow(self.mainWindow)
            #self.textCode = self.canvasScene.addText(self.samePatternAs, QtGui.QFont('Arial Black', textSize, QtGui.QFont.Light))
            self.canvasScene.addItem(self.textCode)
            self.textCode.setPos(self.topLeftX-textSize+2, self.topLeftY-textSize)
            self.textCode.setDefaultTextColor(QtGui.QColor("yellow"))
            #self.textCode.setColor(QtGui.QColor("green"))

    def getTopLeft(self):
        return self.topLeftX, self.topLeftY
    def getBottomRight(self):
        return self.bottomRightX, self.bottomRightY
    def __str__(self):
        return str(self.topLeftX)+","+str(self.topLeftY)+","+str(self.bottomRightX)+","+str(self.bottomRightY)
    def setMatBox (self,mat):
        self.matBox = mat
        pass
    def getMatBox(self):
        return self.matBox
    def setCoord(self,r,c):
        self.row=r
        self.column=c
    def getCoord(self):
        return self.row,self.column
    def getCoordString(self):
        return str(self.row)+"."+str(self.column)
    def setPattern(self,coord):
        self.flagPatternFound=True
        self.samePatternAs=coord

if __name__ == "__main__":
    gb1=GridBox(1,2,3,4)
    print(gb1.getTopLeft())
    print(gb1.getBottomRight())
    print (gb1)
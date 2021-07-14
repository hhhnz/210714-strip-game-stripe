import PySide6
from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import QGraphicsTextItem, QGraphicsScene, QMenu


class GScene(QGraphicsScene):
    itemRightClicked = QtCore.Signal(object)

class GText(QGraphicsTextItem):

    def mousePressEvent(self, event):
        self.saveOneAction = QtGui.QAction(QtGui.QIcon('saveFile32.png'), 'Save One Stripe',self)
        self.saveOneAction.setShortcut('Ctrl+Shift+S')
        self.saveOneAction.triggered.connect(self.actionSaveOne)
        if event.button() == QtCore.Qt.LeftButton:
            print ("txt left button clicked")
        if event.button() == QtCore.Qt.RightButton:
            menu = QMenu()
            menu.addAction(self.saveOneAction)
            menu.exec_(QtGui.QCursor.pos())

    def setMainWindow(self,mw):
        self.mainWin = mw
    def actionSaveOne(self):
        self.mainWin.actionSaveOne(self.code)
    def setCode(self,c):
        self.code = c


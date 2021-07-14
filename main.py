import sys
import random

import cv2
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QStatusBar, QPushButton, QMainWindow, QHBoxLayout, QVBoxLayout, QFrame, QTextEdit, \
    QSplitter, QWidget, QLabel, QLineEdit, QFileDialog, QGraphicsItem

from cvAction import CvAction
from gScene import GScene
from gridBox import GridBox


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.flagSSpriteClicked = False
        self.setWindowTitle("Road Fighter")
        self.createMenuBar()
        self.createStatusBar()
        self.createToolBar()
        self.cva = CvAction()
        self.currentViewScale = 1.0
        self.flagImageLoad = False
        self.flagGridDrawn = False
        self.listHLine = []
        self.listVLine = []
        self.list2dGridBox = []
        self.dictSprite = {}

    @QtCore.Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))

    def createStatusBar(self):
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage('Hello')
        self.initUI()

    def actionOpenImage(self):
        # TODO: check if image already load, and clean
        if self.flagSSpriteClicked:
            self.textedit.clear()
            self.dictSprite.clear()
            if self.flagSSpriteClicked:
                for row in self.list2dGridBox:
                    for cell in row:
                        cell.clearPattern()
            self.flagSSpriteClicked = False
        if self.flagGridDrawn:
            # remove all grid lines
            self.flagGridDrawn = False
            pass
        if self.flagImageLoad:
            self.flagImageLoad = False
            pass

        path_to_file, _ = QFileDialog.getOpenFileName(self, self.tr("Load Image"), self.tr("."),
                                                      self.tr("Images (*.*)"))
        print(path_to_file)
        if path_to_file != "":
            self.cva.loadImage(path_to_file)

            self.image = self.cva.matOriginalImg  # cv mat image
            self.image = self.cva.cvToQImage(self.image)
            # self.topleft.setPixmap(QtGui.QPixmap.fromImage(self.image))
            self.scene.clear()
            w = self.image.width()
            h = self.image.height()
            pixMap = QPixmap.fromImage(self.image)
            self.scene.addPixmap(pixMap)
            self.view.fitInView(QRectF(0, 0, w, h), Qt.KeepAspectRatio)
            self.scene.update()
            self.statusBar.showMessage("image size: " + str(self.image.width()) + " * " + str(self.image.height()))
            self.flagImageLoad = True
        else:
            self.statusBar.showMessage("file open cancelled")

    def actionSaveAllStripe(self):
        fileName = QFileDialog.getSaveFileName(self, 'Save Stripes', '.',selectedFilter="*.png")
        if fileName[0]!='':
            print (fileName)
            for item in self.dictSprite.items():
                newFileName=fileName[0]+item[0]+".png"
                gb = item[1]
                cv2.imwrite(newFileName, gb.getMatBox())
        else:
            self.statusBar.showMessage("File save cancelled!")


    def createMenuBar(self):
        self.openAction = QtGui.QAction(QtGui.QIcon('openFile32.png'), 'Open', self)
        self.openAction.setShortcut('Ctrl+O')
        self.openAction.triggered.connect(self.actionOpenImage)
        self.saveStripeAction = QtGui.QAction(QtGui.QIcon('saveFileAll32.png'), 'Save All Stripe', self)
        self.saveStripeAction.setShortcut('Ctrl+Shift+S')
        self.saveStripeAction.triggered.connect(self.actionSaveAllStripe)

        self.exitAction = QtGui.QAction(QtGui.QIcon('exit24.png'), 'Exit', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.triggered.connect(self.close)
        menubar = self.menuBar()
        fileMenu = menubar.addMenu("&File")
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveStripeAction)
        fileMenu.addAction(self.exitAction)
    def actionSaveOne(self,code):
        print ("action save one in main window")
        fileName = QFileDialog.getSaveFileName(self, 'Save One Stripe', '.', selectedFilter="*.png")
        if fileName[0] != '':
            gb = self.dictSprite.get(code)
            newFileName = fileName[0] + code + ".png"
            cv2.imwrite(newFileName, gb.getMatBox())
        else:
            self.statusBar.showMessage("File save cancelled!")
    def createToolBar(self):
        toolbar = self.addToolBar('Tools')
        toolbar.addAction(self.openAction)
        toolbar.addAction(self.saveStripeAction)
        lbOffsetX = QLabel("Offset X")
        toolbar.addWidget(lbOffsetX)
        self.tbOffsetX = QLineEdit('0')
        self.tbOffsetX.setFixedWidth(30)
        toolbar.addWidget(self.tbOffsetX)
        lbOffsetY = QLabel("Offset Y")
        toolbar.addWidget(lbOffsetY)
        self.tbOffsetY = QLineEdit('0')
        self.tbOffsetY.setFixedWidth(30)
        toolbar.addWidget(self.tbOffsetY)
        # grid input
        lbGridX = QLabel("Grid X")
        toolbar.addWidget(lbGridX)
        self.tbGridX = QLineEdit('16')
        toolbar.addWidget(self.tbGridX)
        lbGridY = QLabel("Grid Y")
        toolbar.addWidget(lbGridY)
        self.tbGridY = QLineEdit('16')
        toolbar.addWidget(self.tbGridY)
        # add grid buttons
        self.btnDrawGrid = QPushButton("Draw Grid")
        toolbar.addWidget(self.btnDrawGrid)
        self.btnDrawGrid.clicked.connect(self.actionDrawGrid)

        # add zoom
        lbZoom = QLabel("zoom")
        toolbar.addWidget(lbZoom)
        self.leditZoomRatio = QLineEdit('1.0')
        toolbar.addWidget(self.leditZoomRatio)
        self.btnZoom = QPushButton("Zoom", self)
        self.btnZoom.clicked.connect(self.actionZoomClicked)
        toolbar.addWidget(self.btnZoom)
        self.btnZoomFit = QPushButton("Zoom to Fit", self)
        self.btnZoomFit.clicked.connect(self.actionZoomFitClicked)
        toolbar.addWidget(self.btnZoomFit)
        # add strip sprite
        self.btnSSprite = QPushButton("Strip Sprite", self)
        self.btnSSprite.clicked.connect(self.actionSSpriteClicked)
        toolbar.addWidget(self.btnSSprite)

    def actionZoomFitClicked(self):
        vw = self.view.width()
        vh = self.view.height()
        w, h, _ = self.cva.getMat().shape
        scale = 1
        if w >= h:
            scale = round(vw / w)
            r = (float(scale / self.currentViewScale))
        else:
            scale = round(vh / h)
            r = (float(scale / self.currentViewScale))
        self.view.scale(r, r)

        self.leditZoomRatio.setText(str(scale))
        self.currentViewScale = float(self.leditZoomRatio.text())
    def actionSSpriteClicked(self):
        self.textedit.clear()
        self.dictSprite.clear()
        if self.flagSSpriteClicked:
            for row in self.list2dGridBox:
                for cell in row:
                    cell.clearPattern()
        if self.flagGridDrawn:
            # print("strip sprite clicked")
            list2dGridBox2 = self.list2dGridBox.copy()
            for row in self.list2dGridBox:
                for cell in row:
                    template = cell.getMatBox()
                    r, c = cell.getCoord()
                    # cv2.imshow(str(r)+"-"+str(c),template)
                    for r2 in list2dGridBox2:
                        for c2 in r2:
                            if not c2.flagPatternFound:
                                template2 = c2.getMatBox()
                                # diff = CvAction.compareMat(template, template2)
                                # TODO:pixel compare
                                diff = CvAction.pixelCompareMat(template, template2)
                                if diff <= 0.0:
                                    c2.setPattern(cell.getCoordString())
                                    # print(cell.getCoordString() + "vs" + c2.getCoordString() + " difference:" + str(
                                    # CvAction.compareMat(template, template2)))
                                    c2.showCode()
                                    # TODO: show pattern in gui view

                                    if cell.getCoordString() not in self.dictSprite:
                                        self.dictSprite[cell.getCoordString()] = cell
                                        self.showCellText(cell)
            self.flagSSpriteClicked = True
            self.statusBar.showMessage("total stripes found = " + str(self.dictSprite.__len__()))
        else:
            self.statusBar.showMessage("Please load image and draw grid first!")

    def showCellText(self, c):
        bText = c.getCoordString()
        # m = c.getMatBox()
        # print (m.shape)
        # cv2.imshow(bText,c.getMatBox())
        # bImage = CvAction.cvToQImage(m)
        self.textedit.append(bText)

    def actionZoomClicked(self):
        if (self.flagImageLoad):
            r = (float(self.leditZoomRatio.text()) / self.currentViewScale)
            self.view.scale(r, r)
            self.currentViewScale = float(self.leditZoomRatio.text())
        else:
            self.statusBar.showMessage("Please open an image first!")

    def removeAllFromScene(self, list):
        for o in list:
            self.scene.removeItem(o)
            self.view.update()
            del o

    def generateGridBox(self, sizeX, sizeY, rr, cc, offsetX, offsetY):
        self.list2dGridBox.clear()
        if offsetX == 0:
            noCol = cc
        else:
            noCol = cc - 1
        if offsetY == 0:
            noRow = rr
        else:
            noRow = rr - 1
        for r in range(noRow):
            listRow = []
            for c in range(noCol):
                topX = c * sizeX + offsetX
                topY = r * sizeY + offsetY
                bottomX = (c + 1) * sizeX + offsetX
                bottomY = (r + 1) * sizeY + offsetY
                gb = GridBox(topX, topY, bottomX, bottomY)
                gb.mainWindow = self
                gb.canvasView = self.view
                gb.canvasScene = self.scene
                m = self.cva.getMat().copy()
                w, h, _ = m.shape
                print(str(topX) + " " + str(topY) + " " + str(bottomX) + " " + str(bottomY))
                print(str(w) + " " + str(h))
                crop = m[topY:bottomY, topX:bottomX]

                gb.setMatBox(crop)
                gb.setCoord(r, c)

                # cv2.imshow(gb.getCoordString(), gb.getMatBox())
                # cv2.waitKey(0)
                listRow.append(gb)

            self.list2dGridBox.append(listRow)

    def actionDrawGrid(self):
        if self.flagSSpriteClicked:
            for row in self.list2dGridBox:
                for cell in row:
                    cell.clearPattern()
        if (self.flagGridDrawn):
            self.removeAllFromScene(self.listHLine)
            self.removeAllFromScene(self.listVLine)
        self.view.update()
        if (self.flagImageLoad):
            totalW = self.image.width()
            totalH = self.image.height()
            gridW = int(self.tbGridX.text())
            gridH = int(self.tbGridY.text())
            offsetX = int(self.tbOffsetX.text())
            offsetY = int(self.tbOffsetY.text())
            self.listVLine.clear()
            self.listHLine.clear()
            if gridW == 0 or gridH == 0:
                self.statusBar.showMessage("Grid size can not be zero!")
                return
            totalHLine = round(totalH / gridH)
            print(totalHLine)
            totalVLine = round(totalW / gridW)
            print(totalVLine)
            if offsetX != 0:
                pass
                # totalVLine -= 1
            if offsetY != 0:
                pass
                # totalHLine -= 1

            for i in range(totalHLine):
                line = self.scene.addLine(0, (i * gridH) + offsetY, totalW, (i * gridH) + offsetY)
                # print("0" + "," + str(i * gridH) + "," + str(totalW) + "," + str(i * gridH))
                pen = QtGui.QPen()
                pen.setColor(QtGui.QColor("red"))
                line.setPen(pen)
                self.listHLine.append(line)
            for j in range(totalVLine):
                line = self.scene.addLine((j * gridW) + offsetX, 0, (j * gridW) + offsetX, totalH)
                pen = QtGui.QPen()
                pen.setColor(QtGui.QColor("red"))
                line.setPen(pen)
                self.listVLine.append(line)
            self.generateGridBox(gridW, gridH, totalHLine, totalVLine, offsetX, offsetY)
            # print(self.list2dGridBox)
            self.flagGridDrawn = True
        else:
            self.statusBar.showMessage("Please open an image first!")

    def initUI(self):
        w = QWidget()
        hbox = QHBoxLayout(w)
        # self.topleft = QtWidgets.QLabel("image")
        # self.topleft.setFrameShape(QFrame.StyledPanel)
        #self.scene = QtWidgets.QGraphicsScene(QtCore.QRectF(0, 0, 300, 300))
        self.scene = GScene(QtCore.QRectF(0, 0, 300, 300))
        self.view = QtWidgets.QGraphicsView(
            self.scene, alignment=QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft
        )
        # self.view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # self.view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.view.setBackgroundBrush(
            QtWidgets.QApplication.style()
                .standardPalette()
                .brush(QtGui.QPalette.Window)
        )
        # line1 = self.scene.addLine(0, 0, 200, 100)
        # line2 = self.scene.addLine(0, 100, 200, 0)
        # pen = QtGui.QPen()
        # pen.setDashPattern((4, 4))
        # pen.setColor(QtGui.QColor("red"))
        # line2.setPen(pen)

        # rect = self.scene.addRect(QtCore.QRectF(QtCore.QPointF(50, 25), QtCore.QPointF(150, 75)))
        # rect.setBrush(QtGui.QColor("blue"))
        # rect.setFlag(QGraphicsItem.ItemIsMovable)
        # self.topleft.resize(200, 100)
        bottom = QFrame()
        bottom.setFrameShape(QFrame.StyledPanel)
        splitter1 = QSplitter(Qt.Horizontal)
        self.textedit = QTextEdit()
        splitter1.addWidget(self.view)
        splitter1.addWidget(self.textedit)
        splitter1.setSizes([300, 100])
        splitter2 = QSplitter(Qt.Vertical)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(bottom)
        splitter2.setSizes([300, 100])
        hbox.addWidget(splitter2)
        w.setLayout(hbox)
        self.setCentralWidget(w)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyApp()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())

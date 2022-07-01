import sys
import turtle

import tree
import koch
import gosper

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic

qtCreatorFile = "GUI.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class main(QMainWindow, Ui_MainWindow):

    def tree_creation(self):
        iteration = int(self.tree_iter.text())
        length = int(self.tree_length.text())
        angle = int(self.tree_angle.text())

        inst = tree.createLSystem(iteration, "M")
        print(inst)

        turtle.TurtleScreen._RUNNING = True
        t = turtle.Turtle()  # setting up turtle
        wn = turtle.Screen()
        wn.screensize(1500, 1500)
        t.left(90)
        t.penup()
        t.goto(0, -300)
        t.speed(10)

        tree.drawLsystem(t, inst, angle, length)


    def koch_creation(self):
        iteration = int(self.koch_iter.text())
        length = int(self.koch_length.text())
        angle = int(self.koch_angle.text())

        inst = koch.createLSystem(iteration, "F")
        print(inst)

        turtle.TurtleScreen._RUNNING = True
        t = turtle.Turtle()  # setting up turtle
        wn = turtle.Screen()
        wn.screensize(1500, 1500)
        t.penup()
        t.goto(-400, 0)
        t.speed(10)

        koch.drawLsystem(t, inst, angle, length)

    def gosper_creation(self):
        iteration = int(self.gosper_iter.text())
        length = int(self.gosper_length.text())
        angle = int(self.gosper_angle.text())

        inst = gosper.createLSystem(iteration, "L")  # create the string with number of iterations and axiom
        print(inst)
        turtle.TurtleScreen._RUNNING = True
        t = turtle.Turtle()  # setting up turtle
        wn = turtle.Screen()
        wn.screensize(1500, 1500)
        t.left(90)
        t.penup()
        t.goto(0, 0)
        t.speed(10)

        gosper.drawLsystem(t, inst, angle, length)

    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.tree_generate.clicked.connect(self.tree_creation)
        self.koch_generate.clicked.connect(self.koch_creation)
        self.gosper_generate.clicked.connect(self.gosper_creation)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = main()
    window.show()
    app.exec_()
    del window, app

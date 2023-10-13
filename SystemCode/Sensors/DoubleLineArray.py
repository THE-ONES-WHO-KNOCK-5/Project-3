import LineSensor

class DoubleLineArray(object):
    # stores sensors here
    lineL = None
    lineR = None
    def __int__(self, portL, portR):
        self.lineR = LineSensor(portR)
        self.lineL = LineSensor(portL)

    def isRightOnLine(self):
        return self.lineR.getValue()

    def isLeftOnLine(self):
        return self.lineL.getValue()
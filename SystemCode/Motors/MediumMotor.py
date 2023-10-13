import GenericMotor
class MediumMotor(GenericMotor):
    maxRPM = 250

    def setPower(self, power):
        boundedVal = max([min([power,1.0]), -1.0])
        self.setRPM(boundedVal * self.maxRPM)
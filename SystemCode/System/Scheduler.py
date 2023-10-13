from SystemCode.System.Commands.GenericCommand import GenericCommand
class Scheduler(object):
    commandList = []

    def scheduleCommand(self, command: GenericCommand):
        self.commandList.append(command)

    def executeList(self):
        for i in self.commandList:
            i.execute()

    def isFinished(self):
        newList = []
        for i in self.commandList:
            if not i.isFinished():
                newList.append(i)
            else:
                i.end(False)
        self.commandList = newList

    def killCommands(self):
        for i in self.commandList:
            i.end(True)
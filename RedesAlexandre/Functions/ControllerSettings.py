from random import randint


class Controller:
    def __init__(self, idController, ipController, port, sensorResponse, sensorResponseTolerance, danger, sensorErro,
                 StructSize,
                 sensorPacket):
        self.idController = idController
        self.ipController = ipController
        self.port = port
        self.danger = danger
        self.conexao = None
        self.sensorResponse = sensorResponse
        self.sensorErro = sensorErro
        self.placeCode = None
        self.placeName = None
        self.sensorPacket = sensorPacket
        self.StructSize = StructSize
        self.sensorResponseTolerance = sensorResponseTolerance
        self.workday = True
        self.controllerErro = 0
        self.dangerCode = False
        self.timeNow = None
        self.message = ""
        self.sensores = {}

    def getDangerCode(self):
        return self.dangerCode

    def setDangerCode(self, code):
        self.dangerCode = code

    def getId(self):
        return self.idController

    def getIpController(self):
        return self.ipController

    def getWorkday(self):
        return self.workday

    def getPort(self):
        return self.port

    def getTolerance(self):
        return self.sensorResponseTolerance

    def getDanger(self):
        return self.danger

    def getSensorResponse(self):
        return self.sensorResponse

    def getSensorErro(self):
        return self.sensorErro

    def getPlaceCode(self):
        return self.placeCode

    def getPlaceName(self):
        return self.placeName

    def getSensorPacket(self):
        return self.sensorPacket

    def getStructSize(self):
        return self.StructSize

    def setPlaceCode(self, code):
        self.placeCode = code

    def setPlaceName(self, name):
        self.placeName = name

    def setIdController(self, id):
        self.idController = id

    def getControllerErro(self):
        return self.controllerErro

    def addControllerErro(self):
        self.controllerErro +=1

    def cleanControllerErro(self):
        self.controllerErro = 0

    def setWorkDay(self, value):
        self.workday = value

    def setTime(self, tempo):
        self.timeNow = tempo

    def getTime(self):
        return self.timeNow

    def getMessage(self):
        return self.message

    def setMessage(self, message):
        self.message = message

    def getSensor(self, chave):
        return self.sensores[chave]

    def setSensor(self, chave, valor):
        if chave not in self.sensores:
            self.sensores[chave] = valor

    def getSensores(self):
        return self.sensores

    def setConexao(self, conn):
        self.conexao = conn

    def getConexao(self):
        return self.conexao


def newController():
    file = open("Settings/controllerSettings.txt", "rt")
    lists = []
    txt = file.read().split('\n')

    for i in range(len(txt)):
        if ("<CONTROLLER>" in txt[i]):
            for j in range(i + 1, len(txt)):
                dado = txt[j].strip().split('\'')

                if ("IP_CONTROLLER" in txt[j]):
                    lists.append(dado[1])
                elif ("PORT_SENSOR" in txt[j]):
                    lists.append(int(dado[1]))
                elif ("SENSOR_RESPONSE" in txt[j]):
                    lists.append(int(dado[1]))
                elif ("SENSOR_RESPONSE_TOLERANCE" in txt[j]):
                    lists.append(int(dado[1]))
                elif ("DANGER" in txt[j]):
                    lists.append((int(dado[3]), int(dado[1])))
                elif ("SENSOR_ERRO" in txt[j]):
                    lists.append(int(dado[1]))
                elif ("[PACKET]" in txt[j]):
                    lists.append(int(dado[1]))
                    lists.append(dado[3])
                elif ("END" in txt[j]):
                    break

    controller = Controller(randint(1000, 60000), lists[0], lists[1], lists[2], lists[3], lists[4], lists[5], lists[6],
                            lists[7])
    return controller


def cadController(id):
    controller = newController()
    controller.setIdController(id)
    return controller
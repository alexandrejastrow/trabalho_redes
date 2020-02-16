from random import randint, uniform


class Sensor:

    def __init__(self, code, idSensor, typeSensor, sensorName, workAlone, response, minValue, maxValue, apparatusControl,
                 dependency):
        self.code = code
        self.idSensor = idSensor
        self.typeSensor = typeSensor
        self.vlSensor = 0
        self.sensorName = sensorName
        self.apparatusControl = apparatusControl
        self.dependency = dependency
        self.minValue = minValue
        self.maxValue = maxValue
        self.datSend = None
        self.workAlone = workAlone
        self.erro = 0
        self.cliente = None
        self.response = response

    def getResponse(self):
        return self.response

    def getCliente(self):
        return self.cliente

    def setCliente(self, cliente):
        self.cliente = cliente

    def getCode(self):
        return self.code

    def getWorkAlone(self):
        return self.workAlone

    def getId(self):
        return self.idSensor

    def getType(self):
        return self.typeSensor

    def getName(self):
        return self.sensorName

    def getApparatusControl(self):
        return self.apparatusControl

    def getDependency(self):
        return self.dependency

    def getErro(self):
        return self.erro

    def getMinValue(self):
        return self.minValue

    def getMaxValue(self):
        return self.maxValue

    def getDatSend(self):
        return self.datSend

    def getValue(self):
        return self.vlSensor

    def getRandomValue(self):

        if (self.code == 1):
            if (randint(0, 1000) >= 10):
                self.vlSensor = uniform(0, 45)
            else:
                self.vlSensor = uniform(-20, 1000)
        elif (self.code == 2):
            if (randint(0, 100) >= 10):
                self.vlSensor = uniform(0, 4000)
            else:
                self.vlSensor = uniform(2000, 4000)

        elif (self.code == 3):
            if (randint(0, 20) >= 10):
                self.vlSensor = 1
            else:
                self.vlSensor = randint(0, 1)

        return self.vlSensor

    def setValue(self, value):
        if value:
            if (self.getMinValue() <= value and self.getMaxValue() >= value):
                self.vlSensor = value
                return 1
            else:
                return 0
        else:
            self.vlSensor = 0

    def addErro(self):
        self.erro += 1

    def cleanErro(self):
        self.erro = 0

    def setId(self, value):
        self.idSensor = value

    def setDatSend(self, data):
        self.datSend = data


class Settings:
    def __init__(self, ip, port, packetType):
        self.ip = ip
        self.port = port
        self.packetType = packetType

    def getIp(self):
        return self.ip

    def getPort(self):
        return self.port

    def getPacketType(self):
        return self.packetType


def getSettings():
    file = open("Settings/sensorSettings.txt", "rt")
    lists = []
    txt = file.read().split('\n')

    for i in range(len(txt)):
        if ("<SETTINGS>" in txt[i]):
            for j in range(i + 1, len(txt)):
                dado = txt[j].strip().split('\'')
                if ("[IP]" in txt[j]):
                    lists.append(dado[1])
                elif ("[PORT]" in txt[j]):
                    lists.append(int(dado[1]))
                elif ("[PACKET]" in txt[j]):
                    lists.append(dado[1])
                elif ("[END]" in txt[j]):
                    break
    file.close()
    settings = Settings(lists[0], lists[1], lists[2])
    return settings


def newSensor(code):
    file = open("Settings/sensorSettings.txt", "rt")
    lists = []
    txt = file.read().split('\n')
    apparatus = []
    dependency = []

    for i in range(len(txt)):

        if ("<SENSOR_SETTINGS>" in txt[i]):
            for j in range(i + 1, len(txt)):
                dado = txt[j].strip().split('\'')

                if ("[SENSOR_CODE]" in txt[j] and code == int(dado[1])):
                    lists.append(code)
                    for k in range(j, len(txt)):

                        dado = txt[k].strip().split('\'')
                        if ("[ID_SENSOR]" in txt[k]):
                            lists.append(randint(int(dado[1]), int(dado[3])))
                        elif ("[SENSOR_NAME]" in txt[k]):
                            lists.append(dado[1])
                        elif ("[WORK_ALONE]" in txt[k]):
                            if (dado[1] == 'True'):
                                lists.append(True)
                            else:
                                lists.append(False)
                        elif ("[APPARATUS_CODE]" in txt[k]):
                            apparatus.append(int(dado[1]))
                        elif ("[RESPONSE]" in txt[k]):
                            lists.append(int(dado[1]))
                        elif ("[DEPENDENCY]" in txt[k]):
                            dependency.append(int(dado[1]))
                        elif ("[SENSOR_MIN_VALUE]" in txt[k]):
                            lists.append(int(dado[1]))
                        elif ("[SENSOR_MAX_VALUE]" in txt[k]):
                            lists.append(int(dado[1]))
                        elif ("[TYPE]" in txt[k]):
                            lists.append(dado[1])
                        elif ("[END]" in txt[k]):
                            break
    sensor = Sensor(lists[0], lists[1], lists[2], lists[3], lists[4], lists[5], lists[6], lists[7], apparatus, dependency)

    file.close()
    return sensor


def cadSensor(code, idSensor, vlSensor):
    sensor = newSensor(code)
    sensor.setId(idSensor)
    sensor.setValue(vlSensor)

    return sensor


def getSensores():
    file = open("Settings/sensorSettings.txt", "rt")
    lists = {}
    txt = file.read().split('\n')
    for i in range(len(txt)):

        if ("<SENSOR_SETTINGS>" in txt[i]):
            for j in range(i + 1, len(txt)):

                if ("[SENSOR_CODE]" in txt[j]):
                    for k in range(j, len(txt)):
                        if ("[SENSOR_NAME]" in txt[k]):
                            dado = txt[k].strip().split('\'')
                            lists[code] = (dado[1])
                        elif ("[END]" in txt[k]):
                            break
                        elif ("[SENSOR_CODE]" in txt[k]):
                            dado = txt[k].strip().split('\'')
                            code = int(dado[1])
    return lists

def setSensor(dicSensor, nameSensor):

    if (dicSensor):
        try:
            for elem in dicSensor:
                if (dicSensor[elem] == nameSensor):
                    sensor = newSensor(elem)
                    return sensor
        except:
            return -1
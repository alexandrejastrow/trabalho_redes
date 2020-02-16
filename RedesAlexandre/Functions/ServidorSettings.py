class Settings:
    def __init__(self, ipServer, portServer, response, maxErro,StructSize, controllerPacket, maxSizeStruct, textSeparator,
                 chaveValor, dicAlertas):
        self.ipServer = ipServer
        self.portServer = portServer
        self.response = response
        self.dangerCode = dicAlertas
        self.textSeparator = textSeparator
        self.controllerPacket = controllerPacket
        self.structSize = StructSize
        self.chaveValor = chaveValor
        self.maxSizeStruct = maxSizeStruct
        self.maxErro = maxErro
        self.diaUtil = 1

    def getDiaUtil(self):
        return self.diaUtil

    def getIpServer(self):
        return self.ipServer

    def getPacket(self):
        return self.controllerPacket

    def getMaxSizeStruct(self):
        return self.maxSizeStruct

    def getChaveValor(self):
        return self.chaveValor

    def getStructSize(self):
        return self.structSize

    def getPortServer(self):
        return self.portServer

    def getResponse(self):
        return self.response

    def getDangerCode(self, value):
        return self.dangerCode[value]

    def getTextSeparator(self):
        return self.textSeparator

    def getMaxErro(self):
        return self.maxErro

    def setDiaUtil(self):
        if(self.diaUtil):
            self.diaUtil = 0
        else:
            self.diaUtil = 1


def getServerSettings():
    file = open('Settings/serverSettings.txt', "rt")
    lists = []
    txt = file.read().split('\n')
    dicAlertas = {}
    for i in range(len(txt)):
        if ("<SETTINGS>" in txt[i]):
            for j in range(i + 1, len(txt)):
                dado = txt[j].strip().split('\'')
                if ("[IP_SERVIDOR]" in txt[j]):
                    lists.append(dado[1])
                elif ("[PORT_SERVIDOR]" in txt[j]):
                    lists.append(int(dado[1]))
                elif ("[SERVER_RESPONSE]" in txt[j]):
                    lists.append(int(dado[1]))
                elif ("[PACKET]" in txt[j]):
                    lists.append(int(dado[1]))
                    lists.append(str(dado[3]))
                elif ("[MAX_PACKET_SIZE]" in txt[j]):
                    lists.append(int(dado[1]))
                elif ("[CONTROLLER_ERRO]" in txt[j]):
                    lists.append(int(dado[1]))
                elif ("[TEXT_SEPARATOR]" in txt[j]):
                    lists.append(dado[1])
                elif ("[CHAVE:VALOR]" in txt[j]):
                    lists.append(dado[1])
                elif ("[END]" in txt[j]):
                    break

    for i in range(len(txt)):
        if ("<DANGERS>" in txt[i]):
            for j in range(i + 1, len(txt)):
                dado = txt[j].strip().split('\'')
                if (not "[END]" in txt[j]):
                    dicAlertas[int(dado[1])] = dado[3]
                else:
                    break


    file.close()
    settings = Settings(lists[0], lists[1], lists[2], lists[3], lists[4], lists[5], lists[6], lists[7], lists[8], dicAlertas)
    return settings

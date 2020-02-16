class Apparatus:
    def __init__(self, code, apparatusName, minValueOn, maxValueOn, minValueOff, maxValueOff):
        self.apparatusName = apparatusName
        self.code = code
        self.minValueOn = minValueOn
        self.maxValueOn = maxValueOn
        self.minValueOff = minValueOff
        self.maxValueOff = maxValueOff
        self.status = False
        self.onOff = {"ON": [], "OFF": []}

    def setTimeOn(self, time):
        self.onOff["ON"].append(time)

    def setTimeOff(self, time):
        self.onOff["OFF"].append(time)

    def getApparatusName(self):
        return self.apparatusName

    def getCode(self):
        return self.code

    def getMinValueOn(self):
        return self.minValueOn

    def getMaxValueOn(self):
        return self.maxValueOn

    def getMinValueOff(self):
        return self.minValueOff

    def getMaxValueOff(self):
        return self.maxValueOff

    def getStatus(self):
        return self.status

    def setOn(self):
        self.status = True

    def setOff(self):
        self.status = False

    def setStatus(self, valor, type):
        if (type == "BINARY"):
            self.status = valor
            return valor

        if (valor >= self.minValueOn and valor <= self.maxValueOn):
            self.status = 1
            return 1
        elif (valor >= self.minValueOff and valor <= self.maxValueOff):
            self.status = 0
            return 0


def newApparatus():
    file = open("Settings/apparatusSettings.txt", "rt")
    lista = {}
    txt = file.read().split('\n')

    for i in range(len(txt)):
        if ("<APPARATUS>" in txt[i]):
            for j in range(i + 1, len(txt)):
                aux = []
                if ("[APPARATUS_CODE]" in txt[j]):
                    dado = txt[j].strip().split('\'')
                    aux.append(int(dado[1]))
                    aux.append(dado[3])
                    for k in range(j + 1, len(txt)):

                        if ("[END]" in txt[k]):
                            break
                        else:

                            dado = txt[k].strip().split('\'')
                            aux.append(int(dado[1]))
                            aux.append(int(dado[3]))
                    aparatus = Apparatus(aux[0], aux[1], int(aux[2]), int(aux[3]), int(aux[4]), int(aux[5]))
                    lista[aux[0]] = aparatus
    file.close()
    return lista
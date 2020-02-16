from Functions import SensorSettings
from Functions.InterfaceFunctions import *
from Functions.ControllerSettings import *
from Functions.Places import getPlaces
from Functions.ApparatusSettings import *
from Functions.FunctionsSystema import *
from Functions.SensorSettings import *
from Functions.ServidorSettings import *
from functools import partial
import socket
import _thread
import time
import platform
from datetime import datetime, timedelta


def select() -> None:
    """Funcao responsavel selecionar o local da controladora.

    Funcao que nao possui retorno"""

    if dicInfos["CONTROLLER"].getPlaceCode() == None:
        dicInfos["CONTROLLER"].setPlaceName(system.getComboBox("PLACES"))
        text = "LOCAL: " + system.getComboBox("PLACES")
        system.setLabel("LOCAL", text=text)
        for elem in dicInfos["PLACES"]:
            if (system.getComboBox("PLACES") == dicInfos["PLACES"][elem]):
                dicInfos["CONTROLLER"].setPlaceCode(elem)
                break


def startApparatus() -> None:
    for elem in dicInfos["APPARATUS"]:
        pushBtn = partial(pushBtnApparatus, elem)
        system.addButtons(system.getContainers("APPARATUS"), dicInfos["APPARATUS"][elem].getApparatusName(), pushBtn,
                              width=120, text=dicInfos["APPARATUS"][elem].getApparatusName(), place=False, fill="x",
                              padx=1, pady=1)
        if(platform.system().upper() == "WINDOWS"):
            system.addLabels("APPARATUS_STATUS", dicInfos["APPARATUS"][elem].getApparatusName(), font=("Verdana", "12"),
                         text="OFF", background="red", fill="x", pady=2, padx=2, place=False)
        else:

            system.addLabels("APPARATUS_STATUS", dicInfos["APPARATUS"][elem].getApparatusName(), font=("Verdana", "14"),
                             text="OFF", background="red", fill="x", pady=3, padx=3, place=False)


def pushBtnApparatus(id: int) -> None:
    if dicInfos["CONTROLLER"].getWorkday():
        if dicInfos["APPARATUS"][id].getStatus():
            system.setLabel(dicInfos["APPARATUS"][id].getApparatusName(), background="red", text="OFF")
            system.addText("LOGS", "Equipamento: " + dicInfos["APPARATUS"][id].getApparatusName() + " Desligado! ")
            dicInfos["APPARATUS"][id].setOff()

        else:

            system.setLabel(dicInfos["APPARATUS"][id].getApparatusName(), background="green", text="ON")
            system.addText("LOGS", "Equipamento: " + dicInfos["APPARATUS"][id].getApparatusName() + " Ligado! ")
            dicInfos["APPARATUS"][id].setOn()
    else:
        system.addText("LOGS", "Não foi possivel Ligar o Aparelho Consulte o Administrador do Sistema!!!")


def liga(Id: int, sensor: SensorSettings.Sensor) -> None:
    """Funcao responsavel por ''desligar'' o equipamento.

        :type sensor: Functions.SensorSettings.Sensor
        :type Id: int

    Funcao que nao possui retorno"""

    system.setLabel(dicInfos["APPARATUS"][Id].getApparatusName(), background="green", text="ON")
    dicInfos["APPARATUS"][Id].setOn()
    dicInfos["APPARATUS"][Id].setTimeOn(datetime.now())
    if sensor != None:
        system.addText("LOGS", sensor.getName() + " valor: " + str(
            sensor.getValue()) + " Equipamento: " + str(
            dicInfos["APPARATUS"][Id].getApparatusName()) + " Ligado! ")


def desliga(Id: int, sensor: SensorSettings.Sensor) -> None:
    """Funcao responsavel por ''desligar'' o equipamento.

        :type sensor: Functions.SensorSettings.Sensor
        :type Id: int

    Funcao que nao possui retorno"""
    system.setLabel(dicInfos["APPARATUS"][Id].getApparatusName(), background="red", text="OFF")
    dicInfos["APPARATUS"][Id].setOff()
    dicInfos["APPARATUS"][Id].setTimeOff(datetime.now())
    if sensor != None:
        system.addText("LOGS", sensor.getName() + " valor: " + str(
            sensor.getValue()) + " Equipamento: " + str(
            dicInfos["APPARATUS"][Id].getApparatusName()) + " Desligado! ")
    else:
        system.addText("LOGS", str(dicInfos["APPARATUS"][Id].getApparatusName()) + " Desligado! ")


def trataTime():
    while True:
        for elem in dicInfos["SENSORES"]:
            time1 = dicInfos["SENSORES"][elem].getDatSend() + timedelta(seconds=dicInfos["CONTROLLER"].getTolerance() +
                                                                                dicInfos["SENSORES"][elem].getResponse())
            time2 = datetime.now()
            if time1 < time2:
                dicInfos["SENSORES"][elem].addErro()
        if dicInfos["CONTROLLER"].getSensorResponse() > 180:
            time.sleep(180)
        else:
            time.sleep(dicInfos["CONTROLLER"].getSensorResponse())


def trataErro():
    while True:
        try:
            for elem in dicInfos["SENSORES"]:

                if (dicInfos["SENSORES"][elem].getErro() >= dicInfos["CONTROLLER"].getSensorErro()):
                    dicInfos["ERRO_SENSOR"][elem] = dicInfos["SENSORES"][elem]
                    del dicInfos["SENSORES"][elem]
                    if dicConn["SERVIDOR"]:
                        mySend(dicConn["SERVIDOR"], dicInfos["SETTINGS"].getPacket(), dicInfos["CONTROLLER"].getId(),
                               time.time(), "alerta:2")
                        system.addText("LOGS", "Mensagem de Alerta SENSOR DEFEITUOSO enviada ao servidor: ")
        except:
            pass
        time.sleep(10)


def trataConn(sensor: SensorSettings.Sensor) -> None:
    if (dicInfos["CONTROLLER"].getDanger()[0] == sensor.getCode() and sensor.getValue() >
            dicInfos["CONTROLLER"].getDanger()[1]):
        dicInfos["CONTROLLER"].setDangerCode(True)
        if dicConn["SERVIDOR"]:
            mySend(dicConn["SERVIDOR"], dicInfos["SETTINGS"].getPacket(), dicInfos["CONTROLLER"].getId(), time.time(),
                   "alerta:1")
            system.addText("LOGS", "Mensagem de Alerta de INCENDIO enviada ao servidor: ")
        else:
            system.addText("LOGS", "PERIGO " + sensor.getName() + "  VALOR: " + str(sensor.getValue()))
    else:
        if dicInfos["CONTROLLER"].getWorkday():
            for equipamento in sensor.getApparatusControl():
                for sensors in dicInfos["SENSORES"]:
                    if (dicInfos["SENSORES"][sensors].getId() != sensor.getId()):
                        for equip in dicInfos["SENSORES"][sensors].getApparatusControl():
                            if (equipamento == equip):
                                if (dicInfos["APPARATUS"][equipamento].setStatus(sensor.getValue(), sensor.getType())
                                        and dicInfos["APPARATUS"][equip].setStatus(
                                            dicInfos["SENSORES"][sensors].getValue(),
                                            dicInfos["SENSORES"][
                                                sensors].getType())):
                                    liga(equipamento, sensor)
                                    pass
                                else:
                                    desliga(equipamento, sensor)
                                    pass


def pushBtnSensor(sensor: SensorSettings.Sensor) -> None:
    system.delText("SENSOR_SETTINGS")
    system.addText("SENSOR_SETTINGS", "", "", "", "   Nome do Sensor: " + sensor.getName(),
                   "   ID do Sensor " + str(sensor.getId()))
    if sensor.getErro() == dicInfos["CONTROLLER"].getSensorErro():
        system.addText("SENSOR_SETTINGS", "   Status do Sensor: OFF")
    else:
        system.addText("SENSOR_SETTINGS", "   Status do Sensor: ON")

    system.addText("SENSOR_SETTINGS", "   Ultimo Valor " + str(sensor.getValue())
                   , "   Codigo do Sensor " + str(sensor.getCode()), "   Erros do Sensor " + str(sensor.getErro())
                   , "   Valor Minimo " + str(sensor.getMinValue()), "   Valor Maximo " + str(sensor.getMaxValue())
                   , "   Equipamentos que o Sensor Controla:")
    for elem in sensor.getApparatusControl():
        for appa in dicInfos["APPARATUS"]:
            if elem == appa:
                system.addText("SENSOR_SETTINGS", "   " + dicInfos["APPARATUS"][elem].getApparatusName())


def newBtnSensor(sensor: SensorSettings.Sensor) -> None:
    pushBtn = partial(pushBtnSensor, sensor)
    name = sensor.getName() + " - " + str(sensor.getId())
    system.addButtons(system.getContainers("SENSORES"), name, pushBtn, text=name, width=120, place=False,
                      fill="x", padx=1, pady=1)
    if(platform.system().upper() == "WINDOWS"):
        system.addLabels("SENSORES_STATUS", sensor.getName(), font=("Verdana", "12"), text="ON",
                         background="green", fill="x", pady=2, padx=2, place=False)
    else:
        system.addLabels("SENSORES_STATUS", sensor.getName(), font=("Verdana", "14"), text="ON",
                         background="green", fill="x", pady=3, padx=3, place=False)
    system.addText("LOGS", "Sensor: " + dicInfos["SENSORES"][sensor.getId()].getName() +
                   "    conectado! " + "      ID: " + str(
        dicInfos["SENSORES"][sensor.getId()].getId()) + "      Valor: " +
                   str(dicInfos["SENSORES"][sensor.getId()].getValue()))


def sensorConexao(conexao: socket.socket, cliente: tuple) -> None:
    while True:
        try:
            values = receve(conexao, dicInfos["CONTROLLER"].getStructSize(), dicInfos["CONTROLLER"].getStructSize(),
                            dicInfos["CONTROLLER"].getSensorPacket())
            flag = True

            if values[0] not in dicInfos["SENSORES"] and values[0] not in dicInfos["ERRO_SENSOR"]:
                while flag:
                    dicInfos["MUTEX"].acquire()
                    dicInfos["SENSORES"][values[0]] = cadSensor(values[1], values[0], values[2])
                    dicInfos["SENSORES"][values[0]].setDatSend(datetime.now())
                    dicInfos["SENSORES"][values[0]].setCliente(cliente)
                    flag = False
                    newBtnSensor(dicInfos["SENSORES"][values[0]])
                    dicInfos["MUTEX"].release()

            elif values[0] in dicInfos["ERRO_SENSOR"] and values[0] not in dicInfos["SENSORES"]:
                while flag:
                    dicInfos["MUTEX"].acquire()
                    dicInfos["SENSORES"][values[0]] = dicInfos["ERRO_SENSOR"][values[0]]
                    del dicInfos["ERRO_SENSOR"][values[0]]
                    dicInfos["SENSORES"][values[0]].cleanErro()
                    dicInfos["SENSORES"][values[0]].setValue(values[2])
                    dicInfos["SENSORES"][values[0]].setDatSend(datetime.now())
                    flag = False
                    dicInfos["MUTEX"].release()
            else:
                while flag:
                    dicInfos["MUTEX"].acquire()
                    dicInfos["SENSORES"][values[0]].setValue(values[2])
                    dicInfos["SENSORES"][values[0]].setDatSend(datetime.now())
                    flag = False
                    dicInfos["MUTEX"].release()
            dicInfos["SENSORES"][values[0]].cleanErro()
            trataConn(dicInfos["SENSORES"][values[0]])

        except:
            time.sleep(dicInfos["SENSORES"][values[0]].getResponse())


# ------------------------------------#
def startConnServer():
    sens = ""
    for elem in dicInfos["SENSORES"]:
        sens += dicInfos["SENSORES"][elem].getName() + ":" + str(dicInfos["SENSORES"][elem].getId()) + "|"

    while True:
        mySend(dicConn["SERVIDOR"], dicInfos["SETTINGS"].getPacket(), dicInfos["CONTROLLER"].getId(), time.time(),
               "tipolocal:" +
               str(dicInfos["CONTROLLER"].getPlaceCode()) + "|" + sens)
        time.sleep(dicInfos["SETTINGS"].getResponse())


def offAll():
    for elem in dicInfos["APPARATUS"]:
        desliga(elem, None)


def receveServerMenssages():
    while True:
        try:
            values = receve(dicConn["SERVIDOR"], dicInfos["SETTINGS"].getStructSize(),
                        dicInfos["SETTINGS"].getMaxSizeStruct(),
                        dicInfos["SETTINGS"].getPacket())
            data = values[2].decode()
            text = data.split('|')
            for elem in text:
                chave, valor = elem.split(":")

                if chave.upper() in "DATAHORA":
                    dicInfos["CONTROLLER"].setTime(time.ctime(float(valor)))
                elif chave.upper() in "DIAUTIL":
                    if (int(valor)):
                        dicInfos["CONTROLLER"].setWorkDay(True)
                        system.addText("LOGS", "Dia Util!!! ")
                    else:
                        dicInfos["CONTROLLER"].setWorkDay(False)
                        system.addText("LOGS", "Não é um Dia Util, Desligando tudo!!! ")
                        offAll()
                elif chave.upper() in "COMANDO":
                    if (int(valor)):
                        dicInfos["CONTROLLER"].setWorkDay(True)
                        system.addText("LOGS", "Comando do Servidor, Permição para Ligar Aparelhos!!! ")
                    else:
                        system.addText("LOGS", "Comando do Servidor, Desligando tudo!!! ")
                        offAll()
                        dicInfos["CONTROLLER"].setWorkDay(False)
        except:
            pass


def pushBtnConecta() -> None:
    if not dicConn["SERVIDOR"] and dicInfos["CONTROLLER"].getPlaceName():
        try:
            dicConn["SERVIDOR"] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            dicConn["SERVIDOR"].connect((dicInfos["SETTINGS"].getIpServer(), dicInfos["SETTINGS"].getPortServer()))
            system.addText("LOGS", "Conexao com Servidor efetuada no IP: " + dicInfos["SETTINGS"].getIpServer() +
                           "    PORT: " + str(dicInfos["SETTINGS"].getPortServer()) + "!!!")
            _thread.start_new_thread(startConnServer, tuple([]))
            _thread.start_new_thread(receveServerMenssages, tuple([]))
        except:
            system.addText("LOGS", "Não foi possivel efetuar a Conexão!!! ")

    elif not dicInfos["CONTROLLER"].getPlaceName():
        system.addText("LOGS", "Selecione o local da Controladora!!! ")


def btnSendAtualizacao():
    sens = ""
    for elem in dicInfos["SENSORES"]:
        sens += dicInfos["SENSORES"][elem].getName() + ":" + str(dicInfos["SENSORES"][elem].getId()) + "|"
    try:
        mySend(dicConn["SERVIDOR"], dicInfos["SETTINGS"].getPacket(), dicInfos["CONTROLLER"].getId(), time.time(),
               "tipolocal:" + str(dicInfos["CONTROLLER"].getPlaceCode()) + "|" + sens)
        system.addText("LOGS", "Mensagem de atualização enviada ao Servidor!!! ")
    except:
        pass


# ------------------------------------#


dicInfos = {"SENSORES": {}, "ERRO_SENSOR": {}, "CONTROLLER": newController(), "APPARATUS": newApparatus(),
            "PLACES": getPlaces(),
            "MUTEX": _thread.allocate_lock(), "SETTINGS": getServerSettings()}

# conexao para Sensores
dicConn = {"SENSOR": socket.socket(socket.AF_INET, socket.SOCK_STREAM), "SERVIDOR": None}
dicConn["SENSOR"].bind((dicInfos["CONTROLLER"].getIpController(), dicInfos["CONTROLLER"].getPort()))
dicConn["SENSOR"].listen(1)

# iniciando interface grafica
root = startTk(geometry="1280x720", title="Controladora", resizable=False)
system = newSystem(root, "Settings/controllerInterfaceSettings.txt", platform.system())


if(platform.system().upper() == "WINDOWS"):
    # combobox
    system.addComboBox(root, "PLACES", dicInfos["PLACES"], width=30, x=280, y=12)

    # botoes
    system.addButtons(root, "SELECIONAR_LOCAL", select, width=12, text="Selecionar", place=True, x=490, y=10)
    system.addButtons(root, "CONECTAR_SERVIDOR", pushBtnConecta, width=12, text="Conectar", place=True, x=10, y=10)
    system.addButtons(root, "SEND_STATUS", btnSendAtualizacao, width=15, text="Enviar Atualizacao", place=True, x=120, y=10)
    # inicializa os botoes e labels dos equipamentos no arquivo de configuracao
else:
    # combobox
    system.addComboBox(root, "PLACES", dicInfos["PLACES"], width=20, x=280, y=17)

    # botoes
    system.addButtons(root, "SELECIONAR_LOCAL", select, width=7, text="Selecionar", place=True, x=470, y=10)
    system.addButtons(root, "CONECTAR_SERVIDOR", pushBtnConecta, width=8, text="Conectar", place=True, x=10, y=10)
    system.addButtons(root, "SEND_STATUS", btnSendAtualizacao, width=14, text="Enviar Atualizacao", place=True, x=120, y=10)
    # inicializa os botoes e labels dos equipamentos no arquivo de configuracao
startApparatus()

# inicia thread que aceita as conexoes para os sensores
_thread.start_new_thread(newConection, tuple([dicConn["SENSOR"], sensorConexao]))
_thread.start_new_thread(trataTime, tuple([]))
_thread.start_new_thread(trataErro, tuple([]))
root.mainloop()

from Functions.InterfaceFunctions import *
from Functions.ControllerSettings import *
from Functions.Places import getPlaces
from Functions.FunctionsSystema import *
from Functions.SensorSettings import *
from Functions.ServidorSettings import *
from functools import partial
import _thread
import socket
import platform
import time


def pushBtnController(controller):
    global labelsTemporarios

    sensores = controller.getSensores()
    for i in range(len(labelsTemporarios)):
        system.destroiLab(labelsTemporarios[i])

    labelsTemporarios = []

    for elem in sensores:
        system.addLabels("SENSORES", sensores[elem].getName(), font=("Verdana", "12"), text=sensores[elem].getName(),
                         fill="x", pady=2, padx=2, place=False, background="#F8F8FF")
        labelsTemporarios.append(sensores[elem].getName())

        if (sensores[elem].getErro()):
            system.addLabels("SENSORES_STATUS", str(sensores[elem].getId()), font=("Verdana", "12"),
                             text="OFF", fill="x", pady=2, padx=2, place=False, background="red")
            labelsTemporarios.append((sensores[elem].getName() + "SENSORES_STATUS"))
        else:
            system.addLabels("SENSORES_STATUS", str(sensores[elem].getId()), font=("Verdana", "12"),
                             text="ON", fill="x", pady=2, padx=2, place=False, background="green")
            labelsTemporarios.append(str(sensores[elem].getId()))


def newBtnController(cliente, controller) -> None:
    pushBtn = partial(pushBtnController, controller)
    name = str(controller.getId()) + " - " + controller.getPlaceName()
    system.addButtons(system.getContainers("CONTROLLERS"), name, pushBtn, text=name, width=120, place=False,
                      fill="x", padx=1, pady=1)
    if(platform.system().upper() == "WINDOWS"):
        system.addLabels("CONTROLLERS_STATUS", name, font=("Verdana", "12"), text="ON",
                         background="green", fill="x", pady=2, padx=2, place=False)
    else:
        system.addLabels("CONTROLLERS_STATUS", name, font=("Verdana", "14"), text="ON",
                         background="green", fill="x", pady=3, padx=3, place=False)

    system.addText("LOGS", "  Cliente IP:  " + str(cliente[0]) + "  -  CONTROLLER: " +
                   str(dicInfos["CONTROLLER"][controller.getId()].getId()) + "    conectado! " + "     Local: " +
                   dicInfos["CONTROLLER"][controller.getId()].getPlaceName())


def trataConn(conexao, controller, values):
    text = values.split('|')
    for elem in text:
        if (len(elem)):
            chave, valor = elem.split(":")
            if chave.upper() in "TIPOLOCAL":
                controller.setPlaceName(dicInfos["PLACES"][int(valor)])
            elif chave.upper() in "DATAHORA":
                controller.setTime(time.ctime(float(valor)))
            elif (chave.upper() in "ALERTA"):

                if "INCENDIO" in dicInfos["SETTINGS"].getDangerCode(int(valor)):
                    mySend(conexao, dicInfos["SETTINGS"].getPacket(), controller.getId(), time.time(), "comando:0")
                    system.addText("LOGS", "  Controller:  " + str(controller.getId()) + "  Alerta: " +
                                   dicInfos["SETTINGS"].getDangerCode(int(valor)))
                elif "DEFEIT" in dicInfos["SETTINGS"].getDangerCode(int(valor)):
                    system.addText("LOGS", "  Controller:  " + str(controller.getId()) + "  Alerta: " +
                                   dicInfos["SETTINGS"].getDangerCode(int(valor)))
            elif "SENSOR" in chave:
                for elem in dicInfos["TYPE_SENSORES"]:

                    if chave == dicInfos["TYPE_SENSORES"][elem]:
                        sens = cadSensor(elem, int(valor), None)
                        controller.setSensor(int(valor), sens)


def connController(conexao, cliente):
    while True:
        try:
            values = receve(conexao, dicInfos["SETTINGS"].getStructSize(), dicInfos["SETTINGS"].getMaxSizeStruct(),
                            dicInfos["SETTINGS"].getPacket())
            flag = True
            if values[0] not in dicInfos["CONTROLLER"]:
                while flag:
                    dicInfos["MUTEX"].acquire()
                    dicInfos["SOCKETS"][values[0]] = conexao
                    dicInfos["CONTROLLER"][values[0]] = cadController(values[0])
                    trataConn(conexao, dicInfos["CONTROLLER"][values[0]], values[2].decode())
                    newBtnController(cliente, dicInfos["CONTROLLER"][values[0]])
                    mySend(conexao, dicInfos["SETTINGS"].getPacket(), dicInfos["SETTINGS"].getDiaUtil(), time.time(),
                           "DiaUtil:" + str(dicInfos["SETTINGS"].getDiaUtil()))
                    flag = False
                    dicInfos["MUTEX"].release()
            else:
                trataConn(conexao, dicInfos["CONTROLLER"][values[0]], values[2].decode())
        except:

            idController = searchConn(dicInfos["CONTROLLER"], cliente)
            if idController:
                if dicInfos["SETTINGS"].getMaxErro() <= dicInfos["CONTROLLER"][idController].getControllerErro():
                    system.addText("LOGS", "  Cliente IP:  " + str(cliente[0]) + "  Erro: " +
                                   str(dicInfos["CONTROLLER"][idController].getControllerErro()))
                    break

            time.sleep(dicInfos["SETTINGS"].getResponse())
    dicInfos["SOCKETS"][cliente].close()
    _thread.exit()


def senddAll(data):
    for clientes in dicInfos["SOCKETS"]:
        mySend(dicInfos["SOCKETS"][clientes], dicInfos["SETTINGS"].getPacket(), dicInfos["SETTINGS"].getDiaUtil(),
               time.time(), data)
        system.addText("LOGS", "Enviado Comando " + data + " Para a Controladora de ID: " +
                       str(dicInfos["CONTROLLER"][clientes].getId()) + " No Local: " +
                       dicInfos["CONTROLLER"][clientes].getPlaceName())


def btnDiaUtil():
    if not dicInfos["SETTINGS"].getDiaUtil():
        system.setLabel("DIA_UTIL", background="green", text="ON")
        dicInfos["SETTINGS"].setDiaUtil()
        senddAll("DiaUtil:" + str(dicInfos["SETTINGS"].getDiaUtil()))

    else:
        system.setLabel("DIA_UTIL", background="red", text="OFF")
        dicInfos["SETTINGS"].setDiaUtil()
        senddAll("DiaUtil:" + str(dicInfos["SETTINGS"].getDiaUtil()))


def btnOnOff(nameBtn, nameEntry):
    if system.getEntry(nameEntry).isnumeric():
        if searchId(dicInfos["CONTROLLER"], int(system.getEntry(nameEntry))):
            if nameBtn == "ON":
                mySend(dicInfos["SOCKETS"][int(system.getEntry(nameEntry))], dicInfos["SETTINGS"].getPacket(),
                       dicInfos["SETTINGS"].getDiaUtil(),
                       time.time(), "Comando:1")
                system.addText("LOGS", "Enviado Comando de ON para Trabalhar" + " Para a Controladora de ID: " +
                               str(dicInfos["CONTROLLER"][int(system.getEntry(nameEntry))].getId()) + " No Local: " +
                               dicInfos["CONTROLLER"][int(system.getEntry(nameEntry))].getPlaceName())
            else:
                mySend(dicInfos["SOCKETS"][int(system.getEntry(nameEntry))], dicInfos["SETTINGS"].getPacket(),
                       dicInfos["SETTINGS"].getDiaUtil(),
                       time.time(), "Comando:0")
                system.addText("LOGS", "Enviado Comando de OFF para Trabalhar" + " Para a Controladora de ID: " +
                               str(dicInfos["CONTROLLER"][int(system.getEntry(nameEntry))].getId()) + " No Local: " +
                               dicInfos["CONTROLLER"][int(system.getEntry(nameEntry))].getPlaceName())


root = startTk(geometry="1280x720", title="Controladora", resizable=False)

system = newSystem(root, "Settings/serverInterfaceSettings.txt", platform.system())
labelsTemporarios = []
dicInfos = {"SENSORES": {}, "CONTROLLER": {}, "CONTROLLER_ERRO": {}, "PLACES": getPlaces(),
            "MUTEX": _thread.allocate_lock(), "SETTINGS": getServerSettings(),
            "TYPE_SENSORES": getSensores(), "SOCKETS": {}}

# abri conexao para controladoras

tcpControladora = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpControladora.bind((dicInfos["SETTINGS"].getIpServer(), dicInfos["SETTINGS"].getPortServer()))
tcpControladora.listen()


if(platform.system().upper() == "WINDOWS"):
    ##----------
    system.addButtons(None, "DIA_UTIL", btnDiaUtil, width=12, text="Dia util", place=True, x=10, y=10)
    system.addLabels("DIA_UTIL", "DIA_UTIL", font=("Verdana", "13"), text="ON", y=10, x=120, place=True, width=9)
    system.setLabel("DIA_UTIL", background="green")
    system.addLabels(None, "ID_CONTROLLER", font=("Verdana", "8"), text="ID da controladora para enviar comando de On/Off",
                     y=17, x=250, place=True, width=50)
    system.addEntry(None, "ENTRY_ID", width=15, x=580, y=15)
    btnOn = partial(btnOnOff, "ON", "ENTRY_ID")
    btnOff = partial(btnOnOff, "OFF", "ENTRY_ID")
    system.addButtons(None, "COMANDO_ON", btnOn, width=8, text="ON", place=True, x=680, y=10)
    system.addButtons(None, "COMANDO_OFF", btnOff, width=8, text="OFF", place=True, x=750, y=10)
else:
    ##----------
    system.addButtons(None, "DIA_UTIL", btnDiaUtil, width=8, text="Dia util", place=True, x=10, y=15)
    system.addLabels("DIA_UTIL", "DIA_UTIL", font=("Verdana", "14"), text="ON", y=17, x=120, place=True, width=8)
    system.setLabel("DIA_UTIL", background="green")
    system.addLabels(None, "ID_CONTROLLER", font=("Verdana", "8"), text="ID da controladora para enviar comando de On/Off",
                     y=25, x=230, place=True, width=40)
    system.addEntry(None, "ENTRY_ID", width=10, x=530, y=17)
    btnOn = partial(btnOnOff, "ON", "ENTRY_ID")
    btnOff = partial(btnOnOff, "OFF", "ENTRY_ID")
    system.addButtons(None, "COMANDO_ON", btnOn, width=6, text="ON", place=True, x=620, y=10)
    system.addButtons(None, "COMANDO_OFF", btnOff, width=6, text="OFF", place=True, x=700, y=10)

# inicia thread que aceita as conexoes para os sensores
_thread.start_new_thread(newConection, tuple([tcpControladora, connController]))
root.mainloop()

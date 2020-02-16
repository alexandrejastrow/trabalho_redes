import _thread
import socket
import struct
from threading import Timer
from datetime import datetime, timedelta
from functools import partial
from tkinter import *
import time
import Functions.SensorSettings
from Functions.ControllerSettings import *
from Functions.ServidorSettings import *


def receve(socket, config):

    msg = socket.recv(config.getMaxSizeStruct())
    pack_size = len(msg) - config.getStructSize()
    mask_format =  config.getControllerPacket() + str(pack_size) + 's'
    return struct.unpack(mask_format, msg)


def newBtnSensor():
    ...


def mySend(tcpServer, settings, info):
    data = "Alerta:2"
    mask_format = settings.getControllerPacket() + str(len(data.encode('utf-8'))) + 's'
    msg = struct.pack(mask_format, 1, time.time(), data.encode('utf-8'))
    tcpServer.send(msg)


def searchIdController(dicController: dict, idController: int) -> bool:
    for control in dicController:
        if (dicController[control].getIdController() == idController):
            return True
    return False


def newBtnController(cliente, controller, btnController, mutex, argsContainers):
    function = partial(functionBtnController, controller)
    mutex.acquire()
    btnController[cliente] = (Button(argsContainers[0], command=function), Label(argsContainers[1], text="ON"))
    btnController[cliente][1]["background"] = "green"
    btnController[cliente][1]["font"] = ("Calibri", "11")
    btnController[cliente][0].pack(side=TOP, fill="x", padx=2, pady=1)
    btnController[cliente][1].pack(side=TOP, fill="x", padx=2, pady=2)
    btnController[cliente][0]["text"] = controller.getPlaceName() + " ID: " + str(controller.getIdController())
    mutex.release()


def trataConn(conexao, bodyText, controller, dicController, config, mutex, btnController, argsContainers):
    #print(argsContainers)
    pass


def controllerConexao(conexao: socket.socket, cliente: tuple, dicController: dict, dicControllerErro: dict,
                      config: functions.ServidorSettings.Settings, btnController: dict, mutex: _thread.allocate_lock,
                      *argsContainers: tuple) -> None:
    while True:
        idCotroller, timeNow, bodyText = receve(conexao, config)

        if (_thread.get_ident() not in dicController and not searchIdController(dicController, idCotroller)):
            mutex.acquire()
            local = bodyText.decode('utf-8').split(":")
            dicController[_thread.get_ident()] = cadController(idCotroller, int(local[0]), local[1])
            dicController[_thread.get_ident()].setTime(time.time())
            mutex.release()
            newBtnController(cliente, dicController[_thread.get_ident()], btnController, mutex, argsContainers)
            mySend(conexao, config, "diaUtil"+ config.getChaveValor() + "1" )
        else:
            trataConn(conexao, bodyText.decode(), dicController[_thread.get_ident()], dicController, config, mutex,
                      btnController, argsContainers)


        if (time.ctime(time.time()) > time.ctime(dicController[_thread.get_ident()].getTime() + config.getResponse())):
            dicController[_thread.get_ident()].addControllerErro()
            if (dicController[_thread.get_ident()].getControllerErro() >= config.getMaxErro()):
                pass
        else:
            dicController[_thread.get_ident()].cleanControllerErro()
        time.sleep(config.getResponse())


def functionBtnController(controller):
    pass

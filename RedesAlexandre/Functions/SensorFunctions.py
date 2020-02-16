from tkinter import *
import socket
import struct
import time
from threading import Timer
import sys
from functools import *
import _thread


# funcao que cria conexao com a controladora
from Functions.SensorSettings import setSensor


def conecta(ip, port, infos, sensor, config):
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.connect((ip, port))
    infos.insert(END, "Conexao ativa!!!")
    # cria uma thread onde executa duncoes diversas
    _thread.start_new_thread(conn, tuple([tcp, infos, sensor, config]))
    # retorna o socket
    return tcp


# funcao do botao selecionar onde se escolhe o sensor a depender o que estiver na combobox
def select(sensor, infos, combo, listSensor):
    if (combo.get() and sensor == None):

        sensor = setSensor(listSensor, combo.get())
        if (sensor == -1):
            infos.insert(END, "Erro ao criar o sensor")
            infos.insert(END, "verifique os arquivos de configurações!!!")
            sensor = None
        else:
            infos.insert(END, "sensor " + sensor.getName() + " selecionado!!!")
    elif (sensor):
        infos.insert(END, "Sensor já selecionado!!!")
    else:
        infos.insert(END, "Nenhum sensor selecionado!!!")
    return sensor


# funcao que envia mensagem para controladora
def mySend(socket, infos, config, idSensor, tpSensor, vlSensor):

    try:
        msg = struct.pack(config.getPacketType(), idSensor, tpSensor, vlSensor)
        socket.send(msg)
        infos.insert(END, "Mensagem enviada com sucesso valor: " + str(vlSensor))
        return 1
    except:
        infos.insert(END, "Erro no envio da mensagem!!!")
        return 0


# alarme
def setInterval(function, interval, *params, **kwparams):
    def setTimer(wrapper):
        wrapper.timer = Timer(interval, wrapper)
        wrapper.timer.start()

    def wrapper():
        function(*params, **kwparams)
        setTimer(wrapper)

    setTimer(wrapper)
    return wrapper

    def clearInterval(wrapper):
        wrapper.timer.cancel()


def MensagemControle(tcp, infos, config, sensor):
    if (mySend(tcp, infos, config, sensor.getId(), sensor.getCode(), sensor.getRandomValue()) == 0):
        sys.exit()


# funcao que envia valor pelo botao da interface grafica e sao nao for digitado valor gera valor ramdom
def sendMensage(tcp, infos, sensor, config, valor):
    if (valor != None):
        if (valor >= sensor.getMinValue() and valor <= sensor.getMaxValue()):
            mySend(tcp, infos, config, sensor.getId(), sensor.getCode(), valor)
        else:
            infos.insert(END, "Valor de sensor invalido!!!")
    else:
        mySend(tcp, infos, config, sensor.getId(), sensor.getCode(), sensor.getRandomValue())


# funcao loop que envia mensagem em intervalo de tempo
def conn(tcp, infos, sensor, config):
    try:

        mensagemControl = partial(MensagemControle, tcp, infos, config, sensor)
        interval_monitor = setInterval(mensagemControl, sensor.getResponse())
        mySend(tcp, infos, config, sensor.getId(), sensor.getCode(), sensor.getRandomValue())
        while (True):
            time.sleep(sensor.getResponse())
    except:
        infos.insert(END, "Conexao finalizada!!!")

    _thread.exit()

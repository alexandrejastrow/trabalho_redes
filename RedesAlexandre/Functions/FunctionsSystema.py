import socket
import struct
import _thread

def receve(socket: socket.socket, size: int, max_size: int, packet: str) -> tuple:
    """Recebe mensagem do sensor cria botao e label e encaminha para funcao que trata.

        :type socket: socket.socket
        :type size: int
        :type max_size: int
        :type packet: str
    Retorna uma mensagem descompactada no farmato tuple """

    mensagem = socket.recv(max_size)
    pack_size = len(mensagem) - size
    mask_format = packet + str(pack_size) + 's'
    return struct.unpack(mask_format, mensagem)


def mySend(tcpServer, pack, Id, timeData, data):

    mask_format = pack + str(len(data.encode('utf-8'))) + 's'
    msg = struct.pack(mask_format, Id, timeData, data.encode('utf-8'))
    tcpServer.send(msg)


def newConection(tcp, function) -> None:
    while True:

        conn, client = tcp.accept()
        _thread.start_new_thread(function, tuple([conn, client]))


def searchId(objects: dict, id: int) -> bool:
    for ob in objects:
        if objects[ob].getId() == id:
            return True
    return False


def searchConn(objects: dict, id: tuple) -> int:
    for ob in objects:
        if objects[ob].getConexao() == id:
            return ob
    return False
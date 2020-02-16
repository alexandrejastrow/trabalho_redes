from tkinter import ttk
from Functions.SensorSettings import *
from Functions.SensorFunctions import *
import platform
# configuracoe da janbela
root = Tk()
root.geometry("300x500")
root.title("Sensor")
root.resizable(width=False, height=False)
fonte = ("Verdana", "10")

# fim configuracoes da janela


# variaveis
sensor = None
listSensor = getSensores()
config = getSettings()
flag = 1
tcp = None


# funcoes dos botoes
def btConn():
    global flag
    global sensor
    global tcp

    if (flag and sensor):
        try:
            tcp = conecta(config.getIp(), config.getPort(), infos, sensor, config)
            flag = 0
        except:
            pass
    elif (flag):
        infos.insert(END, "Nenhum sensor selecionado!!!")


def btnSelect():
    global sensor
    sensor = select(sensor, infos, combo, listSensor)


def btnSend():
    global tcp
    global sensor


    if(entryEnviar.get() and tcp and sensor and entryEnviar.get().isnumeric()):
        sendMensage(tcp, infos, sensor, config, int(entryEnviar.get()))

    elif(not entryEnviar.get() and tcp and sensor):
        sendMensage(tcp, infos, sensor, config, None)

    elif(not entryEnviar.get().isnumeric()):
        infos.insert(END, "Digite um valor valido!!!")
    else:
        if(not sensor):
            infos.insert(END, "Nenhum sensor selecionado!!!")
        if(not tcp):
            infos.insert(END, "Nenhuma conexao estabelecida!!!")

if(platform.system() == 'Windows'):

    # combobox para escolha do sensor
    combo = ttk.Combobox(root, width=30)
    combo.grid(row=1, column=0, columnspan=6, padx=5, pady=5)

    # caixa de entrada para inserir valor de envio do sensor
    entryEnviar = Entry(root, background="white", widt=32)
    entryEnviar.grid(row=2, column=0, columnspan=6, padx=5, pady=5)

    # botoes de conectar selecionar e enviar
    btnConectar = Button(root, text="Conectar", width=40, command=btConn)
    btnConectar.grid(row=0, column=0, columnspan=8, padx=5, pady=5)

    btnSelec = Button(root, text="Selecionar", width=10, command=btnSelect)
    btnSelec.grid(row=1, column=7, pady=5, padx=5)

    btneEnvia = Button(root, text="Enviar", width=10, command=btnSend)
    btneEnvia.grid(row=2, column=7, pady=5, padx=5)

    status = Label(root, text="STATUS", font=fonte)
    status.grid(row=3, column=0, columnspan=8, pady=5, padx=5)

    # caixa onde as informaçoes seram atualizadas
    infos = Listbox(root, width=45, height=20, font=("Calibri", "9"))
    infos.place(x=10, y=150, bordermode=OUTSIDE, height=320, width=290)
    scrollInfos = Scrollbar(infos)
    scrollInfos.pack(side=RIGHT, fill=Y)
    infos["yscrollcommand"] = scrollInfos.set
    scrollInfos.config(command=infos.yview)
else:
    # combobox para escolha do sensor
    combo = ttk.Combobox(root, width=20)
    combo.grid(row=1, column=0, columnspan=6, padx=5, pady=5)

    # caixa de entrada para inserir valor de envio do sensor
    entryEnviar = Entry(root, background="white", widt=21)
    entryEnviar.grid(row=2, column=0, columnspan=6, padx=5, pady=5)

    # botoes de conectar selecionar e enviar
    btnConectar = Button(root, text="Conectar", width=15, command=btConn)
    btnConectar.grid(row=0, column=0, columnspan=8, padx=5, pady=5)

    btnSelec = Button(root, text="Selecionar", width=8, command=btnSelect)
    btnSelec.grid(row=1, column=7, pady=5, padx=5)

    btneEnvia = Button(root, text="Enviar", width=8, command=btnSend)
    btneEnvia.grid(row=2, column=7, pady=5, padx=5)

    status = Label(root, text="STATUS", font=fonte)
    status.grid(row=3, column=0, columnspan=8, pady=5, padx=5)

    # caixa onde as informaçoes seram atualizadas
    infos = Listbox(root, width=45, height=20, font=("Calibri", "9"))
    infos.place(x=10, y=150, bordermode=OUTSIDE, height=320, width=290)
    scrollInfos = Scrollbar(infos)
    scrollInfos.pack(side=RIGHT, fill=Y)
    infos["yscrollcommand"] = scrollInfos.set
    scrollInfos.config(command=infos.yview)
#insere as opcoes de sensor na combobox
listCombo = ()
for elem in listSensor:
    listCombo += (listSensor[elem],)
combo['values'] = listCombo

root.mainloop()

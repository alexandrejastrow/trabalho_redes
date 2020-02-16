import functools
from tkinter import *
from tkinter import ttk
import tkinter

from Functions import FunctionsSystema


class System:
    def __init__(self, root):
        self.root = root
        self.containers = {}
        self.labels = {}
        self.buttons = {}
        self.comboBox = {}
        self.entry = {}

    def getContainers(self, name: str) -> tkinter.Listbox:
        """Recebe um nome de container.

            :type name: str

            Retorna um objeto tkinter.ListBox."""
        return self.containers[name]

    def getLabels(self, name) -> tkinter.Label:
        """Recebe um nome de label.

            :type name: str

         Retorna um objeto tkinter.Label."""
        return self.labels[name]

    def getButtons(self, name) -> tkinter.Button:
        """Recebe um nome de Button.

            :type name: str

         Retorna um objeto tkinter.Button."""
        return self.buttons[name]

    def getComboBox(self, name) -> str:
        """Recebe um nome de ComboBox.

            :type name: str

         Retorna uma String."""
        return self.comboBox[name].get()

    def addContainers(self, root: tkinter.Tk, name: str, **args: dict) -> None:
        """Cria um novo objeto container.

            :type root: tkinter.Tk
            :type name: str
            :type **args: dict

         Nao possui retorno."""
        self.containers[name] = Listbox(root, background=args["background"])
        self.containers[name].place(x=args["x"], y=args["y"], bordermode=OUTSIDE,
                                    height=args["height"], width=args["width"])

        if args["scroll"]:
            scrollContainer = Scrollbar(self.containers[name])
            scrollContainer.pack(side=RIGHT, fill=Y)
            self.containers[name]["yscrollcommand"] = scrollContainer.set
            scrollContainer.config(command=self.containers[name].yview)

    def addLabels(self, root: str, name: str, **args: dict) -> None:
        """Cria um novo objeto Label.

            :type root: str
            :type name: str
             :type **args: dict

        Nao possui retorno."""
        if args["place"]:
            self.labels[name] = Label(self.root, text=args["text"], font=args["font"])
            self.labels[name].place(x=args["x"], y=args["y"])
        else:
            self.labels[name] = Label(self.getContainers(root), text=args["text"], font=args["font"], background=args["background"])
            self.labels[name].pack(side=TOP, fill=args["fill"], padx=args["padx"], pady=args["pady"])
        try:
            self.labels[name]["width"] = args["width"]
        except:
            pass

    def addButtons(self, root: tkinter.Tk, name: str, function: functools.partial, **args: dict) -> None:
        """Cria um novo objeto Button.

             :type root: tkinter.Tk
            :type name: str
            :type function: functools.partial
            :type **args: dict

         Nao possui retorno."""

        self.buttons[name] = Button(root, text=args["text"], width=args["width"],
                                       command=function)
        if args["place"]:
            self.buttons[name].place(x=args["x"], y=args["y"])
        else:
            self.buttons[name].pack(side=TOP, fill=args["fill"], padx=args["padx"],
                                       pady=args["pady"])

    def addComboBox(self, root: tkinter.Tk, name: str, infos: dict, **args: dict) -> None:
        """Cria um novo objeto ComboBox.

            :type root: tkinter.Tk
            :type name: str
            :type infos: dict
            :type **args: dict

        Nao possui retorno."""
        if root:
            self.comboBox[name] = ttk.Combobox(root, width=args["width"])
            self.comboBox[name].place(x=args["x"], y=args["y"])
            opcCombo = ()
            for elem in infos:
                opcCombo += (infos[elem], )
            self.comboBox[name]['values'] = opcCombo

    def setLabel(self, name: str, **args: dict) -> None:
        """Configura objeto Label.

            :type name: str
            :type **args: dict

        Nao possui retorno."""

        try:
            self.labels[name]["background"] = args["background"]
        except:
            pass
        try:
            self.labels[name]["text"] = args["text"]
        except:
            pass

    def addText(self, name: str, *args: list) -> None:
        """adciona texto a um Container.

            :type name: str
            :type *args: list

        Nao possui retorno."""
        for elem in args:
            self.containers[name].insert(END, elem)

    def delText(self, name: str) -> None:
        """deleta texto a um Container.

            :type name: str

        Nao possui retorno."""
        self.containers[name].delete(0, END)

    def destroiLab(self, name):
        self.labels[name].destroy()

    def addEntry(self,  root: str, name: str, **args: dict):
        if root:
            self.entry[name] = Entry(self.getContainers(root), width=args["width"])
            self.entry[name].place(x=args["x"], y=args["y"])
        else:
            self.entry[name] = Entry(root, width=args["width"])
            self.entry[name].place(x=args["x"], y=args["y"])

    def getEntry(self, name):
        return self.entry[name].get()

def getContainers(sistema: str, fileSettings: str) -> dict:
    """pega as configuracoes em um arquivo.

        :type sistema: str
        :type fileSettings: str

    retorna dicionario com as configuracoes"""

    file = open(fileSettings, "rt")
    dic = {}
    txt = file.read().split('\n')
    flag = True
    for i in range(len(txt)):
        if sistema in txt[i]:
            for j in range(i + 1, len(txt)):
                if "<CONTAINERS>" in txt[j] and flag:

                    for k in range(j + 1, len(txt)):
                        dado = txt[k].strip().split('\'')
                        if not "[END]" in txt[k]:
                            dic[dado[1]] = [int(dado[3]), int(dado[5]), int(dado[7]), int(dado[9]), dado[11],
                                            int(dado[13])]
                        else:
                            flag = False
                            break
                if not flag:
                    break
    return dic


def getLabels(sistema: str, fileSettings: str) -> dict:
    """pega as configuracoes em um arquivo.

            :type sistema: str
            :type fileSettings: str

        retorna dicionario com as configuracoes"""

    file = open(fileSettings, "rt")
    dic = {}
    txt = file.read().split('\n')
    flag = True
    for i in range(len(txt)):
        if sistema in txt[i]:
            for j in range(i + 1, len(txt)):
                if "<LABELS>" in txt[j] and flag:

                    for k in range(j + 1, len(txt)):
                        dado = txt[k].strip().split('\'')
                        if not "[END]" in txt[k]:
                            dic[dado[3]] = [int(dado[1]), dado[5], dado[7], int(dado[9]), int(dado[11]), int(dado[13]),
                                            int(dado[15]), int(dado[17])]
                        else:
                            flag = False
                            break
                if not flag:
                    break
    return dic

def newSystem(root: tkinter.Tk, fileSettings: str, sistem: str) -> System:
    """Cria uma stancia da Classe System e faz as configuracoes que estao no arquivo de configuracoes.

        :type root: tkinter.Tk
        :type fileSettings: str
        :type sistem: str

    retorna um objeto System"""

    cont = getContainers(sistem.upper(), fileSettings)
    lab = getLabels(sistem.upper(), fileSettings)
    sis = System(root)

    for elem in cont:
        sis.addContainers(root, elem, height=cont[elem][0], width=cont[elem][1], x=cont[elem][2],
                          y=cont[elem][3], background=cont[elem][4][1:-1], scroll=cont[elem][5])
    for elem in lab:
        if lab[elem][0]:

            sis.addLabels(elem, elem, text=lab[elem][1], background=lab[elem][2][1:-1], place=lab[elem][0],
                          x=lab[elem][3], y=lab[elem][4], font=("Verdana", "12"))
        else:
            sis.addLabels(elem, elem, text=lab[elem][1], background=lab[elem][2], place=lab[elem][0],
                          padx=lab[elem][5], pady=lab[elem][6], fill='x', font=("Verdana", "10"))

    return sis


def startTk(**args) -> tkinter.Tk:
    """Cria uma stancia de janela.

            :type args: dict

        retorna um objeto janela"""

    root = Tk()
    root.geometry(args["geometry"])
    root.title(args["title"])
    if not args["resizable"]:
        root.resizable(width=False, height=False)

    return root

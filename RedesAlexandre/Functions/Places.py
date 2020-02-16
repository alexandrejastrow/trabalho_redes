def getPlaces():
    file = open("Settings/places.txt", "rt")
    lists = {}
    txt = file.read().split('\n')

    for i in range(len(txt)):
        if ("<PLACES>" in txt[i]):
            for j in range(i + 1, len(txt)):
                dado = txt[j].strip().split('\'')
                if (not "[END]" in txt[j]):
                    lists[int(dado[1])] = dado[3]
                else:
                    break
    return lists

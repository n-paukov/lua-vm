def read_all_text(path):
    file = open(path, mode='r')
    text = file.read()
    file.close()

    return text

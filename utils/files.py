def read_all_text(path: str) -> str:
    file = open(path, mode='r')
    text = file.read()
    file.close()

    return text


def write_all_text(path: str, text: str):
    file = open(path, mode='w')
    file.write(text)
    file.close()

def read_file(path):
    text_file = open(path, "r")
    data = text_file.read()
    text_file.close()
    return data
# memory.py — stores past data

memory = []

def save_memory(data):
    memory.append(data)

def get_memory():
    return memory
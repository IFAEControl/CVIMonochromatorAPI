from serial.tools import list_ports


def get_available_ports():
    ports = list_ports.comports()
    ports_names = []
    for value in ports:
        ports_names.append(value.device)
    return ports_names

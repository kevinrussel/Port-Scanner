ip_addres = '127.0.0.1'
port_range_low = 8000
port_range_high = 8080
x = "hi".tobytes()
print(x)

class Packet:

    def __init__(self):
        self.version = 0x4
        self.IHL = 0x5
        self.v_ihl = (self.version << 4) | self.IHL
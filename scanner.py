ip_addres = '127.0.0.1'
port_range_low = 8000
port_range_high = 8080


class Packet:

    def __init__(self):
        # -- FIRST CHUNK ## 
        self.version = 0x4
        self.IHL = 0x5
        self.v_ihl = (self.version << 4) | self.IHL
        self.tos = 0x00
        self.total_length = 0x33 
        print(self.v_ihl)

        #-- SECOND CHUNK ##
        self.identification = 0x5

packet = Packet()
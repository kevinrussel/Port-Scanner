import socket

ip_addres = '127.0.0.1'
port_range_low = 8000
port_range_high = 8080


class Packet:

    def __init__(self,src_ip, dest_ip, dest_port):
        #-- IP HEADER --#
        # -- FIRST CHUNK ## 
        self.version = 0x4
        self.IHL = 0x5
        self.v_ihl = (self.version << 4) | self.IHL
        self.tos = 0x00
        self.total_length = 0x33 
        print(self.v_ihl)

        #-- SECOND CHUNK ##
        self.identification = 0x5
        self.flag = 0x0
        self.fragment_offset = 0x0
        self.f_fragment_offset = (self.flag << 13) | self.fragment_offset

        # -- THIRD CHUNK ##
        self.ttl = 0x40
        self.protocol = 0x6
        self.checksum = 0x0

        #-- FOURTH CHUNK --#
        self.src_ip = src_ip
        self.src_addr = socket.inet_aton(self.src_ip)
        print(self.src_addr)

        #-- FIFTH CHUNK -- #
        self.dest_ip = dest_ip
        self.dest_addr = socket.inet_aton(self.dest_ip)

        # -- TCP HEADER --#
        ## First Chunk
        self.src_port = 0x1F90
        self.dest_port = dest_port

        ## Second chunk
        self.seq_num = 0x0
        self.ack_num = 0x0

        ## Third chucnk
        self.tcp_offset = 0x5
        self.reserved = 0x0
        self.ns = 0x0
        self.cwr = 0x0
        self.ece = 0x0
        self.urg = 0x0
        self.ack = 0x0
        self.psh = 0x0
        self.rst = 0x0
        self.syn = 0x1
        self.fin = 0x0
        self.data_offset_res_flags = (self.tcp_offset << 12) | (self.reserved << 9) | (self.ns << 8) | (self.cwr << 7)|(self.ece << 6) | (self.urg << 5) | (self.ack << 4) | (self.psh << 3) | (self.rst << 2) | (self.syn << 1) | (self.fin)

        self.window_size = 0x7110
        

packet = Packet("127.0.0.1", "127.0.0.1", 8081)
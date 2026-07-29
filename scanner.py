import socket
from struct import *
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
        self.total_length = 0x28
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

        ## Third chunck
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

        ## FOURTH CHUNK:
        self.tcp_checksum = 0x0
        self.urg_pointer = 0x0

        self.ip_header = b""
        self.tcp_header = b""
        self.packet = b""

    def generate_tmp_ip_header(self):
        tmp_ip_header = pack(!)

    def generate_packet(self):
        # IP Header + checksum
        final_ip_header = pack("!BBHHHBBH",self.v_ihl,self.tos,self.total_length,self.identification,self.f_fragment_offset,self.ttl,self.protocol,self.create_tmp_ip_header(),)

packet = Packet("127.0.0.1", "127.0.0.1", 8081)
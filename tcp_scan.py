import socket
from struct import *
import asyncio



class Packet:

    def __init__(self,src_ip, dest_ip, dest_port):
        #-- IP HEADER --#
        # -- FIRST CHUNK ## 
        self.version = 0x4
        self.IHL = 0x5
        self.v_ihl = (self.version << 4) | self.IHL
        self.tos = 0x00
        self.total_length = 0x28
        

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
        

        #-- FIFTH CHUNK -- #
        self.dest_ip = dest_ip
        self.dest_addr = socket.inet_aton(self.dest_ip)

        ####################################################
        # -- TCP HEADER --#
        ## First Chunk
        self.src_port = 0x1F90
        self.dest_port = dest_port

        ## Second chunk
        self.seq_num = 0x0
        self.ack_num = 0x0

        ## Third chunk
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

    def calculate_tcp_flags(self,tcp_offset,reserved,ns,cwr,ece,urg,ack,psh,rst,syn,fin):
        pass

    def calc_checksum(self, msg):
        s = 0
        for i in range(0, len(msg), 2):
            w = (msg[i] << 8) + msg[i+1] 
            s = s + w
        # s = 0x119cc
        s = (s >> 16) + (s & 0xffff)
        # s = 0x19cd
        s = ~s & 0xffff
        # s = 0xe632
        return s

    def generate_tmp_ip_header(self):
        tmp_ip_header = pack("!BBHHHBBH4s4s", self.v_ihl,self.tos,self.total_length,self.identification,self.f_fragment_offset,self.ttl,self.protocol,self.checksum,self.src_addr,self.dest_addr)
        return tmp_ip_header

    def generate_tmp_tcp_header(self):
        tmp_tcp_header = pack("!HHLLHHHH",self.src_port,self.dest_port,self.seq_num,self.ack_num,self.data_offset_res_flags,self.window_size,self.tcp_checksum,self.urg_pointer)
        return tmp_tcp_header
    
    def generate_syn_packet(self):
        # IP Header + checksum
        final_ip_header = pack("!BBHHHBBH4s4s",self.v_ihl,self.tos,self.total_length,self.identification,self.f_fragment_offset,self.ttl,self.protocol,self.calc_checksum(self.generate_tmp_ip_header()),self.src_addr,self.dest_addr)

        tmp_tcp_header = self.generate_tmp_tcp_header()
        pseudo_header = pack("!4s4sBBH",self.src_addr,self.dest_addr,0x0,self.protocol,len(tmp_tcp_header))
        psh = pseudo_header + tmp_tcp_header
        final_tcp_header = pack("!HHLLHHHH",self.src_port,self.dest_port,self.seq_num,self.ack_num,self.data_offset_res_flags,self.window_size,self.calc_checksum(psh),self.urg_pointer)


        self.ip_header  = final_ip_header
        self.tcp_header = final_tcp_header
        self.packet = self.ip_header + self.tcp_header

    async def send_packet(self):
        s = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_TCP)
        s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        s.setblocking(False)
        s.sendto(self.packet,(self.dest_ip,0))
        loop = asyncio.get_event_loop()

        ## Linux sends an immediate SYN back the moment we send out the packet, this is to ignore that
        while True:
            data = await loop.sock_recv(s,1024)
            ip = data[:20]
            tcp = data[20:40]

            src_port, dst_port, seq, ack, off_flags, *_ = unpack(
                "!HHLLHHHH", tcp
            )
            if src_port == self.dest_port and dst_port == self.src_port:
                break
        s.close()
        return data

    

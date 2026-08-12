import tcp_scan
import struct
import asyncio



class ScanPort:

    def __init__(self):
        self.results = []
        self.port_open = []
        self.start_port = 1000
        self.end_port = 9000
        self.type_of_scan = "synscan"
          
    async def send_packet(self,src_ip, dest_ip, port,type_of_scan):
        packet = tcp_scan.Packet(src_ip,dest_ip,port)
        if(type_of_scan == "synscan"):
            packet.generate_syn_packet()
            try:
                result = await asyncio.wait_for(packet.send_packet(),timeout=0.5)
                self.check_if_open(port,result)
            except asyncio.TimeoutError:
                    print(f"Port {port} is: filtered (no response)")
        elif(type_of_scan == "finscan"):
            packet.generate_fin_packet()
            try:
                result = await asyncio.wait_for(packet.send_packet(),timeout=0.5)
            except asyncio.TimeoutError:
                self.port_open.append(f"Port {port} is: filtered (no response)")

        elif (type_of_scan == "nullscan"):
            packet.generate_null_packet()
            try:
                result = await asyncio.wait_for(packet.send_packet(),timeout=0.5)
            except asyncio.TimeoutError:
                self.port_open.append(f"Port {port} is: filtered (no response)")


    def check_if_open(self,port, response):
        ip = response[:20]
        tcp = response[20:40]
        src_port, dst_port, seq, ack, flags, *_ = struct.unpack(
        "!HHLLHHHH", tcp
    )

        if (flags & 0x1FF == 0x12):
            ans = "Port "+str(port)+" is: open"
            self.port_open.append(ans)
        else:
            ans = "Port "+str(port)+" is: closed"
        self.results.append(ans)


    async def main(self,start, end,type_of_scan): 
        
        tasks = [self.send_packet("127.0.0.1", "127.0.0.1",value,type_of_scan) for value in range(start,end)]   
        await asyncio.gather(*tasks)
        if(type_of_scan == "synscan"):
            with open("Every_Port_Status.txt", "w") as file:
                for entry in self.results:
                    file.write(f"{entry}\n")
            with open("open_port.txt","w") as file:
                for entry in self.port_open:
                    file.write(f"{entry}\n")
        elif (type_of_scan == "finscan" or type_of_scan == "nullscan"):
            with open("open_port.txt","w") as file:
                        for entry in self.port_open:
                            file.write(f"{entry}\n")
    



    def run(self,start = 1000, end = 9000,type_of_scan = "synscan"):
        asyncio.run(self.main(start,end,type_of_scan))
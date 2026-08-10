import tcp_scan
import struct
import asyncio
results = []
port_open = []
async def send_packet(src_ip, dest_ip, port,type_of_scan):

    packet = tcp_scan.Packet(src_ip,dest_ip,port)
    if(type_of_scan == "synscan"):
        packet.generate_syn_packet()
    elif(type_of_scan == "finscan"):
        packet.generate_fin_packet()
    try:
        result = await asyncio.wait_for(packet.send_packet(),timeout=1.0)
        check_if_open(port,result)
    except asyncio.TimeoutError:
        print(f"Port {port} is: filtered (no response)")
    

def check_if_open(port, response):
    

    ip = response[:20]
    tcp = response[20:40]
    src_port, dst_port, seq, ack, flags, *_ = struct.unpack(
    "!HHLLHHHH", tcp
)

    if (flags & 0x1FF == 0x12):
        ans = "Port "+str(port)+" is: open"
        port_open.append(ans)
    else:
        ans = "Port "+str(port)+" is: closed"
    results.append(ans)


async def main(start, end,type_of_scan):
    tasks = [send_packet("127.0.0.1", "127.0.0.1",value) for value in range(start,end,type_of_scan)]   
    await asyncio.gather(*tasks)
    if(type_of_scan == "synscan"):
        with open("Every_Port_Status.txt", "w") as file:
            for entry in results:
                file.write(f"{entry}\n")
        with open("open_port.txt","w") as file:
            for entry in port_open:
                file.write(f"{entry}\n")
    else:
        total_entries = []
        for i in range(start,end):
            total_entries.append(i)
            


def run(start = 1000, end = 9000,type_of_scan = "synscan"):
    asyncio.run(main(start,end,type_of_scan))
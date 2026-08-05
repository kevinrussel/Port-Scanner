import tcp_scan
import struct
import asyncio
results = []
port_open = []
async def send_packet(src_ip, dest_ip, port):

    packet = tcp_scan.Packet(src_ip,dest_ip,port)
    packet.generate_packet()
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
async def main(start, end):
    tasks = [send_packet("127.0.0.1", "127.0.0.1",value) for value in range(start,end)]   
    await asyncio.gather(*tasks)
    with open("Every_Port_Status.txt", "w") as file:
        for entry in results:
            file.write(f"{entry}\n")
    with open("open_port.txt","w") as file:
        for entry in port_open:
            file.write(f"{entry}\n")

def run(start = 1000, end = 9000):
    asyncio.run(main(start,end))
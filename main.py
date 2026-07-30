import scanner
import struct
import asyncio

async def send_packet(packet,value):
    print("Hello world")
    # result = await packet.send_packet()
    # check_if_open(value,result)

def check_if_open(port, response):
    

    ip = response[:20]
    tcp = response[20:40]
    src_port, dst_port, seq, ack, flags, *_ = struct.unpack(
    "!HHLLHHHH", tcp
)
    

    if (flags & 0x1FF == 0x12):
        print("Port "+str(port)+" is: open")
    else:
        print("Port "+str(port)+" is: closed")
async def main():
    tasks = [scanner.Packet("127.0.0.1", "127.0.0.1", value) for value in range(8081,8090)]   
    await asyncio.gather(tasks*)


asyncio.run(main())
import socket
import json
import ipaddress
import threading
from packet import Packet
from urllib.parse import urlparse
from redirect import redirectedUrl
from urlParsing import parseReponse, parseURL
from packet_constructor import Packet_Constructor
from packet_sender import Packet_Sender

p_built = Packet_Constructor()
conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
seq_num = 0
router = "localhost"
router_port = 3000
router = (router,router_port)

def postUrl(url, port ,headers, body):
    url = urlparse(url)
    path = url.path
    if path == "":
        path = "/"
    host=url.netloc
    headers["Host"] = host
    message = "POST %s HTTP/1.1 \r\n" % (path)
    for header in headers:
        message = "%s%s: %s\r\n"%(message, header, headers[header])
    message = message + "\r\n"
    byte_message = message.encode('utf-8') + body + "\r\n".encode('utf-8')
    received_payload = False
    payload = None
    
    try:
        received_payload = False
        payload = None
        peer_ip = ipaddress.ip_address(socket.gethostbyname(host))

        connect(host, port, peer_ip)
        print(byte_message)
        print(conn)
        print(router)
        print(peer_ip)
        print(port)

        Packet_Sender.send_as_packets(byte_message, conn, router, peer_ip, port)
        while(not received_payload):
            print("awaiting packet")
            data, sender = conn.recvfrom(1024)
            print("got a packet")
            threading.Thread(target=packet_client, args=(conn, data, sender)).start()
    except Exception as e:
        print("got exception")
        print(e)
    finally:
        #close_connection()
        return parse_packet_response(payload)

def packet_client(conn,data,sender):
    global p_constructor
    global received_payload
    global payload

    p = Packet.from_bytes(data)
    if p.seq_num == Packet_Constructor.d_type:
        print(p.seq_num)
        payload = p_built.add_packet(p, conn, sender)
        if(payload):
            print(payload)
            received_payload = True

def connect(host, port, peer_ip):
    global conn
    global p_constructor
    global router
    global seq_num
    print(peer_ip)
    print(port)
    data = b''

    p = Packet(packet_type=Packet_Constructor.syn_type,
                       seq_num=seq_num,
                       peer_ip_addr=peer_ip,
                       peer_port=port,
                       is_last_packet=False,
                       payload=data)
    
    conn.sendto(p.to_bytes(), router) 

    response, sender = conn.recvfrom(1024)
    p = Packet.from_bytes(response)

    if(p.packet_type == Packet_Constructor.syn_ack_type):
        print("Got syn ack, responding with ack")
        p.packet_type = Packet_Constructor.ack_type
        conn.sendto(p.to_bytes(), sender)
    else:
        print("During TCP handshake, got the wrong packet type. Restarting")
        connect(host, port, peer_ip)

    
    
        

    
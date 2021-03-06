import socket
import selectors
import types

sel = selectors.DefaultSelector()


def accept_wrapper(sock):
    conn, addr = sock.accept()
    print("accepted connection from", addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)


def service_connection(key, mask, request_handler):
    try:
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)
            if recv_data:
                data.outb += request_handler(recv_data).encode('ascii')
            else:
                print("closing connection to", data.addr)
                sel.unregister(sock)
                sock.close()
        if mask & selectors.EVENT_WRITE:
            if data.outb:
                sent = sock.send(data.outb)
                data.outb = data.outb[sent:]
    except Exception as e:
        print("Unknown exception!")
        print(e)
        data.outb = 'Error'.encode('ascii')
        sock.send(data.outb)
        sock.close()


def listen(request_handler, host='127.0.0.1', port=8080):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen()
    print("listening on", (host, port))
    sock.setblocking(False)

    sel.register(sock, selectors.EVENT_READ, data=None)

    try:
        while True:
            events = sel.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    accept_wrapper(key.fileobj)
                else:
                    service_connection(key, mask, request_handler)
    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting!")
    finally:
        sock.close()
        sel.close()
    sock.close()
    sel.close()


def send_message(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    sock.send(message.encode('ascii'))
    response = sock.recv(1024)
    sock.close()
    return response

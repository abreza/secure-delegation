from tcp_socket import listen


def request_handler(request):
    return 'response'


listen(request_handler)

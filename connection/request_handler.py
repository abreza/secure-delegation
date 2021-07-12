import json


def request_handler(request, router):
    try:
        req = json.loads(request)
    except:
        return 'Error: bad request! Req should be stringified json.'
    url = req.get('url')
    if not url:
        return 'Error: bad request! Req should have a url field.'

    if url not in router:
        return 'Error: bad url!'

    response = router[url](req)
    if response:
        return response
    return ''

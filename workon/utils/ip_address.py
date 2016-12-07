# encoding: utf-8

PRIVATE_IPS_PREFIX = ('10.', '172.', '192.', )

__all__ = ["get_ip_address_from_request"]

def get_ip_address_from_request(request):
    """get the client ip from the request
    """
    remote_address = request.META.get('REMOTE_ADDR')
    # set the default value of the ip to be the REMOTE_ADDR if available
    # else None
    ip = remote_address
    # try to get the first non-proxy ip (not a private ip) from the
    # HTTP_X_FORWARDED_FOR
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        proxies = x_forwarded_for.split(',')
        # remove the private ips from the beginning
        while (len(proxies) > 0 and
                proxies[0].startswith(PRIVATE_IPS_PREFIX)):
            proxies.pop(0)
        # take the first ip which is not a private one (of a proxy)
        if len(proxies) > 0:
            ip = proxies[0]

    return ip

# def get_ip_address_from_request(request):
#     """ Makes the best attempt to get the client's real IP or return the loopback """
#     PRIVATE_IPS_PREFIX = ('10.', '172.', '192.', '127.')
#     ip_address = ''
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '')
#     if x_forwarded_for and ',' not in x_forwarded_for:
#         if not x_forwarded_for.startswith(PRIVATE_IPS_PREFIX) and is_valid_ip(x_forwarded_for):
#             ip_address = x_forwarded_for.strip()
#     else:
#         ips = [ip.strip() for ip in x_forwarded_for.split(',')]
#         for ip in ips:
#             if ip.startswith(PRIVATE_IPS_PREFIX):
#                 continue
#             elif not is_valid_ip(ip):
#                 continue
#             else:
#                 ip_address = ip
#                 break
#     if not ip_address:
#         x_real_ip = request.META.get('HTTP_X_REAL_IP', '')
#         if x_real_ip:
#             if not x_real_ip.startswith(PRIVATE_IPS_PREFIX) and is_valid_ip(x_real_ip):
#                 ip_address = x_real_ip.strip()
#     if not ip_address:
#         remote_addr = request.META.get('REMOTE_ADDR', '')
#         if remote_addr:
#             if not remote_addr.startswith(PRIVATE_IPS_PREFIX) and is_valid_ip(remote_addr):
#                 ip_address = remote_addr.strip()
#     if not ip_address:
#         ip_address = '127.0.0.1'
#     return ip_address
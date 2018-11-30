import re
import logging
import socket
from urllib import request, error, parse

# 匹配合法 IP 地址
regex_ip = re.compile(
    r"\D*("
    + r"(?:1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\."
    + r"(?:1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\."
    + r"(?:1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\."
    + r"(?:1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)"
    + r")\D*")

# 增强鲁棒性，用多种方式获取 IP
def get_ip():
    return (get_ip_by_azure())
    
def get_ip_by_azure():
    url = 'http://42.159.252.221:55555/'
    try:
        resp = request.urlopen(url=url, timeout=10).read()
        return regex_ip.match(resp.decode("utf-8")).group(1)
    except Exception as e:
        logging.warning("get_ip_by_ipip FAILED, error: %s", str(e))
        return None
 
# 测试
if __name__ == '__main__':
    print(get_ip()                     )

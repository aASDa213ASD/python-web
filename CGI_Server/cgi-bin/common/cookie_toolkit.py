import datetime
import http.cookies
import os


def save_cookie(name, value, path="/", expires=None):
    cookie = http.cookies.SimpleCookie()
    cookie[name] = value
    cookie[name]["path"] = path
    if expires:
        expiration = datetime.datetime.now() + datetime.timedelta(days=1)
        cookie[name]["expires"] = expiration.strftime("%a, %d %b %Y %H:%M:%S GMT")
    print(cookie)

def get_cookie(name):
    if 'HTTP_COOKIE' in os.environ:
        cookies = os.environ['HTTP_COOKIE']
        cookies = cookies.split('; ')
        for cookie in cookies:
            try:
                (_name, _value) = cookie.split('=')
                if name.lower() == _name.lower():
                    return _value
            except:
                return ''
    return ''

def get_all_cookies() -> dict:
    cookies = {}
    if 'HTTP_COOKIE' in os.environ:
        cookie_string = os.environ['HTTP_COOKIE']
        cookie_pairs = cookie_string.split('; ')
        for cookie_pair in cookie_pairs:
            try:
                name, value = cookie_pair.split('=')
                cookies[name] = value
            except:
                pass
    return cookies

def wipe_cookies():
    all_cookies: dict = get_all_cookies()
    for cookie in all_cookies:
        save_cookie(cookie, "")
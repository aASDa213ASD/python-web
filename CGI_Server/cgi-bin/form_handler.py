import cgi
import html
import sys

from common.cookie_toolkit import get_cookie, save_cookie
from common.html_toolkit import get_head, refresh_page


def _local_save_cookies() -> None:
    save_cookie("authorized", "1", expires=True)

    try:
        new_login_counter = str(int(get_cookie("login_counter")) + 1)
        save_cookie("login_counter", new_login_counter, expires=True)
    except ValueError:
        save_cookie("login_counter", "1", expires=True) 
    
    save_cookie("username", str(username), expires=True)
    save_cookie("platform", platform, expires=True)
    save_cookie("languages", programming_langs, expires=True) 

def send_html_data(data: str) -> None:
    print("Content-type:text/html\r\n\r\n")
    print(
        f"""
        <html>
            {get_head()}
            <body>
                <header>
                    <nav>
                        <div class="logo">🕸 CGI-BIN Server</div>

                        <div>
                            
                            <a href="/">
                                <button class="classButton" type="submit">Home</button>
                            </a>
                        </div>
                    </nav>
                    <hr>
                </header>
            
                <h3> {data} </h3>
            </body>
        </html>
        """
    )

""" Security flag """
_valid_data: bool = False

""" UTF-8 encoding """
sys.stdout.reconfigure(encoding='utf-8')

""" Process form submission """
form = cgi.FieldStorage()
 
username = form.getfirst("id", "")
password = form.getfirst("pwd", "")

""" Evil part (XSS Protection) """
username = html.escape(username)
password = html.escape(password)

""" Other data scraping """
platform = form.getfirst("type", "Unknown type.")

programming_languages = form.getlist("programming_language")
programming_langs = ''
for lang in programming_languages:
    programming_langs += " " + lang.upper() + " "

if username and password:
    if username == "admin" and password == "admin1234":
        try:
            _authorized = bool(int(get_cookie("authorized")))
            _valid_data = True
        except ValueError:
            _authorized = False
        
        if not _authorized:
            _local_save_cookies()
        
        auth = "[+] Successfully logged in."
    else:
        auth = "[!] Error, check credentials."
else:
    send_html_data(f"An error occured. Did you enter all the data in authentication panel ?")

if username and password and _valid_data:
    _cookie_login_counter = get_cookie("login_counter")
    if not _cookie_login_counter:
        _cookie_login_counter = 0

    print("Content-type:text/html\r\n\r\n")
    print(
    f"""
        <html>
        {get_head()}
        <body>
            <header>
                <nav>
                    <div class="logo">🕸 CGI-BIN Server</div>

                    <div>
                        
                        <a href="/">
                            <button class="classButton" type="submit">Log Out</button>
                        </a>
                    </div>
                </nav>
                <hr>
            </header>

            <a>Attention: You have been authorized as <b>{username}</b>.</a>
            <br>
            <a>If you <span style="color: lightcoral;">don't see the auth counter update:</span> <b><i>just refresh the page.</i></b></a>
            <br>
            <br>
            <a>Here's all we know about you:</a>
            <hr>
            <table class='table' border='1'>
                <tr><th>Username</th><th>Platform</th><th>Languages</th><th>Auth counter</th></tr>
                <tr><td>{username}</td><td>{platform}</td><td>{programming_langs}</td><td>{_cookie_login_counter}</td></tr>
            </table>

        </body>
        </html>
    """
    )
else:
    send_html_data(f"Invalid credentials, try again.")

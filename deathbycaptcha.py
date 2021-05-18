import deathbycaptcha

# pip install git+https://github.com/codevance/python-deathbycaptcha.git

def solve_captcha(username, password, captcha_file):
    client = deathbycaptcha.SocketClient(username, password)
    try:
        # balance = client.get_balance()
        # print balance
        captcha = client.decode(captcha_file)
        if captcha:
            print("CAPTCHA %s solved: %s" % (captcha["captcha"], captcha["text"]))
            return captcha["text"]
    except deathbycaptcha.AccessDeniedException:
        exit(1)


solve_captcha(username='', password='', captcha_file='captcha_img.jpg')
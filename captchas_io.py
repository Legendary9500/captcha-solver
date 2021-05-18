import requests
import time

CAPTCHAS_IO_KEY = 'Your key'

def captchas_io(site_key):
    payload = {"googlekey": site_key,
               "pageurl": 'https://www.inipec.gov.it/cerca-pec/-/pecs/companies',
               "method": 'userrecaptcha',
               "key": CAPTCHAS_IO_KEY}
    timeout = 300
    try:
        # print ('we try to CAPTCHAS.io service...')
        resp = requests.post('http://api.captchas.io/in.php', data=payload, timeout=timeout)
    except Exception as e:
        print('Error type:', type(e))
        print('CAPTCHAS.io service error to request:', e)
        return False, 'CAPTCHAS.io service error: ' + str(e)

    print("CAPTCHAS.io submit request response:", resp.text);
    if resp.text[0:2] != 'OK':
        print('CAPTCHAS.io service error.\nError code: "' + resp.text + '"')
        return False, resp.text
    captcha_id = resp.text[3:].strip()  # OK|2122988149

    fetch_url = "http://api.captchas.io/res.php?key=" + CAPTCHAS_IO_KEY + "&action=get&id=" + captcha_id
    # wait till captcha is ready
    for i in range(1, 36):  # 36*10 = 360 seconds = 6 min
        time.sleep(3)  # wait 10 sec.
        resp = requests.get(fetch_url)
        # print ('Passed', i*10 , 'seconds. CAPTCHAS.io result response: ', resp.text)
        if resp.text[0:2] == 'OK':
            return True, resp.text[3:]

    return False, resp.text
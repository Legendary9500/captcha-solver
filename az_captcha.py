import requests, time

AZCAPTCHA_KEY = 'Your Key'
def az_captcha(site_key):
    payload = {"googlekey": site_key,
               "pageurl": 'https://www.inipec.gov.it/cerca-pec/-/pecs/companies',
               "method": 'userrecaptcha',
               "key": AZCAPTCHA_KEY}
    timeout = 300
    try:
        resp = requests.post('http://azcaptcha.com/in.php', data=payload, timeout=timeout)
    except Exception as e:
        print('Error type:', type(e))
        print('AZCAPTCHA service error to request:', e)
        return False, 'AZCAPTCHA service error: ' + str(e)

    print("AZcap submit request response:", resp.text);
    if resp.text[0:2] != 'OK':
        print('AZCAPTCHA service error.\nError code: "' + resp.text + '"')
        return False, resp.text
    captcha_id = resp.text[3:]  # OK|2122988149

    fetch_url = "http://azcaptcha.com/res.php?key=" + AZCAPTCHA_KEY + "&action=get&id=" + captcha_id
    # wait till captcha is ready
    for i in range(1, 36):  # 36*10 = 360 seconds = 6 min
        time.sleep(3)  # wait 10 sec.
        resp = requests.get(fetch_url)
        # print ('Passed', i*10 , 'seconds. AZcap result response: ', resp.text)
        if resp.text[0:2] == 'OK':
            return True, resp.text[3:]

    return False, resp.text
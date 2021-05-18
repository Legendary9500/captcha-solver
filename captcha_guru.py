import requests, time

CAPTCHA_GURU_KEY = 'Your Key'

def captcha_guru(site_key):
    query = 'https://api.captcha.guru/in.php?key=' + CAPTCHA_GURU_KEY + '&method=userrecaptcha&googlekey=' + site_key + '&pageurl=https://www.inipec.gov.it/cerca-pec/-/pecs/companies'
    try:
        resp = requests.get(query, timeout=300)
    except Exception as e:
        print('Error type:', type(e))
        print('CAPTCHA GURU service error to request:', e)
        return False, 'CAPTCHA GURU service error: ' + str(e)

    print("CAPTCHA GURU submit request response:", resp.text);
    if resp.text[0:2] != 'OK':
        print('CAPTCHA GURU service error.\nError code: "' + resp.text + '"')
        return False, resp.text
    captcha_id = resp.text[3:]  # OK|2122988149
    fetch_url = "https://api.captcha.guru/res.php?key=" + CAPTCHA_GURU_KEY + "&action=get&id=" + captcha_id
    # wait till captcha is ready
    for i in range(1, 36):  # 36*10 = 360 seconds = 6 min
        time.sleep(3)  # wait 10 sec.
        resp = requests.get(fetch_url)
        # print ('Passed', i*10 , 'seconds. AZcap result response: ', resp.text)
        if resp.text[0:2] == 'OK':
            return True, resp.text[3:]

    return False, resp.text
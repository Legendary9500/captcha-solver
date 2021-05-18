import requests, time, json

CAPMOSTER_KEY = ''

def capmonster(site_key):
    payload = {
        "clientKey": CAPMOSTER_KEY,
        "task":
            {
                "type": "NoCaptchaTaskProxyless",
                "websiteURL": "https://www.inipec.gov.it//cerca-pec/-/pecs/companies",
                "websiteKey": site_key
            }
    }
    timeout = 300
    try:
        resp = requests.post('https://api.capmonster.cloud/createTask', json=payload, timeout=timeout)
        resp_json = json.loads(resp.text)
        error_code = resp_json['errorCode']
        if error_code:
            return False, error_code
    except Exception as e:
        print('Error type:', type(e))
        print('Capmonster service error to request:', e)
        return False, 'AZCAPTCHA service error: ' + str(e)

    captcha_id = resp_json['taskId']

    request_cnt = 0
    solution = None
    while 1:
        payload = {
            "clientKey": CAPMOSTER_KEY,
            "taskId": captcha_id
        }
        request_cnt += 1
        if request_cnt == 30 and not solution:
            return False, "Captcha timeout"
        try:
            resp = requests.post('https://api.capmonster.cloud/getTaskResult', json=payload, timeout=timeout)
        except:
            continue

        resp_json = json.loads(resp.text)
        solution = resp_json['solution']
        if solution:
            break
        else:
            time.sleep(1)

    return True, solution['gRecaptchaResponse']
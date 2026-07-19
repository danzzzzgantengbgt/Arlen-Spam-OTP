#!/usr/bin/env python3
# utils.py - Utility Functions

import re
import uuid
import random
import string
import urllib.parse
import requests

from useragents import USER_AGENTS

def normalize(phone):
    """Normalisasi nomor telepon ke format 62"""
    n = phone.strip().replace(' ', '').replace('-', '').replace('+', '')
    if n.startswith('08'):
        return '62' + n[1:]
    if n.startswith('8'):
        return '62' + n
    if n.startswith('62'):
        return n
    return ''

def fmt_08(p):
    """Format ke 08"""
    return '0' + p[2:] if p.startswith('62') else p

def fmt_nocode(p):
    """Format tanpa kode negara"""
    return p[2:] if p.startswith('62') else p

def fmt_plus(p):
    """Format ke +62"""
    return '+' + p if not p.startswith('+') else p

def fmt_phone_only(p):
    """Format nomor saja tanpa kode"""
    if p.startswith('62'):
        return p[2:]
    if p.startswith('+62'):
        return p[3:]
    if p.startswith('0'):
        return p[1:]
    return p

def get_public_ip():
    """Mendapatkan IP publik"""
    try:
        return requests.get('https://api.ipify.org', timeout=5).text.strip()
    except:
        return '127.0.0.1'

def extract_csrf(html):
    """Ekstrak CSRF token dari HTML"""
    patterns = [
        r'<meta name="csrf-token" content="([^"]+)"',
        r'<meta name="csrf_token" content="([^"]+)"',
        r'<input type="hidden" name="_token" value="([^"]+)"',
        r'<input type="hidden" name="csrf_token" value="([^"]+)"',
        r'<input type="hidden" name="_csrf" value="([^"]+)"',
        r'csrf_token\s*=\s*"([^"]+)"',
    ]
    for p in patterns:
        m = re.search(p, html, re.I)
        if m:
            return m.group(1)
    return None

def generate_multipart(data, boundary):
    """Generate multipart form data"""
    body = ""
    for key, val in data.items():
        body += f"--{boundary}\r\n"
        body += f'Content-Disposition: form-data; name="{key}"\r\n\r\n'
        body += f"{val}\r\n"
    body += f"--{boundary}--\r\n"
    return body

def get_random_user_agent():
    """Dapatkan user agent random"""
    return random.choice(USER_AGENTS)

def get_headers_with_random_ua(custom_headers=None):
    """Dapatkan headers dengan user agent random"""
    headers = {
        'User-Agent': get_random_user_agent(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Connection': 'keep-alive',
    }
    if custom_headers:
        headers.update(custom_headers)
    return headers

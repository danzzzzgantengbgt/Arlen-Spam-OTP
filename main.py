#!/usr/bin/env python3
# main.py - ARLEN -OTP OTP Spammer

import sys
import time
import platform
import os
import tty
import termios
import math
import random
import threading
import shutil
import re
from colorama import Fore, Style, init

from main_engine import run_single_round, run_infinite_loop

init(autoreset=True)

VERSION = "1.0.0"
TOOLS_NAME = "ARLEN -OTP"

exec_data = {
    'target': '',
    'threads': 5,
    'total_api': 24,
    'status': 'Initializing...',
    'progress': 0,
    'sent': 0,
    'success': 0,
    'failed': 0,
    'last_log': 'Starting...'
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def rgb_color(tick, offset=0):
    r = int((math.sin(tick * 0.5 + offset) + 1) * 127)
    g = int((math.sin(tick * 0.5 + offset + 2) + 1) * 127)
    b = int((math.sin(tick * 0.5 + offset + 4) + 1) * 127)
    return f"\033[38;2;{r};{g};{b}m"

def gradient_text(text, tick, offset=0):
    result = ""
    for i, char in enumerate(text):
        color = rgb_color(tick, offset + i * 0.1)
        result += f"{color}{char}{Style.RESET_ALL}"
    return result

class MatrixBackground:
    def __init__(self):
        try:
            self.width = shutil.get_terminal_size().columns
            self.height = shutil.get_terminal_size().lines
        except:
            self.width = 80
            self.height = 24
        
        self.width = max(40, self.width)
        self.height = max(10, self.height)
        
        self.columns = []
        self.chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()'
        self.init_columns()
    
    def init_columns(self):
        self.columns = []
        for x in range(self.width):
            length = random.randint(8, 25)
            col = {
                'x': x,
                'y': random.randint(-self.height, 0),
                'speed': random.uniform(0.8, 2.5),
                'length': length,
                'chars': [random.choice(self.chars) for _ in range(length)],
                'bright_pos': random.randint(0, length-1)
            }
            self.columns.append(col)
    
    def update(self):
        for col in self.columns:
            col['y'] += col['speed'] * 0.6
            
            if col['y'] > self.height + col['length']:
                col['y'] = random.randint(-self.height, 0)
                col['length'] = random.randint(8, 25)
                col['chars'] = [random.choice(self.chars) for _ in range(col['length'])]
                col['speed'] = random.uniform(0.8, 2.5)
                col['bright_pos'] = random.randint(0, col['length']-1)
            
            if random.random() < 0.03:
                for i in range(len(col['chars'])):
                    if random.random() < 0.3:
                        col['chars'][i] = random.choice(self.chars)
    
    def render(self, overlay_lines=None):
        sys.stdout.write('\033[?25l')
        sys.stdout.write('\033[H')
        
        screen = []
        for y in range(self.height):
            screen.append([' ' for _ in range(self.width)])
        
        for col in self.columns:
            x = col['x']
            start_y = int(col['y'])
            
            for i in range(col['length']):
                y = start_y + i
                if 0 <= y < self.height and 0 <= x < self.width:
                    char = col['chars'][i % len(col['chars'])]
                    
                    if i == col['bright_pos']:
                        color = Fore.GREEN + Style.BRIGHT
                    elif i < col['bright_pos'] + 4 and i > col['bright_pos'] - 2:
                        color = Fore.GREEN
                    else:
                        color = Fore.GREEN + Style.DIM
                    
                    screen[y][x] = color + char + Style.RESET_ALL
        
        for y in range(self.height):
            print(''.join(screen[y]))
        
        if overlay_lines:
            filtered = [line for line in overlay_lines if line.strip()]
            overlay_height = len(filtered)
            start_y = (self.height - overlay_height) // 2
            
            for i, line in enumerate(filtered):
                if line.strip():
                    clean_line = re.sub(r'\x1b\[[0-9;]*m', '', line)
                    x_pos = (self.width - len(clean_line)) // 2
                    if x_pos < 0:
                        x_pos = 0
                    sys.stdout.write(f'\033[{start_y + i};{x_pos}H')
                    print(line, end='')
        
        sys.stdout.write('\033[?25h')

def matrix_loading(duration=3):
    matrix = MatrixBackground()
    
    ascii_arlen = [
        "    █████╗ ██████╗ ██╗     ███████╗███╗   ██╗",
        "   ██╔══██╗██╔══██╗██║     ██╔════╝████╗  ██║",
        "   ███████║██████╔╝██║     █████╗  ██╔██╗ ██║",
        "   ██╔══██║██╔══██╗██║     ██╔══╝  ██║╚██╗██║",
        "   ██║  ██║██║  ██║███████╗███████╗██║ ╚████║",
        "   ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═══╝"
    ]
    
    start_time = time.time()
    tick = 0
    
    while time.time() - start_time < duration:
        tick += 0.05
        matrix.update()
        
        colored_ascii = []
        for line in ascii_arlen:
            colored_line = ""
            for i, char in enumerate(line):
                if char != ' ':
                    color = rgb_color(tick, i * 0.1)
                    colored_line += f"{color}{char}{Style.RESET_ALL}"
                else:
                    colored_line += " "
            colored_ascii.append(colored_line)
        
        progress = (time.time() - start_time) / duration
        dots = "." * (int((time.time() - start_time) * 2) % 4)
        loading_text = f"LOADING{dots}"
        loading_color = rgb_color(tick, 2)
        
        bar_length = min(40, matrix.width - 20)
        filled = int(bar_length * progress)
        bar = "█" * filled + "░" * (bar_length - filled)
        bar_color = rgb_color(tick, 3)
        
        status_color = rgb_color(tick, 4)
        status_text = "INITIALIZING" if progress < 0.3 else "LOADING" if progress < 0.6 else "PREPARING" if progress < 0.8 else "READY"
        
        overlay = [
            "",
            *colored_ascii,
            "",
            f"{loading_color}{loading_text}{Style.RESET_ALL}",
            "",
            f"{bar_color}[{bar}] {int(progress * 100)}%{Style.RESET_ALL}",
            "",
            f"{status_color}{'─' * 20}{Style.RESET_ALL}",
            f"{status_color}  {status_text}  {Style.RESET_ALL}",
            f"{status_color}{'─' * 20}{Style.RESET_ALL}",
        ]
        
        matrix.render(overlay)
        time.sleep(0.03)
    
    sys.stdout.write('\033[?25h')
    sys.stdout.flush()

def print_banner(tick=0):
    color = rgb_color(tick)
    reset = Style.RESET_ALL
    
    title = gradient_text("ARLEN -OTP", tick, 0)
    
    banner = f"""
  ┌──────────────────────────────────────────────────────┐
  │                     {title}                       │
  └──────────────────────────────────────────────────────┘

  ┌──────────────────────────────────────────────────────┐
  │  {color}API{reset}  : 24  │  {color}Version{reset}  : 1.0.0  │  {color}Dev{reset}  : Aldan     │
  └──────────────────────────────────────────────────────┘{reset}
"""
    print(banner)

def print_menu(selected=0, tick=0):
    color1 = rgb_color(tick, 0)
    color2 = rgb_color(tick, 1)
    color3 = rgb_color(tick, 2)
    reset = Style.RESET_ALL
    
    items = [
        ("▶ Single Round", "Sekali kirim ke semua API ", color1),
        ("⟳ Infinite Loop", "Kirim berulang dengan jeda", color2),
        ("✕ Keluar", "Tutup aplikasi            ", color3)
    ]
    
    menu = f"""
  📋 MENU UTAMA                                        
                                                         
"""
    
    for i, (label, desc, color) in enumerate(items):
        if i == selected:
            menu += f"  ┌──────────────────────────────────────────────────────┐\n"
            menu += f"  │  {color}▶ {reset}{label:<16}─ {desc}      │\n"
            menu += f"  └──────────────────────────────────────────────────────┘\n"
        else:
            grad_label = gradient_text(label, tick, i * 2)
            menu += f"  •    {grad_label:<18}─ {desc} \n"
    
    menu += f"""
  ┌──────────────────────────────────────────────────────┐
  │  {color1}↑/↓{reset}  : Navigasi  │  {color1}ENTER{reset}  : Pilih  │  {color1}Q{reset}  : Keluar  │
  └──────────────────────────────────────────────────────┘{reset}
"""
    print(menu)

def print_loading_animation(message="Processing", duration=1):
    chars = ['◐', '◓', '◑', '◒']
    tick = 0
    start = time.time()
    
    while time.time() - start < duration:
        tick += 0.1
        color = rgb_color(tick)
        idx = int((time.time() - start) * 8) % 4
        sys.stdout.write(f'\r{color}{chars[idx]} {message}...{Style.RESET_ALL}')
        sys.stdout.flush()
        time.sleep(0.05)
    print('\r' + ' ' * 50 + '\r', end='')

def input_with_animation(prompt, duration=2):
    chars = ['█', '▓', '▒', '░']
    tick = 0
    start = time.time()
    
    print(f"\n{Fore.CYAN}╔{'═' * 50}╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{Style.RESET_ALL}  {Fore.WHITE}📱 MASUKKAN NOMOR TARGET{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╚{'═' * 50}╝{Style.RESET_ALL}\n")
    
    while time.time() - start < duration:
        tick += 0.1
        color = rgb_color(tick)
        idx = int((time.time() - start) * 4) % 4
        sys.stdout.write(f'\r{Fore.GREEN}  ┌─{Fore.YELLOW} Masukkan nomor target {color}{chars[idx]}{Style.RESET_ALL}')
        sys.stdout.flush()
        time.sleep(0.05)
    
    print("\r" + " " * 60 + "\r", end='')
    print(f"{Fore.GREEN}  └─{Fore.WHITE} ➜ {Style.RESET_ALL}", end='')
    target = input()
    return target.strip()

def show_execution_table(data, tick=0):
    clear_screen()
    color = rgb_color(tick)
    
    print(f"{Fore.CYAN}┌{'─' * 58}┐{Style.RESET_ALL}")
    print(f"{Fore.CYAN}│{Style.RESET_ALL}  {color}⚡ EKSEKUSI OTP SPAMMER{Style.RESET_ALL}{' ' * (58 - 22 - len('⚡ EKSEKUSI OTP SPAMMER'))}{Fore.CYAN}│{Style.RESET_ALL}")
    print(f"{Fore.CYAN}├{'─' * 58}┤{Style.RESET_ALL}")
    
    print(f"{Fore.CYAN}│{Style.RESET_ALL}  {Fore.GREEN}Target    :{Style.RESET_ALL} {Fore.YELLOW}{data.get('target', 'N/A')}{' ' * (58 - 12 - len(str(data.get('target', 'N/A'))))}{Fore.CYAN}│{Style.RESET_ALL}")
    print(f"{Fore.CYAN}│{Style.RESET_ALL}  {Fore.GREEN}Thread    :{Style.RESET_ALL} {Fore.YELLOW}{data.get('threads', 5)}{' ' * (58 - 12 - len(str(data.get('threads', 5))))}{Fore.CYAN}│{Style.RESET_ALL}")
    print(f"{Fore.CYAN}│{Style.RESET_ALL}  {Fore.GREEN}API Total :{Style.RESET_ALL} {Fore.YELLOW}{data.get('total_api', 24)}{' ' * (58 - 12 - len(str(data.get('total_api', 24))))}{Fore.CYAN}│{Style.RESET_ALL}")
    print(f"{Fore.CYAN}│{Style.RESET_ALL}  {Fore.GREEN}Status    :{Style.RESET_ALL} {color}{data.get('status', 'Running...')}{' ' * (58 - 12 - len(str(data.get('status', 'Running...'))))}{Fore.CYAN}│{Style.RESET_ALL}")
    
    progress = data.get('progress', 0)
    bar_length = 30
    filled = int(bar_length * progress / 100)
    bar = "█" * filled + "░" * (bar_length - filled)
    print(f"{Fore.CYAN}│{Style.RESET_ALL}  {Fore.GREEN}Progress  :{Style.RESET_ALL} {color}[{bar}] {progress}%{' ' * (58 - 14 - len(f'[{bar}] {progress}%'))}{Fore.CYAN}│{Style.RESET_ALL}")
    
    print(f"{Fore.CYAN}├{'─' * 58}┤{Style.RESET_ALL}")
    
    sent = data.get('sent', 0)
    success = data.get('success', 0)
    failed = data.get('failed', 0)
    print(f"{Fore.CYAN}│{Style.RESET_ALL}  {Fore.GREEN}Sent    :{Style.RESET_ALL} {Fore.YELLOW}{sent:>4}{Style.RESET_ALL}  {Fore.GREEN}Success :{Style.RESET_ALL} {Fore.GREEN}{success:>4}{Style.RESET_ALL}  {Fore.GREEN}Failed  :{Style.RESET_ALL} {Fore.RED}{failed:>4}{Style.RESET_ALL}  {Fore.CYAN}│{Style.RESET_ALL}")
    
    if data.get('last_log'):
        log_text = data['last_log'][:40]
        spaces = 58 - 12 - len(log_text)
        if spaces < 0:
            spaces = 0
            log_text = log_text[:40]
        
        log_color = Fore.WHITE
        if 'success' in data['last_log'].lower():
            log_color = Fore.GREEN
        elif 'fail' in data['last_log'].lower() or 'error' in data['last_log'].lower():
            log_color = Fore.RED
        elif 'limit' in data['last_log'].lower() or 'block' in data['last_log'].lower():
            log_color = Fore.YELLOW
        
        print(f"{Fore.CYAN}│{Style.RESET_ALL}  {Fore.GREEN}Last Log :{Style.RESET_ALL} {log_color}{log_text}{' ' * spaces}{Fore.CYAN}│{Style.RESET_ALL}")
    
    print(f"{Fore.CYAN}└{'─' * 58}┘{Style.RESET_ALL}")

def get_key():
    try:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            if ch == '\x1b':
                ch += sys.stdin.read(2)
            return ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    except:
        try:
            import msvcrt
            return msvcrt.getch().decode()
        except:
            return None

def update_exec_data(name, status, detail=""):
    global exec_data
    exec_data['last_log'] = f"{name}: {status} {detail}"
    if status == "SUCCESS":
        exec_data['success'] += 1
    elif status == "FAIL" or status == "ERROR" or status == "TIMEOUT":
        exec_data['failed'] += 1
    exec_data['sent'] += 1
    total = exec_data.get('total_api', 24)
    sent = exec_data.get('sent', 0)
    exec_data['progress'] = int((sent / total) * 100)
    if exec_data['progress'] > 100:
        exec_data['progress'] = 100

def run_with_ui(engine_func, target, threads=5):
    global exec_data
    
    exec_data['target'] = target
    exec_data['threads'] = threads
    exec_data['total_api'] = 24
    exec_data['status'] = 'Running...'
    exec_data['progress'] = 0
    exec_data['sent'] = 0
    exec_data['success'] = 0
    exec_data['failed'] = 0
    exec_data['last_log'] = 'Initializing...'
    
    stop_update = False
    
    def update_ui():
        tick = 0
        while not stop_update:
            tick += 0.1
            show_execution_table(exec_data, tick)
            time.sleep(0.1)
    
    update_thread = threading.Thread(target=update_ui, daemon=True)
    update_thread.start()
    
    try:
        if engine_func == run_single_round:
            result = run_single_round(threads=threads, target=target, callback=update_exec_data)
        else:
            result = run_infinite_loop(target=target, callback=update_exec_data)
        
        exec_data['status'] = 'Completed' if result else 'Failed'
        exec_data['progress'] = 100
        time.sleep(1)
        return result
    except KeyboardInterrupt:
        exec_data['status'] = 'Stopped'
        raise
    finally:
        stop_update = True
        time.sleep(0.5)

def menu_navigation():
    selected = 0
    items = ["single", "infinite", "exit"]
    tick = 0
    
    while True:
        try:
            clear_screen()
            tick += 0.05
            print_banner(tick)
            print_menu(selected, tick)
            
            is_termux = os.path.exists("/data/data/com.termux/files/usr")
            
            if is_termux:
                key = get_key()
                
                if key == '\x1b[A':  
                    selected = (selected - 1) % len(items)
                elif key == '\x1b[B':  
                    selected = (selected + 1) % len(items)
                elif key in ['\r', '\n', '\x1b[C']:  
                    choice = items[selected]
                    if choice == "single":
                        clear_screen()
                        target = input_with_animation("Masukkan nomor target", 1)
                        if not target:
                            print(f"\n{Fore.RED}✗ Nomor tidak boleh kosong!{Style.RESET_ALL}")
                            time.sleep(1)
                            continue
                        
                        print_loading_animation("Memulai Single Round", 1)
                        clear_screen()
                        
                        print(f"\n{Fore.YELLOW}⚠️  Menjalankan Single Round...{Style.RESET_ALL}")
                        print(f"{Fore.CYAN}   Tekan {Fore.RED}CTRL+C{Fore.CYAN} untuk berhenti{Style.RESET_ALL}")
                        print()
                        time.sleep(0.5)
                        
                        try:
                            run_with_ui(run_single_round, target, threads=5)
                        except KeyboardInterrupt:
                            print(f"\n\n{Fore.YELLOW}⚠️ Proses dihentikan oleh user{Style.RESET_ALL}")
                        
                        print(f"\n{Fore.GREEN}✓ Proses selesai!{Style.RESET_ALL}")
                        print(f"\n{Fore.YELLOW}⏎ Tekan Enter untuk kembali...{Style.RESET_ALL}")
                        input()
                        
                    elif choice == "infinite":
                        clear_screen()
                        target = input_with_animation("Masukkan nomor target", 1)
                        if not target:
                            print(f"\n{Fore.RED}✗ Nomor tidak boleh kosong!{Style.RESET_ALL}")
                            time.sleep(1)
                            continue
                        
                        print_loading_animation("Memulai Infinite Loop", 1)
                        clear_screen()
                        
                        print(f"\n{Fore.YELLOW}⚠️  Mode Infinite Loop akan berjalan terus menerus{Style.RESET_ALL}")
                        print(f"{Fore.YELLOW}   Tekan {Fore.RED}CTRL+C{Fore.YELLOW} untuk berhenti{Style.RESET_ALL}")
                        print()
                        time.sleep(1)
                        
                        try:
                            run_with_ui(run_infinite_loop, target, threads=5)
                        except KeyboardInterrupt:
                            print(f"\n\n{Fore.YELLOW}⚠️ Proses dihentikan oleh user{Style.RESET_ALL}")
                        
                        print(f"\n{Fore.GREEN}✓ Proses selesai!{Style.RESET_ALL}")
                        print(f"\n{Fore.YELLOW}⏎ Tekan Enter untuk kembali...{Style.RESET_ALL}")
                        input()
                        
                    elif choice == "exit":
                        print(f"\n{Fore.CYAN}◐ {Fore.WHITE}Keluar...{Style.RESET_ALL}")
                        time.sleep(0.5)
                        print(f"{Fore.GREEN}✓ Sampai jumpa! 👋{Style.RESET_ALL}")
                        sys.exit(0)
                        
                elif key in ['q', 'Q']:
                    print(f"\n{Fore.CYAN}◐ {Fore.WHITE}Keluar...{Style.RESET_ALL}")
                    time.sleep(0.5)
                    print(f"{Fore.GREEN}✓ Sampai jumpa! 👋{Style.RESET_ALL}")
                    sys.exit(0)
            else:
                print(f"\n{Fore.YELLOW}ℹ️  Mode keyboard tidak tersedia, gunakan input angka{Style.RESET_ALL}")
                print(f"{Fore.CYAN}   [1] Single Round{Style.RESET_ALL}")
                print(f"{Fore.CYAN}   [2] Infinite Loop{Style.RESET_ALL}")
                print(f"{Fore.CYAN}   [3] Keluar{Style.RESET_ALL}")
                choice = input(f"\n{Fore.WHITE}Pilih (1/2/3): {Style.RESET_ALL}").strip()
                
                if choice == "1":
                    clear_screen()
                    target = input(f"{Fore.WHITE}Nomor target (08xx): {Style.RESET_ALL}").strip()
                    if not target:
                        print(f"\n{Fore.RED}✗ Nomor tidak boleh kosong!{Style.RESET_ALL}")
                        time.sleep(1)
                        continue
                    
                    try:
                        run_with_ui(run_single_round, target, threads=5)
                    except KeyboardInterrupt:
                        print(f"\n\n{Fore.YELLOW}⚠️ Proses dihentikan oleh user{Style.RESET_ALL}")
                    
                    print(f"\n{Fore.GREEN}✓ Proses selesai!{Style.RESET_ALL}")
                    print(f"\n{Fore.YELLOW}⏎ Tekan Enter untuk kembali...{Style.RESET_ALL}")
                    input()
                    
                elif choice == "2":
                    clear_screen()
                    target = input(f"{Fore.WHITE}Nomor target (08xx): {Style.RESET_ALL}").strip()
                    if not target:
                        print(f"\n{Fore.RED}✗ Nomor tidak boleh kosong!{Style.RESET_ALL}")
                        time.sleep(1)
                        continue
                    
                    print(f"\n{Fore.YELLOW}⚠️  Mode Infinite Loop akan berjalan terus menerus{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}   Tekan {Fore.RED}CTRL+C{Fore.YELLOW} untuk berhenti{Style.RESET_ALL}")
                    print()
                    time.sleep(1)
                    
                    try:
                        run_with_ui(run_infinite_loop, target, threads=5)
                    except KeyboardInterrupt:
                        print(f"\n\n{Fore.YELLOW}⚠️ Proses dihentikan oleh user{Style.RESET_ALL}")
                    
                    print(f"\n{Fore.GREEN}✓ Proses selesai!{Style.RESET_ALL}")
                    print(f"\n{Fore.YELLOW}⏎ Tekan Enter untuk kembali...{Style.RESET_ALL}")
                    input()
                    
                elif choice == "3":
                    print(f"\n{Fore.CYAN}◐ {Fore.WHITE}Keluar...{Style.RESET_ALL}")
                    time.sleep(0.5)
                    print(f"{Fore.GREEN}✓ Sampai jumpa! 👋{Style.RESET_ALL}")
                    sys.exit(0)
                    
        except KeyboardInterrupt:
            print(f"\n\n{Fore.CYAN}◐ {Fore.WHITE}Keluar...{Style.RESET_ALL}")
            time.sleep(0.5)
            print(f"{Fore.GREEN}✓ Sampai jumpa! 👋{Style.RESET_ALL}")
            sys.exit(0)
        except Exception as e:
            print(f"\n{Fore.RED}✗ Error: {e}{Style.RESET_ALL}")
            time.sleep(1)
            continue

def main():
    try:
        is_termux = os.path.exists("/data/data/com.termux/files/usr")
        
        matrix_loading(3)
        clear_screen()
        
        if is_termux:
            print(f"{Fore.GREEN}✓ Mode Termux terdeteksi{Style.RESET_ALL}")
            print(f"{Fore.CYAN}  Gunakan tombol ↑/↓ untuk navigasi{Style.RESET_ALL}")
            print(f"{Fore.CYAN}  ENTER atau → untuk memilih, Q untuk keluar{Style.RESET_ALL}")
            print()
            time.sleep(1)
        
        menu_navigation()
            
    except KeyboardInterrupt:
        print(f"\n\n{Fore.CYAN}◐ {Fore.WHITE}Keluar...{Style.RESET_ALL}")
        time.sleep(0.5)
        print(f"{Fore.GREEN}✓ Sampai jumpa! 👋{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}✗ Error: {e}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()

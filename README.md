# Blind-SQLi-extractor
A small Python tool to exploit blind SQL injection in a feedback-style form that stores user input via an unsafe INSERT. It recovers a secret (e.g., a flag) one character at a time by using the page’s response as an oracle (success vs. error).\

# How it works

 - The target app builds something like:
  - INSERT INTO feedback(username, feedback) VALUES(?, '<USER_INPUT>')
 - We submit payloads that succeed only when our character guess is correct, and fail otherwise, e.g. (SQLite example):
 - '||(SELECT CASE
           WHEN substr(secret,POS,1)='C' THEN ''
           ELSE (SELECT 1/0) END
         FROM secret_table)||'
 - The script loops over positions (POS = 1..N) and a character set until it reconstructs the value.
# Requirements
 -  Python 3.8+
 -  pip install requests pwntools (pwntools is only for nice progress UI)

# Quick Start
python3 pwntools_feedback_extractor.py \
  --url https://TARGET/ \
  --cookie '<session_cookie_value>' \
  --insecure          # if the site uses a self-signed cert
  
# What to edit (config)
 - SUCCESS_MARKER:\
   The substring that reliably appears only on a successful insert.
   - Default: "Thanks for the feedback".
   - Change it to a page-specific string (e.g., "Success", "Saved", "OK").
   - You can also switch to a more robust check (see “Choosing the success signal” below).
 - URL: The POST endpoint that accepts the feedback (often /).
 - session cookie: Replace with your valid authenticated cookie value.
 - CHARSET: Characters to try for each position (defaults to digits, A–Z, a–z, {, }, _). Add/remove symbols as needed.
 - MAX_LEN: Safety cap for maximum characters to brute force.
 - --insecure : TLS/Proxy settings for CTF labs.

# Choosing the success signal (very important)
If the target doesn’t literally print a success string, pick another stable oracle and update the script’s check accordingly:
 - Body substring (default): Set SUCCESS_MARKER to a unique success-only phrase.
 - HTTP status: Treat 2xx as success; modify the script to check r.status_code.
 - Content-Length delta: Compare len(r.text) or a header like Content-Length.
 - Regex: Match a specific HTML fragment (e.g., a CSS class that only appears on success).


# Troubleshooting
 - CERT errors: Use --insecure or import the lab CA certificate.
 - WAF/rate-limit: Increase --delay, add retries, or reduce concurrency.
 - No visible difference: Re-check your oracle; try status code or length checks.
 - Blacklists: Avoid banned keywords; the provided payload uses no WHERE/UNION/LIKE.

# Legal
 - For educational use in authorized labs/CTFs only. Do not target systems you don’t own or have explicit permission to test.

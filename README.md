# Blind-SQLi-extractor
A small Python tool to exploit blind SQL injection in a feedback-style form that stores user input via an unsafe INSERT. It recovers a secret (e.g., a flag) one character at a time by using the page’s response as an oracle (success vs. error).\

#How it works

 - The target app builds something like:\
 - INSERT INTO feedback(username, feedback) VALUES(?, '<USER_INPUT>')

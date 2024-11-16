
## The SQL WAF just said "SQLi detected" for every special character (I thought I had not yet fuzzed special character set, but the normal ones for SQL injection were flagged)

1) The leaking of source code was intended, we know this because if you go to **/console** to access the debug page it is removed, so they cleary intended to have the Debug mode enabled.
2) Character set fuzzing is something that would've been done in Hindsight had I not been able to get anywhere
3) Content-Types were changed, Request methods too, no luck. Got HEAD to work, but nothing was being actually processed or sent.
4) Still a bit confused how it bypassed, I assume the 2 "=" either caused smt to break or it did a check as **=** because of that extra one.

<img width="628" alt="Screenshot 2024-11-15 at 10 14 37 PM" src="https://github.com/user-attachments/assets/ff0db6b0-4f33-4115-a2f5-3b16f7112ca7">

<img width="717" alt="Screenshot 2024-11-15 at 10 14 44 PM" src="https://github.com/user-attachments/assets/d4954824-0382-4343-87dc-d48cad8802bc">

<img width="723" alt="Screenshot 2024-11-15 at 10 14 48 PM" src="https://github.com/user-attachments/assets/e43eff06-749e-4abc-961c-8b614d9b6a12">

<img width="788" alt="Screenshot 2024-11-15 at 10 14 51 PM" src="https://github.com/user-attachments/assets/248259d4-a200-4999-a602-73f070c44d55">

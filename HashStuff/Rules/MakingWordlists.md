hashcat --stdout -r /usr/share/hashcat/rules/OneRuleToRuleThemAll.rule your_password_file.txt > variants.txt
ffuf -request request.txt -w /path/to/your/wordlist.txt --color

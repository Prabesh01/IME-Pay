IME Pay web integration example<br>

_Disclaimer: Although I have made sure that the system is secure following recommended guidelines, I am not responsible for any of your loss caused while using these codes due to any kind of bug or security flaws herein_


# Reference: https://developer.imepay.com.np/

Create a merchant account. As of now, you have to Contact them personally and ask for API Keys.

-    Fill the provided credentials in config.py
-    git clone https://github.com/Prabesh01/IME-Pay.git
-    cd IME-Pay
-    pip install -r requirements.txt
-    python manage.py makemigrations
-    python manage.py migrate
-    python manage.py createsuperuser
-    python manage.py runserver

_Now, visit http://127.0.0.1:8000/ for the main site and http://127.0.0.1:8000/admin for admin panel_

## CronJob
_Sometimes due to various reason like server error or mid payment interruptions, even if the payment is made by the user it might not be marked as paid in the database. So use the command `python manage.py runcrons` once a while (every 5 min is fine) which makes sure to recheck such the transaction status and do the needful for the customer. It also removes cancelled and unsucessfull transactions from the database._


# Why IME Pay?
- IME Pay is pretty cool
- Which freaking wallet gives interest?
- and the free virtual and Physical VISA Card ofcourse. The cards are even found working on some international websites.
- Integration is FREE where other wallets are charging 20-25k.

# Cons :( 
- Only few banks can be linked compared to other wallets. But its just a matter of time before most banks are available.
- No web platform.
- User have to login everytime on each transaction which is irritating. Its the same for other wallets. Do something about this damnit!

# License

[![CC0](http://mirrors.creativecommons.org/presskit/buttons/88x31/svg/cc-zero.svg)](https://creativecommons.org/publicdomain/zero/1.0/)

Run the Django project (https://github.com/sannahan/cybersecurity/) by using the familiar python3 manage.py runserver in the /project1 folder. 

For logging in, use username spongebob and password squarepants. There is also another user, username larry and password thelobster. You can access the admin panel at http://127.0.0.1:8000/admin/ with username admin and password admin.  

There are four security flaws from the OWASP 2021 top ten list in the application. The fifth flaw in the application is a CSRF vulnerability.  

A01:2021-Broken Access Control 

https://github.com/sannahan/cybersecurity/blob/main/project1/accounts/views.py#L14 

Broken access control means that a user can act outside of their intended permissions. By forced browsing, an attacker can find a page that is not referenced by the application. In this application, it is http://127.0.0.1:8000/secret. It contains information that should only be visible to logged in users. 

A fix is to uncomment the line with the @login_required decorator linked above. It forces the user to log in if they are trying to access the secret page. Furthermore, it would be good practice not to name paths intended to be secret with predictable names to prevent a predictable resource location attack.  

A02:2021-Cryptographic Failures 

https://github.com/sannahan/cybersecurity/blob/main/project1/accounts/models.py#L15 

Weak cryptography (or a complete lack of it) can lead to exposure of sensitive data, such as credit card numbers. Credit card numbers should not be stored in a database without encryption. 

To fix this issue, you need to do the following: 

Proper key management includes storing secret keys used to encode and decode production data in a secure way in the production environment’s secrets. The keys should never be published in a version control system such as GitHub. To simulate this in local development, run base64.urlsafe_b64encode(os.urandom(32)).decode(‘utf-8’) in Python and export the resulting key with export FIELD_ENCRYPTION_KEY=[key] so that it can be read in mysite/settings.py#L133. (It should be noted that environment variables are not the preferred way of storing secret keys because they are accessible to all processes and might be included in the logs.) 

(Remove all previously added card numbers from the database as they are not encrypted) 

Switch the card_number field to use EncryptedCharField in https://github.com/sannahan/cybersecurity/blob/main/project1/accounts/models.py#L14, and run python3 manage.py makemigrations && python3 manage.py migrate to apply the change to the database 

You can verify that any card numbers you add after the fix will be encrypted by running sqlite3 db.sqlite3 and SELECT * FROM accounts_card. 

A03:2021-Injection 

https://github.com/sannahan/cybersecurity/blob/main/project1/accounts/views.py#L44 

SQL Injection is made possible when user data is directly concatenated to the SQL query. In http://127.0.0.1:8000/accounts, there is a bank transfer functionality that expects the user to input a source account, a destination account and an amount to be transferred. Because the SQL query is not parameterized, an attacker can for example input the value FI234567" OR 1=1 -- to the destination account field, transferring the desired amount to all bank users’ bank accounts. You can prove this by logging in as spongebob and transferring money between his accounts: because the amount is transferred to all accounts, he gains money in the transfer. 

A fix is to uncomment the correctly formatted SQL query in https://github.com/sannahan/cybersecurity/blob/main/project1/accounts/views.py#L47 . If spongebob tries the SQL injection now, he loses money. (It would be better to code this functionality to take place in a single database transaction so that money is not lost in a transfer under any conditions.) Without SQL injection, the bank transfer should transfer the money as expected. Alternatively, Django’s own database-abstraction API could be used to create an injection-safe database query. 

A05:2021-Security Misconfiguration 

https://github.com/sannahan/cybersecurity/blob/main/project1/mysite/settings.py#L26 

Security misconfiguration can mean many things, but in this project the flaw concerns error handling. A detailed error message is revealed to users. If a logged in user navigates to http://localhost:8000/error/, they see an error message “Currently on user spongebob out of all users ['admin', 'larry', 'spongebob']”, revealing all usernames currently in the database. This is because debug is set to true in the project’s settings.py. Debug should only be used in local development, and setting debug to true would be a security misconfiguration in a production environment. 

To fix this issue, set DEBUG = False in https://github.com/sannahan/cybersecurity/blob/main/project1/mysite/settings.py#L27 . In addition, avoid writing error messages that reveal unneeded and/or sensitive information. 

Not listed in OWASP but considered a flaw: CSRF 

https://github.com/sannahan/cybersecurity/blob/main/project1/accounts/templates/accounts/index.html#L20 

https://github.com/sannahan/cybersecurity/blob/main/project1/accounts/views.py#L64 

A cross-site request forgery (CSRF) means that a website is able to send an authenticated request to another website because the browser stores the authentication token. A CSRF token should be used in genuine requests to prevent a malicious party from performing a CSRF attack. 

Run python3 -m http.server 9000 in the /csrf folder and navigate to http://localhost:9000/csrf.html on the browser where you have the bank website open. The html-file contains a hidden form that sends a POST request to http://localhost:8000/message/ with the message “Please transfer 1000 from my account to charity” when the csrf-page is loading. If a bank was to act on this request, the user would lose money. 

A fix is to uncomment the csrf_token and to comment the @csrf_exempt annotation linked above. 

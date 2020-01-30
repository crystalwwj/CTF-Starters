# FINAL CTF 2020 writeup
### Team gimmemeat
* unicorn011
* iamsteven
* turtle25 

Most of the challenges are done in coordinate effort. Both the solving process and writeup are results of thorough discussion and collaboration.

### Challenges
* 2020/1/11 - 2020/1/13
* Crypto: [RSACTR](#RSACTR), Train, winner winner chicken dinner, RSACTR-revenge, back to 1997 
* Reverse: [PokemonGo](#PokemonGo), [H0W](#H0W), [VwVwVw](#VwVwVw), YugiMuto, DuRaRaRa
* Pwn: [Impossible](#Impossible), [nonono](#nonono), [re-alloc](#re-alloc), EasyROP, BlueNote
* Web: [babyRMI](#babyRMI), how2meow, [King of PHP](#King-of-PHP), echo, Low Balancer
* Misc: [Ponzi Scheme](#Ponzi-Scheme)

** solution code for is in src folder **

## PokemonGo
solved by **turtle25**

We were given a log file to trace how the program executes. Somewhere among the lines hides the mechanism that verifies the password.


### Solution
After looking at tons of meaningless messages which happens to be the system reading a file, we find the relevant part inside `PikaCheck()`. The code reads 20 bytes from the input to an array and checks the sum of consecutive elements. Namely, it checks if `a[0]+a[1]==185`, `a[1]+a[2]==212`, ... `a[18]+a[19]==172`. This means that if we choose a value for `a[0]`, we can determine the whole array. Because the flag only contains alphanumeric characters, we loop `a[0]` over all of them and choose the resulting array that looks most like a flag.

### Flag
`FLAG{PikAPikApikaPikap1Ka}`

## H0W
solved by **unicorn011, iamsteven**

We get three files: a python bytecode file (pyc), a dynamically linked library file (.so), and an output file (txt). Run the pyc and we can see that it takes an input file and creates output.txt, so we can assume that the executable encodes or encrypts the input file in some way. Also, we can infer that the functions called by the python script should be stored in the terrynini.so file.

### Solution
> After decompiling the pyc with uncompyle6, we get a python3 script which shows us how the program is executed. The flow is as follows:
```
check number of input arguments
nini3()
read input file and pad to multiple of 4 bytes
nini1()
nini4()
for every 4bytes:
    nini6(nini5(4bytes))
nini6(nini2())
```

> Now, we have to find out what each of these nini functions do! We throw terrynini.so into IDA and try to reverse the library functions. From the exported functions we can link the ninis to sub_XXX, and we can also see that these sub_XXX functions all use some special user-defined functions: ichinokata, ninokata, sannokata, yonnokata. 
> These functions all perform very simple computations:
```
ichinokata(input):
    input ^ 0xfaceb00c

ninokata(input):
    input + 74628

sannokata(input):
    rotate left 2 bits(input && 0xAAAAAAAA) | rotate right 4 bits(input && 0x55555555)

yonnokata(input):
    ichinokata(input)
    ninokata(input)
    sannokata(input)
```
> Basically we can see that ichinokata does an xor, ninokata does addition, sannokata rotates odd bits to the left (since `0xA == b'1010`), even bits to the right (since `0x5 == b'0101`), and yonnakata combines the above three. This is how our input file will be encoded!
> Next, we check to see what each of the nini functions do.
```
nini3() opens 'output.txt'

nini1():
    time(NULL)

nini4():
    srand()

nini5(input):
    choice = rand()%4
    switch(choice):
        0: ichinokata(input)
        1: ninokata(input)
        2: sannokata(input)
        3: yonnokata(input)

nini6() writes to 'output.txt'
nini2() exposes the timestamp
```
> We have a full view of the program now. For every 4 bytes in the input file, it is randomly encoded by one of the kata functions, and then the bytes are written to the output file. Finally, the timestamp is appended to the output file. Reversing the program is simple: we set the timestamp, take the input file, revert the transformation, and write to a output file.

> However, we had trouble reproducing the correct random number generator. We set the time to be `2019/08/03 5:14:25`, but somehow the results were always wrong. At first we wondered if python and c used different random number generators, so we even wrote another c file to generate the numbers, but that didn't work as well. After some time we realized that the time given wasn't what we assumed. `3` was week_day instead of month_day, and `8` was september instead of august..... no wonder our random numbers were always wrong... 
> Finally we get a valid png file!
![](https://i.imgur.com/H31eFU8.jpg)

> solution in code/H0W.py
### Flag
`FLAG{H3Y_U_C4NT_CHiLL_H3R3}`

### Notes
After successfully solving this challenge, we noticed something really stupid. If we had checked the file dates of output.txt, we would have already known that it was created on 9/11(Wed) 2019 at around 5:14 .... we didn't need to actually reverse that information at all...

## VwVwVw
solved by **iamsteven**

We get a binary file: ./verify , usage: ./verify flag, **flag is a string not a file.

### Solution

First, run the binary with ltrace,
![](https://i.imgur.com/biKpl0Y.png)
By IDA, we can find out the real length of the flag is 24. 
Then xor the flag with "***./verify./verify./verify***".
Then we do a (18bits-->24bits) transformation: (like base64) 
```
            o          n          7    (ASCII)
  011011   110110   111000   110111    (binary)

TRANSFORM

       b        2        4        3    (ASCII)
01100010 00110010 00110100 00110011    (binary)
```
We can get the result string from IDA(stored in text), and then reverse the string to get flag.  
### Flag
`FLAG{7h1s15justAbase64enc0d3!}`
### Notes
Although this is basic base64 encoding, the program doesn't take care of unprintable characters, so when we cannot just throw the discovered string into a base64 decoder and get flag.

## Ponzi Scheme
solved by **unicorn011**

After completing a proof of work we enter a page where we can choose to invest $1000 in ponzi from three options. We get the flag if we have $10000.


### Solution
> I didn't understand the challenge at first because we could only invest all our money and wait for time to pass. So I opened three tabs after three pows and waited for an hour. Afterwards, when I checked, many people had invested and ponzi had more than $76888. My account balance was $10000, so I reloaded the page and got the flag.
 
![](https://i.imgur.com/wOShID5.png)

### Flag
`FLAG{ponzi_scheme_fa_da_chai_$_$!!!}`

## Impossible
solved by **unicorn011, iamsteven, turtle25**

This is a simple pwn challenge, with protections NX only. We are asked for an input `size`, then `size` is checked before we get to send our input.

### Solution
> This is very similar to the exercises in class, where we can overflow a buffer and chain ROP to get shell. The protections are mostly off, so we don't have to leak canary or bypass other checks. The only restriction here is that our input size is checked by two passes. First, since the value of `size` is read in by scanf, it is possible that the user may input a negative value, so the program takes the absolute value of `size` if it is negative. Second, the program checks if the now positive value is larger than `0x100` and truncates `size` to `0x100`. Afterwards, the program safely assumes that `size` is well protected and takes input of `size` bytes.

> The vulnerability here is `abs()`(from this [writeup](https://bestwing.me/dragon-ctf-2018-Fast-Storage-writeup.html)). We can see that there is an overflow problem with signed int, since its range is `-2147483648 ~ 2147483647`, so if we set size to be `-2147483648 == 0x80000000`, then its value becomes `abs(-2147483648) = -2147483648`, and we bypass the too-long(`>0x100`) size check. Since `read()` takes size_t as input type, our negative `size` is interpreted as an unsigned int, and we can input much more than enough to overflow the buffer and set our ROP chain!

> The rest is pretty straightforward. Our ROP chain leaks libc address by printing the got entry of printf, and then we return to the beginning of main and repeat the process. During the second pass we do `system('/bin/sh')` and get shell.

> solution in code/impossible.py
### Flag
`FLAG{H0w_did_y0u_byp4ss_my_ch3cking?_I7s_imp0ss1b1e!}`
### Notes

## nonono
Attempted

This time we don't have source code QQQ
The challenge looks very similar to Note++, since we can add, delete, and show notes. However, we have to specify the id of the note to operate on, so we cannot use off-by-one to leak information by showing all notes.

### Solution
> We did a lot of trial and error with gdb and reversing since there is no source code. We found some interesting vulnerabilities, though we didn't figure out how to chain these holes together to form our exploit.

> First, the `index` is restricted to -256~256, so we can access memory before `note`. At first we thought we could overwrite the got table and jump to our gadgets because `index` is not checked for negative values, but then we discovered that we couldn't go beyond -256, so we couldn't touch anywhere important. However, we did notice that immediately before `note` there was an entry at `0x500508` which contained the value `0x500508`, so we could leak the binary base and bypass PIE. Step 1, get global base, check.

> The next step was to get libc address. We considered the same technique and tried to leak entries in the plt table, but it was too far away. Our next attempt was to get libc by freeing to the unsorted bin, but we couldn't figure out how to trigger a double free. When the program frees, it sets the corresponding entry in `note` to 0, which equals to setting the pointer of the deleted note to NULL. On the other hand, when we add a note, it doesn't check if the note index is already in use, so if we add two new notes with the same index, the entry in `note` is overwritten with the heap address of the second note. This means we can have floating chunks in the heap with no one pointing to them and their addresses lost. We were stuck here. Even if we could create these ghosts chunks we couldn't access them or free them again, and even if we had their addresses(calculated or leaked), we couldn't write the addresses into the entries in `note`. Also, when we allocate a new chunk, the data written is appended with a null byte, so we can't read the previously stored data, such as fd bk or main arena...

> We were stuck here since we couldn't do a double free and didn't know what to do with the negative index except leak global base.

> partial code in code/nonono.py
### Flag
Not obtained.
### Notes

## babyRMI
Attempted

Do you know Java RMI? 
No I don't.

### Solution
> I didn't know java RMI, so I googled a lot about it. According to [this source](http://www.codersec.net/2018/09/%E4%B8%80%E6%AC%A1%E6%94%BB%E5%87%BB%E5%86%85%E7%BD%91rmi%E6%9C%8D%E5%8A%A1%E7%9A%84%E6%B7%B1%E6%80%9D/) and [this writeup](https://github.com/ALLESCTFTeam/ctf/tree/master/2018/RealWorldCTF2018_Finals/RMI), java RMI is a method to invoke remote procedure calls. Since it uses object serializtion to transfer objects between client and server, there is a deserialization vulnerability. If we can trigger certain gadgets on the java class path libraries, we can get RCE. We get a RMI endpoint that runs on port 11099, so if we create a RMIclient and send a commonscollections RCE object to the server, we can get any command executed. However, in the newer JRE there is a RMI Registry Filter, so if we try to run the same payload we get a rejected message. The solution would be to run a JRMP listener and client from the ysoserial exploitation library, and use UnicastRef object to bypass filter checks.

### Flag
Not obtained.

### Notes

## King of PHP
Attempted

This web challenge allows us to upload a file to a randomly generated file path. That path is known to us. We can also read arbitrary files by giving a filename to `file_get_contents()`.

### Solution
> Because we can control the contents of the file that we uploaded and read it afterwards, the first thing that comes to mind is to use local file inclusion. However, in this case we only have `file_get_contents()` instead of `include()`, so normally we cannot execute any code. To achieve code execution with `file_get_contents()`, we can make use of the Phar deserialization vulnerability. Here we are stumped because we cannot give a filename starting with **p**, and we need a filename that begins with the `phar://` wrapper. Our attempts end here during the competition.

> After the end of the competition, we find out that `compress.zlib://phar://<filename>` can be used to bypass the filter. We should be able to get the flag following this line of thought.
### Flag
Not obtained.

### Notes
During our many attempts, we stumbled accross a file `readflag.c` in the root directory. From the contents we know that the flag is in the file `/why_the_flag_name_is_so_weird`. However, we do not have enough privilege to read that file. Such a careful author.

## RSACTR
Attempted

This problem uses RSA as the encryption for the Counter (CTR) block cipher mode. For each block(16 bytes) of the flag, a number(`nonce`) is encrpted with the private key and added to the block. `nonce` is then incremented by 2020 after each encryption. Next it will encrypt `nonce+2020` with the private key, add it to the block, and so on.

The public key is known, so we can decrpyt any message encrypted by the private key.

### Solution

> We are allowed to give a message for the program to encrypt. If we send 16 null bytes, the program will return an encrypted nonce + 0. Using the public key, we can know the value of nonce.

> The problem is that we can only know the value of (encrypted nonce + flag), but not (encrypted nonce).
> 
> We have tried to find the private key as follows:
> In the first try, we send 16 null bytes, hence (encrypted nonce) is known. In the second try, nonce is incremented by 2020 and we get (encrypted (nonce + 2020)) or we can write it as 
![](https://i.imgur.com/n9xdT37.png)
> Since we have 
![](https://i.imgur.com/9yrqLjn.png)
![](https://i.imgur.com/KvUKGBU.png)
> But still, we can not obtain private key d from these information.

> Next, we tried to find the relationship between each try. In the first try and second try, we both send 16 null byte as input, but in the last try, flag is chosen as input. Therefor the information we get would be:
(1) ![](https://i.imgur.com/0SPALtj.png)
(2) ![](https://i.imgur.com/zVBTB7Y.png)
(3) ![](https://i.imgur.com/H96Pqwi.png)
> Let the information be r1,r2,r3 respectively. 
> We can conclude that 
![](https://i.imgur.com/OHzRkVZ.png)
> for some integer q1,q2,q3.

> We would like to find some relationship like
![](https://i.imgur.com/R88u5hR.png) 
> for some constant c. 
> If we can calculate c, then after the modulo-n operation we would get: ![](https://i.imgur.com/8L4LrKD.png), and the flag is found.
> Using the binomial theorem,
![](https://i.imgur.com/1lFqqnY.png)

> But power of 2 here depends on d and i, thus it is not a constant. 
> Another attempt is that
![](https://i.imgur.com/QOgA06n.png)
> The ratio here does not depend on d anymore, but it is still not a constant. 
> The relationship is not found.

### Flag
Not obtained.

### Notes
After observing the code of RSACTR-revenge, we find that the only change is e is much larger. e is 3 in RSACTR while it is 4097 in RSACTR-revenge. We suspect that the small e plays an important role in solving this problem, but we are not able to take advantage of this.

## re-alloc
Attempted

As the name suggests, the program uses `realloc()` to simulate the functionalities of `alloc()` or `free()` or both at the same time. We can allocate up to two blocks of memory, with sizes no larger than 0x78 bytes.

We know that the program runs with `libc2.29`, so freed memory will be managed by tcache.


### Solution
> We identified a vulnerability in the function `allocate()`. If we fill the data right up to the size of the block, we can create a off-by-one null byte injection.
> As far as we can tell, we cannot exploit use after free or double free because `rfree()` will set `ptr = NULL`.
> We also lack a way to leak information such as libc address becuase we cannot print out the contents of an allocated block.
> We don't know how to proceed from here. Without other major vulnerabilities, we can't even make use of the supposedly more unsafe (compared to fastbin) tcache mechanism.

### Flag
Not obtained.

# CTF HW7 Writeup

Topic: Binary

### Problem 1: Casino++

#### Problem description

> The source code is exactly the same as last week's challenge casino, with the only difference being NX enabled this time.

#### Solution

> With NX enabled, we are unable to put shellcode in `name` like we did last time and jump to the shellcode by got table hijacking. So what do we do? Our first try was using `ret2csu` because the TA hinted about it being an incredibly powerful solution. `ret2csu` would be the equivalent to any ROP chain solution because if we can overflow some buffer and write ROP gadgets over the return address we can also write all the values we need for `ret2csu` on the stack. But the problem is, we can't write on the stack! We tried to access the stack from indexing the `guess` array, but `guess` is in `0x602070` and the stack is somewhere around `0x7fff00000000`, the distance is too large(larger than a `int` could carry) and would overflow the index. So, we are unable to access the stack and write our ROP chain over the return address. The next idea we had was to use one gadget, but all of the one gadgets failed, because we couldn't satisfy the constraints(partly due to the fact that we cannot control the stack). We were stuck for a while because people in the chatroom talked about using ROP chains, but we had no idea how to chain gadgets and control their values by inserting on the stack.

![](src/stacksofar)

> Then I had an idea. I remembered from last week's challenge that I had tried to overwrite the got table of printf, puts, and atoi. You can see from the code snippet below that when casino does `readint()`, it takes input from the user and feeds it into `atoi`. Since `system` is clearly not in the code and we have no way of using gadgets to perform a syscall, I thought maybe I could use indexing to change `atoi` into `system` and the next time `readint()` is called, I can input `/bin/sh` and get a shell! The only problem was that `readint()` is called when casino asks for an input, so I will have to change the address during the first attempt of the game(which means only 4 bytes of the address). That is not a problem, because `system` should be close to `atoi` in libc, so we should only have to change the last few bytes. We tried in gdb and was successful in opening a shell! This means if we know where `system` is located we can RCE. So the next step would be to leak libc base address.

> Now that we know we have to leak libc, we can't just play casino once, because if the game ended after leaking libc, we can't hijack `atoi` into `system` anymore. So the next thing we do is to try to get the game repeating. During the first pass, we change `puts` into `casino` so that it iteratively calls itself again and again until we lose and each layer pops itself to exit the game. As long as we input the correct guesses, we will have endless chances to do other things with indexing. 

> Our flow is now as follows:
* First pass: change `puts` to `casino` to keep the game repeating
* Second pass: try to leak libc base address and find `system`
* Third pass: use leaked address to change `atoi` to `system`
* input `/bin/sh` in the next `readint()` and get shell

> We have done the first part, and now we have to leak libc. This is where we got stuck. HOW DO WE LEAK LIBC? We have to use the libc functions in the plt table, because using any other function in libc requires that we already know where the libc base is. We thought about changing `atoi` to different functions every time, because this is the only function where we can give arbitrary input, but the problem is that atoi becomes broken and we can't change it into anything else because `guess` will be overwritten by trash. We can't use `put` either, because it is already changed to system and we can't control the string input to `put` in the program. After a really long time we suddenly had an idea. What if we changed `srand()` to `printf()` and control the `seed` to be the address of a got entry? We already know that we can overflow the seed with a long `name`, so if we give `seed` some value such as `0x602020` we can leak the address libc function! The input we gave `name` was something like `'A'*16 + '\x20\x20\x60\x00' + 'A'*16`, and once we confirmed the `rand()` numbers with gdb we can input the correct guesses and complete our exploit! We got our libc base address and from the given libc.so we calculated the correct offset of system. By the way, we truncated the address of `system()` to only the latter half because we suppose it shouldn't be that far away.

![](src/finalexp)

> Finally, after much trial and error, we successfully repeated the game, leaked libc, and executed arbitrary syscall. I still don't know how to chain ROP gadgets to solve this challenge, but I think our solution is quite creative and simple!
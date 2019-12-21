# CTF HW5 Writeup

Topic: Binary

### Problem 1: Casino

#### Problem description

> We get a c file and an executable. The executable declares global variables such as `name`, `age`, `lottery`, `guess`, `seed`, and later takes user input to populate these variables. The casino game randomizes `lottery` with the `seed`, takes user input as `guess`, and checks against `lottery` for two rounds. If any of the results are all correct, the program outputs success(otherwise fail).

#### Solution

> The first thing we do when we get these files is to check the file type. We see that this is a linux x86-64 executable, unstripped. The next thing we do is read the c code and run the file in gdb, disassembling `main` and `casino` to see where everything is stored. We look into the `puts@plt` and see that `puts@got` is located in `0x602020`, which means we can hijack the got table if we modify the address stored at `0x602020`. 

![](src/pltputs)

> Then I typed in a bunch of `A` as input to the user name, and randomly chose `430` as the age to see where data is stored, and the result is the figure below. We can see that the red rectangle shows `puts@got` (in `0x602020`), then comes the `lottery` and `guess` arrays, and then the `name` which we overflowed with `A`(0x41). After the `name` comes two integers `age` and `seed`, which I have highlighted with a yellow rectangle for `age` and blue rectangle for `seed`. Wait.... did we just overflow the `seed`? This is when we realized that the lottery isn't random at all! We can give the name a long value so that it overflows the seed and we can control the input to our guesses, which eventually means we can reach the "You win!" condition! After poking around the binary, the formation is relatively simple. We launch a GOT hijacking attack by inserting shellcode in `name` and redirect `puts` to the address of `name`!

![](src/data)

> Before I go on to the exploit, I would like to discuss some other ideas we had when brainstorming this problem. First of all, there are many functions in the code which we could potentially exploit, such as `puts()`, `printf()`, `atoi()`...... In fact, we went through each of these functions before settling on `puts()` because we were initially convinced that randomness could not be predicted(yes we weren't careful enough to notice that `name` is assigned **after** `seed` QQ). The 3 ideas are as follows:

* Put shellcode in `name` and exploit `printf()`. Since `printf()` is called just about everywhere, our idea was to overwrite its address in the first iteration of the while loop, so that at the beginning of the second iteration, we will call `printf()` immediately and get our shell!
* Nevermind `name` or shellcode. During the first iteration we exploit the "You lose" string (at ) and rewrite it with "/bin/sh", and we exploit the second iteration's `printf()` so that it points to `system`. This is sort of like a return-to-libc attack though we don't have libc file. 
* Nevermind `name` or shellcode. We exploit `atoi()` so that it points to `system`. During the second iteration, when we are asked for a new guess, we input `/bin/sh` as input to `atoi()` so that the function becomes `system("/bin/sh")`. We had to code "/bin/sh" to decimal notation for the input to work.

> In retrospect, each of these ideas seemed plausible, and we did actually try all of them, though, of course, none worked. But it was really fun to just be creative and try to find as many gadgets as possible, and even though we didn't succeed with any of them, we realized **how** we made several mistakes and learnt a lot from these experiences. One of the main obstacles was that we thought only one iteration was enough to overwrite the address of the got entry, so we ended up thinking about how to utilize the second iteration to get shell. In fact, we **needed** the two iterations to successfully perform a got hijack, so the only possible candidate was still `puts` and we had to get into the "You win" condition to do that. And of course, if we had realized earlier that we could control the `seed`, we would never have suspected the other external functions at all. Which now seems like a blessing in disguise :)


> Back to the exploit. Now we know we have to put shellcode in our `name` variable, but we also see that our chain of A's is interrupted by the `age` variable. The work around would be to enter a sled of A's(or just about anything else) long enough to overflow the `seed` and then append the shellcode after that. To simplify addressing, we chose 0x20 A's since it covers exactly 2 rows and we can redirect out `puts` to `name+0x20`. Next don't forget that we have to actually win the lottery in order to call `puts`, so after `lottery` is assigned, keep track of the numbers so that you can enter them in the second iteration of the game! 

![](src/lotto)

> Now comes the important part of this problem. How do we hijack the address of `puts@got`? According to a tutorial I found from HITCON workshops, we can find the addresses of `puts@got` and an array that we have read/write access to (and doesn't check index boundaries), so that later on we can calculate the offset of these two addresses and overwrite `puts@got`! Since the address is 8 bytes long, but we can only access 4 bytes at a time(array `guess` contains 4-byte `int`), we have to write four bytes during the first iteration and another 4 bytes during the second iteration. So the final exploit is as follows: we get the address from the ELF and calculate offsets, then during the first iteration we input random/wrong guesses (we don't want the game to end on the first round!) and overwrite the higher 4 bytes of the address; during the second round we input **correct** guesses (in order to reach `puts()`) and overwrite the lower 4 bytes of the address. Voila!

> Testing on local and remote, we get the shell! As a sidenote, when I used pwntools to send the correct guesses I accidentally wrote them in hex, so the `atoi()` was completely wrong QQQQQ 
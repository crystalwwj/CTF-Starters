# CTF HW3 Writeup

Topic: Web Security

### Problem 1: Unexploitable 

#### Problem description

> A website with nothing on it but a matrix animation.

#### Solution

> There's nothing on the website except the animation, and we can't get any information from the source html. So we tried to changing the url to access some arbitrary files, such as `unexploitable.kaibro.tw/secret` and `unexploitable.kaibro.tw/flag`. Aha! We get 404 not found responses, but the response came from a github page. 

![](src/404git)

> Then we tried searching for the challenge website in github and found a github repository named Bucharesti. Digging into the commit history we found a deleted file. That's our flag!

![](src/gitrepo)
![](src/gitflag)


### Problem 2: Safe R/W 

#### Problem description

> We get a php file reader writer which asks for a directory name, a filename, and some message content. It opens a sandbox, makes a directory, writes the message contents into a file named `meow` and outputs the contents in the specified filename.

#### Solution

> This seems like a local file inclusion(LFI) to remote code execution(RCE) challenge. There are several restrictions: open_basedir is on so we can’t include files beyond the directory of `var/www/html`; $i may not contain the letters `ph` so we cannot explicitly type a php extension name; $c is restricted to 20 chars, it’s impossible to stuff a complete reverse shell. 

> Our idea was to somehow bypass the filtering in `file_get_contents()` but still allow include to read our php code. The php code in $c would have to be short but allowing arbitrary length commands, something like `<?php system(_GET[exp]);` where we can give _GET parameters to get RCE. The problems burns down to bypassing ‘<’ check, which took us 15+ hours and still couldn’t figure out. My first instinct was to use the `data://` wrapper since we cant hen encode the php code in base64 and pass it into the contents, but after reading docs and manuals and local experiments, we discovered that we were able to include pure php code but unable to evaluate/execute it! For example, we could  `include(‘data://text,plain;base64,PD9waHAgc3lzdGVtKF9HRVRbYWFdKTs=’)` and it would return `<?php system(_GET[aa]);` instead of executing it. If we tried `include(‘data://text,plain;base64,bXlkaXIvbWVvdw==’)` it would return the equivalent of `include(mydir/meow)` but not actually read the file! We guessed that the wrappers only work once(decode once) and the result is treated as a plaintext, so that trying to encode the filename and/or php code in base64 either resulted in bypassing both `file_get_contents()` and `include()` or didn’t pass either. We tried other wrappers but none of then really suited our purpose. There was no file uploading(even though phpinfo.php actually shows the option to be true) and allow_url_include was off(which was another reason why `data://` didn’t pass `include()`). We’re stuck here QQQQQQ

> NOTE: after another few days we received the hint that `data://` and `data:` behaved differently...... We were right about tricking `file_get_contents()` to spit out a warning but still pass the check, and `include()` should work fine. Omitting the double slashes after `data:` and our reverse shell worked.... We were so close QQQQQ
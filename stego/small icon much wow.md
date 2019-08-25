# small icon much wow
* hackcon19/20190823
* stego/100 pointes/500 points

### Challenge
One of my friends like to hide data in images.Help me to find out the secret in image.
![Alt text](https://github.com/crystalwwj/CTF-Starters/tree/master/stego/src/stegohackcon19.jpg)

### Solution
This is a simple challenge easily solved with binwalk.
Checking the jpg with binwalk we get:

![Alt text](https://github.com/crystalwwj/CTF-Starters/tree/master/stego/src/stegohackcon19solve.png)

We see another jpg file! Extracting the file using binwalk we get another jpg which appears to be a QRcode. A simple scan leads us to a google search page with the keyword `d4rk{flAg_h1dd3n_1n_th3_thumbnail}c0de`.
This is our flag.

### Flag
d4rk{flAg_h1dd3n_1n_th3_thumbnail}c0de


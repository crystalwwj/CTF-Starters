# NOKI

* hackcon19/20190823 

* crypto/198points/500points

### Challenge

I was told Vigenère Cipher is secure as long as length(key) == length(message). So I did just that!

Break this: g4iu{ocs_oaeiiamqqi_qk_moam!}e0gi

### Solution

d4rk{   _          _  _    !}c0de

translate twos strings by {a = 1,b = 2........z=26} 

then get

7, ,9,20,{....}5, ,7,9

4, ,18,11,{...}3, ,4,5

We can find the number of ciphertext is 2*plaintext - 1 (mod26) ( Due to mod26, there can be two cases of plaintext, and then choose the reasonable one)

### Flag

Get the answer d4rk{how_uncreative_is_that!}c0de

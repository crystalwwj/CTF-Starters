# CTF HW46Writeup

Topic: Web Security

### Problem 1: TinyURL

#### Problem description

> We get a web service that shortens any given url that starts with http:// or https://. There is clearly a SSRF vulnerability since the server requests the user defined url during preview (without any checks) and we can exploit Redis which is running on 6379 in the intranet to RCE.

#### Solution

> Redis can be used for many purposes, and the most common vulnerabilities are arbitrary write and session storage. Attacks that use arbitrary write often a) try to write the attacker’s ssh key to the authorized list to gain login access, or b) write crontab files to periodically execute commands, or c) write to job queues. In this challenge, Redis is used as session storage, so we can try to use “unsafe serialization” to get RCE. The point of deserialization is to exploit the fact that python pickle relies on __reduce__ to dump and load objects, so we can pack our reverse shell into a serialized payload, and set the corresponding value of our session id to this malicious payload. As a result, when the server receives another request with the spoofed session id, it will deserialize our injected malicious payload and execute the command. I tested dumping and loading locally and a shell opened up in my terminal. 

> We open two browsers, since each browser gets a unique cookie and we cannot forge the session data that we are currently using. We have browserA and browserB open on the Tinyurl site. The attack flow is as follows:
1. Construct a url so that the server will send a request to redis, commanding it to set the value of browserB session id to our malicious payload. We exploit CVE-2019-9947 which allows an attacker to inject arbitrary HTTP header due to a flawed url parser. Run the request with pos data url in browserA.
2. We take the shortened url and run it in browserA again, but we get another 500 error, probably due to the urlopen() not working properly(there is no url to retrieve afterall). After this step the redis command should be done and we should have injected a fraudulent session entry in the cache.
3. We open the browserB and refresh the website. Get reverse shell!

> src/url.py describes how we constructed our malicious payload. Basically it is
![](src/payload)

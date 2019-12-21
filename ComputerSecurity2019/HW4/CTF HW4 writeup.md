# CTF HW4 Writeup

Topic: Web Security

### Problem 1: Cathub 2.0

#### Problem description

> A website similar to youtube with cat videos, a register panel, a login page, upload links, and search requests. But the register and upload scripts don’t work. There is a login prompt which might be vulnerable, and a search function that returns cat videos.

#### Solution

> Since I read the chatroom dialogues daily, I know this is a SQL injection problem XDDD Early on I wasn’t sure where to do SQL injection since the only prompt I get is the login form, but using sqlmap I get the response that both `user` and `pass` is not vulnerable to SQL injection. Besides, I tried MySQL, Oracle, SQLite, Cassandra, MSSQL… on the login form but none of the db tests work. By the way, the injection string is filtered through a WAF and we get a ‘bad cat’ error if it contains spaces, single quotes(‘), plus(+), or semicolon(;). Then I saw the hint about watching cat videos, so I went through the cat video results and saw that they were loaded in `video.php` with a get parameter `vid`. I went through a dbms list and discovered that the database was written with Oracle (since it was the only one that didn’t give me an error), so I tried sqlmap and this time it told me `vid` was susceptible to ‘boolean-based blind injections’ and ‘time-based blind injections’, which I found several materials on. Since Oracle didn’t have `limit 1,1` as the lab did, I had to use `offset n rows` to iteratively brute force all the schema names, table names, and column names. There were many schema names but the only reasonable one to use was ‘SCOTT’, and the table name and column names were easy to spot, which were ‘S3CRET’ and ‘V3RY_S3CRET_C0LUMN’. Putting all these information together we get our final exploit. 
`“https://edu-ctf.csie.org:10159/video.php?vid=1%09and%090=1%09union%09SELECT%09NULL,V3RY_S3CRET_C0LUMN,NULL%09FROM%09SCOTT.S3CRET--"`


### Problem 2: How2XSS

#### Problem description

> We are asked for a ‘hack me’ prompt and a md5 hash of the code(in case of DDOS attacks XDDD), then if we can get the cookie, we can try our exploit on the report to admin page. The flag is in admin’s cookie.

#### Solution

> So far I was able to alert(1), but nothing more. My idea was to include a script in the report, such as <svg/onload=“url to a php file on my machine”> so that the page will connect over to a file under my domain and control. My page will take document.cookie as input, so when the admin links over I will get his cookie! 
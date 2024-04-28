import hashlib

passwd = input("明文密码：")
print(hashlib.sha256(str(passwd).encode('utf-8')).hexdigest())
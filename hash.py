import hashlib

email = 'shaon@gmail.com'
pwd = 'chairOnTableWith3Legs'
pwd_encode = pwd.encode()
pwd_hash = hashlib.md5(pwd_encode).hexdigest()
print(pwd)
print(pwd_hash)

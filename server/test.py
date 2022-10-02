import hashlib

login = 'whom'
password_not_hashed = '12344321qwe'
password_hashed = hashlib.sha256(password_not_hashed.encode())
print(password_hashed.hexdigest())
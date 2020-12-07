```
ubuntu 20
Python 3.7.2
pip 18.1
OpenSSL 1.1.1f  31 Mar 2020
```

build

```
apt-get install openssl
pip3 install flask
```

execute

```
python3 app.py
```

commands
```
curl http://localhost:5000/pk > public.pem

curl -X POST -H "Content-Type: multipart/form-data" -F "data=@example.txt" http://localhost:5000/sha3 > hash

curl -X POST -H "Content-Type: multipart/form-data" -F "hash=@hash" http://localhost:5000/sign > hash.sig

curl -X POST -H "Content-Type: multipart/form-data" -F "hash=@hash" -F "sig=@hash.sig" http://localhost:5000/verify
```
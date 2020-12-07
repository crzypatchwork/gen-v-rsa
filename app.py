from flask import Flask, request
import subprocess
import os 

app = Flask(__name__)

# https://stackoverflow.com/questions/40565364/generating-signing-and-verifying-digital-signature

@app.route('/gen')
def gen_keys():

    try:
        sk = subprocess.check_output("openssl genrsa -out private.pem 1024", shell=True)
        pk = subprocess.check_output("openssl rsa -in private.pem -out public.pem -outform PEM -pubout", shell=True)
        return { 'status' : 200 }
    except:
        return { 'status' : 500 }

@app.route('/sha3', methods=['POST'])
def sha3():

    sha3 = subprocess.check_output("echo -n '{}' | openssl dgst -sha3-512".format(request.files['data'].read()), shell=True)
    sha3 = str(sha3).split('= ')[1][:-3]
    subprocess.call("echo -n '{}' > hash".format(sha3), shell=True)

    os.remove('hash')

    return sha3

@app.route('/sign', methods=['POST'])
def sign_hash():

    with open('hash', "wb") as file:
        file.write(request.files['hash'].read())

    subprocess.call('openssl dgst -sha256 -sign private.pem -out hash.sig hash', shell=True)
    
    with open('hash.sig', 'rb') as file:
        contents = file.read()   

    os.remove('hash')
    os.remove('hash.sig')

    return contents

@app.route('/verify', methods=['POST'])
def verify():

    with open('hash', "wb") as file:
        file.write(request.files['hash'].read())

    with open('hash.sig', "wb") as file:
        file.write(request.files['sig'].read())    

    res = subprocess.check_output('openssl dgst -sha256 -verify public.pem -signature hash.sig hash', shell=True)

    os.remove('hash')
    os.remove('hash.sig')

    return { 'status' : res.decode("utf-8") }

@app.route('/pk')
def pk():

    data = open('public.pem').read()    
    return data

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

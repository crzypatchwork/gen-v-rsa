from os import environ
import subprocess
from flask import Flask, request

app = Flask(__name__)

# https://stackoverflow.com/questions/40565364/generating-signing-and-verifying-digital-signature

@app.route('/gen')
def gen_keys():
    sk = subprocess.check_output(
        "openssl genrsa -out private.pem 1024", shell=True)
    pk = subprocess.check_output(
        "openssl rsa -in private.pem -out public.pem -outform PEM -pubout", shell=True)
    
    print(pk)
    # return bytestring
    return pk 


@app.route('/sha3', methods=['POST'])
def sha3():

    sha3 = subprocess.check_output(
        "echo -n '{}' | openssl dgst -sha3-512".format(request.files['data'].read()), shell=True)
    print(sha3)
    sha3 = str(sha3).split('= ')[1][:-3]
    subprocess.call("echo -n '{}' > hash".format(sha3), shell=True)
    return sha3

@app.route('/sign')
def sign_hash():
    subprocess.call('openssl dgst -sha256 -sign private.pem -out hash.sig hash', shell=True)
    
    #return bytestring
    return { 'status' : 200 }

@app.route('/verify')
def verify():

    subprocess.call('openssl dgst -sha256 -verify public.pem -signature hash.sig hash', shell=True)

    # return bytestring
    return { 'status' : 200 }

if __name__ == '__main__':
    from os import environ
    app.run(debug=True, host='0.0.0.0', port=environ.get("PORT", 5000))

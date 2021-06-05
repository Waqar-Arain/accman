import os
import sys
import base64
import hashlib
import argparse
import pyperclip
from getpass import getpass
from signal import signal, SIGINT
import yaml
import scrypt
import colorama
from termcolor import colored
from cryptography.fernet import Fernet
colorama.init()

def main():
    parser = argparse.ArgumentParser(description = 'Your own very secure account manager.')
    group_parser = parser.add_mutually_exclusive_group()
    group_parser.add_argument('--read', help='name of the account you want to find. e.g "python accman.py --read twitter"')
    group_parser.add_argument('--write', help='to insert account information. e.g "python accman.py --write"', action='store_true')
    group_parser.add_argument('--list', help='listing all the saved accounts. e.g "python accman.py --list"', action='store_true')
    group_parser.add_argument('--delete', help='delete any listed account. e.g "python accman.py --delete"', action='store_true')
    group_parser.add_argument('--clean', help='clean all account data from files. e.g "python accman.py --clean"', action='store_true')
    group_parser.add_argument('--gpass', help='set global password. e.g "python accman.py --gpass"', action='store_true')
    args = parser.parse_args()
    if args.read:
        data_reader(args.read)
    if args.write:
        data_writer()
    if args.list:
        listingAccounts()
    if args.delete:
        deletingAccount()
    if args.clean:
        cleaning()
    if args.gpass:
        globalPass(0)
    if len(sys.argv) == 1:
        parser.print_help()

def loc():
    #setting up path
    files_path = os.path.expanduser('~')
    if os.path.exists(f'{files_path}/.accman/') == True:
        pass
    else:
        os.mkdir(files_path+'/.accman/')
    return files_path

def getData(name, encrypted_data):
    #getting password
    passwd = getpass('Please type in the security password assigned to this account: ')
    passwd = passwd.encode()
    files_path = loc()
    try:
        #getting salt
        with open(f'{files_path}/.accman/salt.yml', 'r') as d:
            y = yaml.safe_load(d)
            try:
                salt = y[name]
                for k in salt:
                    salt = salt[k]
                salt = salt.encode()
            except:#TypeError & KeyError
                print(colored('\nProgram is unable to find Salt for this account!\n', 'red', attrs=['bold']))
                exit(0)
    except FileNotFoundError:
        print(colored('\nProgram is unable to find Salt file!\n', 'red', attrs=['bold']))
        exit(0)
    #generatting key
    key = scrypt.hash(passwd, salt, 2048, 8, 1, 32)
    key = base64.urlsafe_b64encode(key)
    f = Fernet(key)
    #decryptting data
    encrypted_data_items = []
    decrypted_data_items = []
    for i in range(len(encrypted_data)):
        encrypted_data_items.append(encrypted_data[i].encode())
        try:
            decrypted_data = f.decrypt(encrypted_data_items[i])
            decrypted_data_items.append(decrypted_data.decode())
        except:
            print(colored('\nYour password might be incorrect!\n', 'red', attrs=['bold']))
            exit(0)
    return decrypted_data_items

def keygen(name=None, passwrd=None):
    #generating key
    salt = os.urandom(16)
    passphrase = hashlib.sha256(salt)
    passphrase = passphrase.hexdigest()
    if passwrd == None:
        passphraseDict = {
            name:{
                'salt': passphrase
            }
        }
        passwd = getpass(prompt='this password will be used to encrypt account data, it will not be saved for security purposes: ')
        passwd = passwd.encode()
    elif passwrd != None:
        passphraseDict = {
            'GlobalSalt':passphrase
        }
        passwd = passwrd

    files_path = loc()
    try:
        #saving generated salt
        if passwrd != None:
            with open(f'{files_path}/.accman/data.yml', 'r') as d:
                y = yaml.safe_load(d)
                y.update(passphraseDict)
                encryptedFile = open(f'{files_path}/.accman/data.yml', 'w')
                encryptedFile.write(yaml.safe_dump(y,  sort_keys=False))
                encryptedFile.close()
        else:
            with open(f'{files_path}/.accman/salt.yml', 'r') as d:
                y = yaml.safe_load(d)
                y.update(passphraseDict)
                encryptedFile = open(f'{files_path}/.accman/salt.yml', 'w')
                encryptedFile.write(yaml.safe_dump(y,  sort_keys=False))
                encryptedFile.close()
    except:
        if passwrd != None:
            encryptedFile = open(f'{files_path}/.accman/data.yml', 'w')
            encryptedFile.write(yaml.safe_dump(passphraseDict,  sort_keys=False))
            encryptedFile.close()
        else:
            encryptedFile = open(f'{files_path}/.accman/salt.yml', 'w')
            encryptedFile.write(yaml.safe_dump(passphraseDict,  sort_keys=False))
            encryptedFile.close()

    #returning key
    key = scrypt.hash(passwd, passphrase, 2048, 8, 1, 32)
    key = base64.urlsafe_b64encode(key)
    return key

def doesAccountExists(name):
    files_path = loc()
    try:
        #checking if the typed account exists or not
        with open(f'{files_path}/.accman/information.yml', 'r') as d:
            y = yaml.safe_load(d)
            if name in y:
                user_input = input('Account already exist, do you want to overwrite your account? (yes/no) ')
                if user_input == 'yes':
                    return True
                if user_input == 'no':
                    byebye()
                    exit(0)
                else:
                    print(colored('\nInvalid Input!\n', 'red', attrs=['bold']))
                    exit(0)
    except FileNotFoundError:
        return True

def data_writer():
    #setting up global password
    globalPass(0)
    #getting account information
    name = input('Name of the website: ')
    doesAccountExists(name)
    website_addr = input('Website address: ')
    usr_name = input('Account username: ')
    passwd = getpass(prompt='Account password: ')
    other_info = input('Other information: ')
    #getting key to encrypt that information
    key = keygen(name, None)
    f = Fernet(key)
    info = [website_addr, usr_name, passwd, other_info]
    encoded_data = []
    for i in range(len(info)):
        encoded_data.append(f.encrypt(info[i].encode()))

    data = {
        name:{
            'website address': encoded_data[0].decode(),
            'username': encoded_data[1].decode(),
            'password': encoded_data[2].decode(),
            'other information': encoded_data[3].decode()
            }
        }
    files_path = loc()
    try:
        #saving account information
        with open(f'{files_path}/.accman/information.yml', 'r') as d:
            y = yaml.safe_load(d)
            y.update(data)
            encryptedFile = open(f'{files_path}/.accman/information.yml', 'w')
            encryptedFile.write(yaml.safe_dump(y,  sort_keys=False))
            print(colored('\nData written successfully!\n','cyan'))
            encryptedFile.close()
    except:
        encryptedFile = open(f'{files_path}/.accman/information.yml', 'w')
        encryptedFile.write(yaml.safe_dump(data,  sort_keys=False))
        print(colored('\nData written successfully!\n','cyan'))
        encryptedFile.close()

def data_reader(usr_input):
    files_path = loc()
    try:
        #fetching file information
        with open(f'{files_path}/.accman/information.yml', 'r') as d:
            y = yaml.safe_load(d)
            try:
                encrypted_account = y[usr_input]
                encryptedItems = []
                for i in encrypted_account:
                    encryptedItems.append(encrypted_account[i])

                #decrypting the fetched data
                decrypted_items = getData(usr_input, encryptedItems)
                #printing account information
                print()
                print('     '+colored(usr_input,'cyan')+':')
                c = 0
                for key in encrypted_account:
                    if c==2:
                        print('\t'+'|'+ colored(key,'green',attrs=['bold']) +': '+ colored('Copied to clipboard','cyan'))
                        pyperclip.copy(decrypted_items[2])
                    else:
                        print('\t'+'|'+ colored(key,'green',attrs=['bold']) +': '+ colored(decrypted_items[c],'red',attrs=['bold']))
                    c+=1
                print()
            except KeyError:
                print('\n     '+colored(usr_input,'cyan')+' account does not exist!\n')
    except FileNotFoundError:
        print(colored('\nThe file you are looking for does not exist!\n', 'red', attrs=['bold']))

def listingAccounts():
    files_path = loc()
    try:
        #listing all the accounts in the files
        with open(f'{files_path}/.accman/information.yml', 'r') as d:
            y = yaml.safe_load(d)
        if y == {}:
            print(colored("\nProgram doesn't find any account!\n",'cyan'))
        else:
            accounts = list(y.keys())
            for i in range(len(accounts)):
                print(str(i+1)+': '+ colored(accounts[i], 'cyan'))
    except FileNotFoundError:
        print(colored('\nThe file you are looking for does not exist!\n', 'red', attrs=['bold']))

def deletingAccount():
    #confirming the owner
    globalPass(1)

    files_path = loc()
    try:
        with open(f'{files_path}/.accman/salt.yml', 'r') as saltData:
            d = yaml.safe_load(saltData)
        with open(f'{files_path}/.accman/information.yml', 'r') as data:
            y = yaml.safe_load(data)
            # list all the accounts
            accounts = list(y.keys())
            for i in range(len(accounts)):
                print(str(i+1)+': '+ colored(accounts[i], 'cyan'))
            # delete the account user typed in
            user_input = input('type in the account name you want to delete: ')
            try:
                del d[user_input]
                del y[user_input]
                # update data in the file
                encryptedData = open(f'{files_path}/.accman/information.yml', 'w')
                encryptedData.write(yaml.safe_dump(y,  sort_keys=False))
                encryptedData.close()
                # update data in the salt file
                encryptedData = open(f'{files_path}/.accman/salt.yml', 'w')
                encryptedData.write(yaml.safe_dump(d,  sort_keys=False))
                encryptedData.close()

                print(colored('\nSuccessfully deleted!\n','green',attrs=['bold']))
            except:#KeyError and TypeError
                print('\n     '+colored(user_input,'cyan')+' account/salt does not exist!\n')
            
    except FileNotFoundError:
        print(colored('\nThe account/salt file does not exist!\n', 'red', attrs=['bold']))

def cleaning():
    #confirming the owner
    globalPass(1)

    #warning prompt
    usr_input = input('Are you sure you want to clear all stored data? (yes/no): ')

    if usr_input == 'yes':
        #cleaning info file
        files_path = loc()
        encryptedData = open(f'{files_path}/.accman/information.yml', 'w')
        encryptedData.write(yaml.safe_dump({},  sort_keys=False))
        encryptedData.close()
        #cleaning salt file
        encryptedData = open(f'{files_path}/.accman/salt.yml', 'w')
        encryptedData.write(yaml.safe_dump({},  sort_keys=False))
        encryptedData.close()
    
        print(colored('\nCleaned Successfully!\n','green',attrs=['bold']))
    elif usr_input == 'no':
        print(colored('\nCanceled!\n', 'red', attrs=['bold']))
    else:
        print(colored('\nInvalid input!\n', 'red', attrs=['bold']))

def globalPass(flag=None):
    files_path = loc()
    #terminators call
    if flag == 1:
        try:
            with open(f'{files_path}/.accman/data.yml', 'r') as d:
                y = yaml.safe_load(d)

            #check check
            globalPass = getpass('Please enter global password to proceed: ')
            try:
                with open(f'{files_path}/.accman/data.yml', 'r') as d:
                    y = yaml.safe_load(d)
                    salt = y['GlobalSalt']
                #generate a key
                key = scrypt.hash(globalPass, salt, 2048, 8, 1, 32)
                key = base64.urlsafe_b64encode(key)

                with open(f'{files_path}/.accman/data.yml', 'r') as d:
                    y = yaml.safe_load(d)
                    key2 = y['GlobalPassword']
                    key2 = str(key2).replace('{', '').replace('}', '')
            except TypeError:
                print(colored('\nFirst set up the global password!\n', 'red', attrs=['bold']))
                exit(0)
            #compare the keys
            if str(key) == str(key2):
                return True
            else:
                print(colored('\nInvalid global password!\n', 'red', attrs=['bold']))
                exit(0)
        except FileNotFoundError:
            print(colored('\nFirst set up the global password!\n', 'red', attrs=['bold']))
            exit(0)

    #writers call
    if flag == 0:
        try:
            with open(f'{files_path}/.accman/data.yml', 'r') as d:
                y = yaml.safe_load(d)
                if 'GlobalPassword' in y:
                    return True
        except:#FileNotFoundError and TypeError
            globalPass = getpass('Enter the global password so that no one else can delete or modify your account information: ')
            key = keygen(None, globalPass)
            data = {
            'GlobalPassword':{key}
            }
            # save the key in information file
            encryptedFile = open(f'{files_path}/.accman/data.yml', 'a')
            encryptedFile.write(yaml.safe_dump(data,  sort_keys=False))
            encryptedFile.close()

def byebye():
    print('\n')
    print('     '+colored('Sayounara!','white', attrs=['bold']))
    print(colored('         ♥','red',attrs=['bold']))

if __name__ == '__main__':
    def signal_handler(signal, frame):
        byebye()
        exit(0)

    signal(SIGINT, signal_handler)
    main()

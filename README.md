# accman

<a href="https://github.com/Waqar-Arain/accman"><img src="https://img.shields.io/badge/accman-0.0.1-brightgreen.svg" alt="Version" data-canonical-src="https://img.shields.io/badge/accman-0.0.1-brightgreen.svg?maxAge=259200" style="max-width:100%;"></a>
<a href="https://github.com/Waqar-Arain/accman"><img src="https://img.shields.io/packagist/l/doctrine/orm.svg" alt="Build" data-canonical-src="https://img.shields.io/packagist/l/doctrine/orm.svg" style="max-width:100%;"></a>

## Your own very secure account manager.
It is a python based command line tool for managing your account information. It uses key-definition-function algorithm to encrypt account details which uses a password and a salt to generate a key for encryption/decryption, so no one can decrypt your account information even if they have access to your computer, this tool, or the files where the information is stored.

### Works on:
- Windows
- Linux

### Usage examples:
1. accman help menu: `python accman.py --help`
[![help](/images/img1.png)]()
2. To write account: `python accman.py --write`
[![write](/images/img2.png)]()
3. To read the account details: `python accman.py --read Twitter`
[![read](/images/img3.png)]()
4. Listing all available accounts: `python accman.py --list`
[![list](/images/img4.png)]()
5. To delete an account: `python accman.py --delete`
[![delete](/images/img5.png)]()
6. Clean up all the stored account data: `python accman.py --clean`
[![clean](/images/img6.png)]()
5. Setting up Globall password: `python accman.py --gpass`
[![gpass](/images/img7.png)]()

### Requirements
1. python >= 3.7.4

### Installation
1. To run with python (as used in examples)
```terminal
>git clone https://github.com/Waqar-Arain/accman.git
>cd accman
>pip install -r requirements.txt
>cd accman
>python accman.py
```

2. To use as a command on your system
```terminal
>git clone https://github.com/Waqar-Arain/accman.git
>cd accman
>pip install -e .
```

### Bugs? Information?
Notify me 
- Twitter: @_waqarArain
from setuptools import setup, find_packages

setup(
   name='accman',
   version='0.0.1',
   description='Your own very secure account manager.',
   author='Waqar-Arain',
   author_email='adil.cn85@gmail.com',
   url='https://github.com/Waqar-Arain/accman',
   packages=find_packages(include=['accman', 'accman.*']), # its the folder or package which contains __init__ file.

   classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
   python_requires='>=3.7.4',
   install_requires=[
   			'cryptography>=2.8',
   			'scrypt>=0.8.13',
   			'termcolor>=1.1.0',
   			'colorama>=0.4.3',
   			'pyYAML>=5.3.1',
        'pyperclip>=1.8.0'
   	],
   entry_points={
        "console_scripts": [
            "accman=accman.accman:main",
        ]
    }
)
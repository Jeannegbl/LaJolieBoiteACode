import os
from dotenv import load_dotenv

load_dotenv('.env')

hello = os.environ.get('password')

hey = os.getenv('username')
print(hey)
print(hello)
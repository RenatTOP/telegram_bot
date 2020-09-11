from dotenv import load_dotenv
load_dotenv()
import os

config = {'token': os.environ['TOKEN']}

tables_names = {'USERS_TABLE': 'users_renat',
                'PRODUCTS_TABLE': 'products_renat'}

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = os.environ['SECRET_KEY']

PAYMENT_TOKEN = os.environ['PAYMENT_TOKEN']


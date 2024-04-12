import os


TOKEN = '6899962628:AAFyonrDwTtJKH1i8HxgmBTEpsROKUyLz0I'
NAME_DB = 'R_443Y_shop.db'
VERSION = '0.0.1'
AUTHOR = 'R-443Y_company'


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(f'sqlite+aiosqlite:///{BASE_DIR}/data_base/', NAME_DB)
ECHO = False


if __name__ == "__main__":
    print(BASE_DIR)
    print(DATABASE)

#Любую настройку переопределяем тут и добавляем в файл в gitignore
from pathlib import Path
from .settings import BASE_DIR
import os
from dotenv import load_dotenv
load_dotenv(override=True)

SECRET_KEY = os.environ.get('SECRETKEY')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


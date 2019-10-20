# -*- coding:utf-8 -*-

import os
from os.path import join, dirname
from dotenv import load_dotenv


env_path = join(dirname(__file__), '.env')
load_dotenv(env_path)

DB_ROOT_PASSWORD = os.environ.get("MYSQL_ROOT_PASSWORD")
DB_PASSWORD = os.environ.get("MYSQL_PASSWORD")

ROOT_DIR = "./"
IMAGE_DIR = "./static/img"

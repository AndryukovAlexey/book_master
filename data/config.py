from environs import Env
import logging

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN") 
ADMINS = env.list("ADMINS") 
IP = env.str("ip") 

PGUSER = env.str("PGUSER")
PGPASSWORD = env.str("PGPASSWORD")
DATABASE_NAME = env.str("DATABASE_NAME")
DBHOST = env.str("DBHOST")
POSTGRES_URI = f"postgresql://{PGUSER}:{PGPASSWORD}@{DBHOST}/{DATABASE_NAME}"
PROVIDER_TOKEN = env.str("PROVIDER_TOKEN")



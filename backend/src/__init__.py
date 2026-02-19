from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")
load_dotenv(dotenv_path=".env.local", override=True)
load_dotenv(dotenv_path=".env.development", override=True)

import os
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://supabase.moldus.ru")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")  # Лучше хранить в .env


def get_supabase() -> Client:
    print("SUPABASE_URL:", SUPABASE_URL, "SUPABASE_KEY:", SUPABASE_KEY)

    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("Supabase URL or KEY not set")
    return create_client(SUPABASE_URL, SUPABASE_KEY) 
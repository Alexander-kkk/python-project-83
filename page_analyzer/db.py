import os
import psycopg2
from psycopg2.extras import DictCursor
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn


def normalize_url(url):
    parsed = urlparse(url)
    normalize_url = f"{parsed.scheme}://{parsed.netloc}"
    if normalize_url.endswith("/"):
        normalize_url = normalize_url[:-1]
        return normalize_url
    else:
        return normalize_url


def add_url(url):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("INSERT INTO urls (name) VALUES (%s) RETURNING id", (url,))
                url_id = cur.fetchone()[0]
                conn.commit()
                return url_id, True
            except psycopg2.IntegrityError:
                conn.rollback()
                cur.execute("Select id from urls where name = %s", (url,))
                result = cur.fetchone()[0]
                return result, False if result else None


def get_url_by_id(url_id):
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM urls WHERE id = %s", (url_id,))
            result = cur.fetchone()
            return result


def get_all_urls():
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM urls")
            result = cur.fetchall()
            return result


def add_url_check(url_id):
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            try:
                cur.execute(
                    "INSERT INTO url_checks (url_id) VALUES (%s) RETURNING id, created_at",
                    (url_id,),
                )
                result = cur.fetchone()
                conn.commit()
                return result
            except Exception as e:
                conn.rollback()
                raise e


def get_url_checks(url_id):
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(
                "SELECT * FROM url_checks WHERE url_id = %s ORDER BY created_at DESC",
                (url_id,),
            )
            result = cur.fetchall()
            return result

"""Load scraped markdown documents from knowledge/raw/ into Snowflake raw.scraped_documents."""

import os
import yaml
import snowflake.connector
from cryptography.hazmat.primitives import serialization


def load_private_key():
    """Load RSA private key from file or env var."""
    key_path = os.environ.get("SNOWFLAKE_PRIVATE_KEY_PATH", "snowflake_key.p8")
    if os.path.exists(key_path):
        with open(key_path, "rb") as f:
            private_key = serialization.load_pem_private_key(f.read(), password=None)
        return private_key.private_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
    key_data = os.environ.get("SNOWFLAKE_PRIVATE_KEY")
    if key_data:
        private_key = serialization.load_pem_private_key(key_data.encode(), password=None)
        return private_key.private_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
    raise ValueError("No Snowflake private key found (file or env var)")


def get_snowflake_connection():
    return snowflake.connector.connect(
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        user=os.environ["SNOWFLAKE_USER"],
        private_key=load_private_key(),
        database=os.environ.get("SNOWFLAKE_DATABASE", "NHL_ANALYTICS"),
        warehouse=os.environ["SNOWFLAKE_WAREHOUSE"],
        schema="RAW",
    )


def load_url_mapping(config_path="extract/scrape_urls.yaml"):
    """Load filename-to-URL mapping from scrape config."""
    with open(config_path, "r") as f:
        entries = yaml.safe_load(f)
    return {entry["filename"]: entry["url"] for entry in entries}


def main():
    raw_dir = "knowledge/raw"
    url_map = load_url_mapping()
    conn = get_snowflake_connection()
    cur = conn.cursor()

    loaded = 0
    for filename in os.listdir(raw_dir):
        if not filename.endswith(".md") or filename == ".gitkeep":
            continue
        filepath = os.path.join(raw_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        url = url_map.get(filename, "")

        cur.execute("""
            MERGE INTO scraped_documents t
            USING (SELECT %(filename)s AS filename) s ON t.filename = s.filename
            WHEN MATCHED THEN UPDATE SET
                url = %(url)s,
                content = %(content)s,
                _loaded_at = CURRENT_TIMESTAMP()
            WHEN NOT MATCHED THEN INSERT (filename, url, content)
                VALUES (%(filename)s, %(url)s, %(content)s)
        """, {
            "filename": filename,
            "url": url,
            "content": content,
        })
        loaded += 1

    print(f"Loaded {loaded} documents to Snowflake raw.scraped_documents")
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()

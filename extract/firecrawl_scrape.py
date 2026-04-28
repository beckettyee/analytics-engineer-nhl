"""Scrape URLs via Firecrawl API and save markdown to knowledge/raw/."""

import os
import yaml
from firecrawl import V1FirecrawlApp


def load_urls(config_path="extract/scrape_urls.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def scrape_url(app, url):
    """Scrape a single URL and return markdown content."""
    result = app.scrape_url(url, formats=["markdown"])
    return result.markdown or ""


def save_markdown(filename, content, output_dir="knowledge/raw"):
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return filepath


def main():
    api_key = os.environ["FIRECRAWL_API_KEY"]
    app = V1FirecrawlApp(api_key=api_key)

    urls = load_urls()
    scraped = 0
    skipped = 0
    failed = 0

    for entry in urls:
        url = entry["url"]
        filename = entry["filename"]
        filepath = os.path.join("knowledge/raw", filename)

        if os.path.exists(filepath):
            print(f"SKIP (exists): {filename}")
            skipped += 1
            continue

        try:
            print(f"Scraping: {url}")
            content = scrape_url(app, url)
            if content:
                save_markdown(filename, content)
                print(f"  Saved: {filename}")
                scraped += 1
            else:
                print(f"  EMPTY: {url} returned no content")
                failed += 1
        except Exception as e:
            print(f"  FAIL: {url} — {e}")
            failed += 1

    print(f"\nDone: {scraped} scraped, {skipped} skipped, {failed} failed")


if __name__ == "__main__":
    main()

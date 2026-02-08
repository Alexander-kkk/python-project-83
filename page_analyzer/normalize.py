from urllib.parse import urlparse


def normalize_url(url):
    parsed = urlparse(url)
    normalize_url = f"{parsed.scheme}://{parsed.netloc}"
    if normalize_url.endswith("/"):
        normalize_url = normalize_url[:-1]
        return normalize_url
    else:
        return normalize_url
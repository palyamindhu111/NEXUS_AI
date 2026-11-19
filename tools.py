
from ddgs import DDGS
from langchain_core.tools import tool
from urllib.parse import urlparse
import requests


# Selected domains to prioritize in search results
TRUSTED_DOMAINS = [
    "python.org",
    "docs.python.org",
    "developer.mozilla.org",
    "w3.org",
    "nist.gov",
    "nasa.gov",
    "who.int",
    "un.org",
    "europa.eu",
    "gov.in",
    "ac.in",
    "edu"
]


def is_trusted_source(url):
    """Classify selected domains using an allowlist."""

    try:
        hostname = urlparse(url).hostname

        if not hostname:
            return False

        hostname = hostname.lower().rstrip(".")

        return any(
            hostname == domain or hostname.endswith("." + domain)
            for domain in TRUSTED_DOMAINS
        )

    except Exception:
        return False


# WEB SEARCH TOOL
@tool
def search_web(query: str) -> str:
    """Search the web and prioritize selected domains."""

    try:
        with DDGS() as ddgs:
            results = list(
                ddgs.text(query, max_results=10)
            )

        if not results:
            return "Search unavailable: No results found."

        results.sort(
            key=lambda item: is_trusted_source(
                item.get("href", "")
            ),
            reverse=True
        )

        output = []

        for item in results[:8]:

            url = item.get("href", "")

            if not url:
                continue

            category = (
                "PRIORITIZED DOMAIN"
                if is_trusted_source(url)
                else "OTHER SOURCE"
            )

            output.append(
                f"""
Title: {item.get('title', 'No title')}
Link: {url}
Source Category: {category}
Information: {item.get('body', 'No description')}
"""
            )

        if not output:
            return "Search unavailable: No usable links."

        return "\n".join(output)

    except Exception as e:
        return f"Search unavailable: {str(e)}"


# URL ACCESSIBILITY CHECK
def verify_source_url(url):
    """Check whether a source URL responds."""

    try:
        parsed = urlparse(url)

        if (
            parsed.scheme not in ("http", "https")
            or not parsed.hostname
        ):
            return {
                "status": "Invalid URL",
                "http_status": None,
                "final_url": url
            }

        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; NEXUSAI/1.0)"
        }

        response = requests.get(
            url,
            timeout=10,
            allow_redirects=True,
            headers=headers,
            stream=True
        )

        status_code = response.status_code
        final_url = response.url
        response.close()

        if status_code < 400:
            message = f"Reachable | HTTP Status: {status_code}"
        else:
            message = f"HTTP error: {status_code}"

        return {
            "status": message,
            "http_status": status_code,
            "final_url": final_url
        }

    except requests.Timeout:
        return {
            "status": "Check timed out",
            "http_status": None,
            "final_url": url
        }

    except requests.ConnectionError:
        return {
            "status": "Connection failed",
            "http_status": None,
            "final_url": url
        }

    except requests.RequestException as e:
        return {
            "status": f"Request failed: {str(e)}",
            "http_status": None,
            "final_url": url
        }

    except Exception as e:
        return {
            "status": f"Unexpected error: {str(e)}",
            "http_status": None,
            "final_url": url
        }


# SOURCE VERIFICATION TOOL
@tool
def check_source(url: str) -> str:
    """Check URL accessibility and classify its domain."""

    category = (
        "Prioritized domain"
        if is_trusted_source(url)
        else "Other domain"
    )

    result = verify_source_url(url)

    return f"""
Source: {url}
Domain Category: {category}
URL Status: {result['status']}
Final URL: {result['final_url']}
HTTP Status: {result['http_status']}
"""


# TEST FUNCTION
if __name__ == "__main__":

    test_url = "https://www.python.org/"

    print("NEXUS AI SOURCE VERIFICATION TEST")
    print("---------------------------------")

    print(check_source.invoke({
        "url": test_url
    }))

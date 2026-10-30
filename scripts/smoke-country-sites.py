#!/usr/bin/env python3
"""Read-only production HTTP/HTTPS smoke checks for country corporate sites."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import sys
import time
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "countries.json"
REPORT = ROOT / "artifacts" / "country-production-smoke.json"


class Structure(HTMLParser):
    """Extract relevant signals without executing scripts or modifying sites."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lang = ""
        self.canonical = ""
        self.has_main = False
        self.has_header = False
        self.in_header = False
        self.in_small = False
        self.small_text = ""
        self.header_labels = []

    def handle_starttag(self, tag, attrs):
        fields = dict(attrs)
        if tag == "html":
            self.lang = fields.get("lang", "")
        elif tag == "main":
            self.has_main = True
        elif tag == "header":
            self.has_header = self.in_header = True
        elif tag == "small" and self.in_header:
            self.in_small = True
            self.small_text = ""
        elif tag == "link" and "canonical" in fields.get("rel", "").split():
            self.canonical = fields.get("href", "")

    def handle_data(self, data):
        if self.in_small:
            self.small_text += data

    def handle_endtag(self, tag):
        if tag == "small" and self.in_small:
            self.header_labels.append(self.small_text.strip())
            self.in_small = False
        elif tag == "header":
            self.in_header = False


def normalized(value):
    """Canonical comparison tolerates only an equivalent trailing slash."""
    return value.rstrip("/") + "/"


def get_html(url):
    """Request public markup with default certificate verification, no credentials."""
    last_error = None
    for attempt in range(2):
        try:
            req = Request(
                url,
                headers={
                    "User-Agent": "SkunkworksCountrySmoke/1.0 (+https://github.com/skunkworks-africa/theme)",
                    "Accept": "text/html",
                    "Cache-Control": "no-cache",
                },
                method="GET",
            )
            with urlopen(req, timeout=18) as resp:
                final_url = resp.geturl()
                if urlparse(final_url).scheme != "https":
                    raise ValueError("Insecure HTTP redirect")
                if resp.status != 200:
                    raise ValueError(f"HTTP {resp.status}")
                content_type = resp.headers.get("Content-Type", "")
                if "text/html" not in content_type:
                    raise ValueError(f"Not an HTML response: {content_type}")
                body = resp.read(1_048_577)
                if len(body) > 1_048_576:
                    raise ValueError("HTML response exceeds 1 MiB")
                return body.decode("utf-8", errors="replace"), final_url
        except Exception as exc:
            last_error = str(exc)
            if attempt == 0:
                time.sleep(2)
    raise RuntimeError(last_error or "No response")


def validate_registry(data):
    """Schema checks run offline on PRs and cannot be bypassed by a network failure."""
    errors = []
    countries = data.get("countries", [])
    if data.get("authority") != "skunkworks-africa/theme":
        errors.append("Invalid authority")
    if len(countries) < 8:
        errors.append("Missing country websites")
    owners = set()
    for item in countries:
        owner = item.get("owner", "")
        url = item.get("canonical", "")
        if not owner or owner in owners:
            errors.append(f"Duplicate or missing owner: {owner}")
        owners.add(owner)
        if item.get("repository") != f"{owner}/www":
            errors.append(f"Invalid repository for {owner}")
        if urlparse(url).scheme != "https" or not urlparse(url).hostname:
            errors.append(f"Invalid HTTPS canonical for {owner}")
        if not item.get("headerLabel") or not item.get("locale"):
            errors.append(f"Missing country identity for {owner}")
    return errors


def check_country(item):
    """Check one country plus its explicit secondary-language page if applicable."""
    result = {
        "country": item["country"],
        "url": item["canonical"],
        "status": "fail",
        "checks": [],
        "errors": [],
    }
    try:
        body, final = get_html(item["canonical"])
        p = Structure()
        p.feed(body)
        if not p.has_header or not p.has_main:
            result["errors"].append("Header or main landmark missing")
        if p.lang != item["locale"]:
            result["errors"].append(f"Language mismatch: {p.lang or 'missing'}")
        if normalized(p.canonical) != normalized(item["canonical"]):
            result["errors"].append(f"Canonical mismatch: {p.canonical or 'missing'}")
        if item["headerLabel"] not in p.header_labels:
            result["errors"].append(f"Wrong country header: {p.header_labels}")
        result["checks"].append("HTTPS HTML and country identity")
        css_url = urljoin(final, "styles.css")
        try:
            req = Request(css_url, headers={"User-Agent": "SkunkworksCountrySmoke/1.0"})
            with urlopen(req, timeout=14) as resp:
                sample = resp.read(100_000).decode("utf-8", errors="replace")
                if resp.status != 200 or "{" not in sample:
                    result["errors"].append("Global styles.css unavailable or invalid")
                else:
                    result["checks"].append("Core CSS served")
        except Exception as exc:
            result["errors"].append(f"Core stylesheet failed: {exc}")
        if "fr-CM" in item.get("additionalLocales", []):
            try:
                french, _ = get_html(urljoin(item["canonical"], "fr/"))
                fp = Structure()
                fp.feed(french)
                if fp.lang != "fr-CM" or not fp.has_main:
                    result["errors"].append("Cameroon French page is not valid fr-CM HTML")
                else:
                    result["checks"].append("French-language edition")
            except Exception as exc:
                result["errors"].append(f"French-language edition failed: {exc}")
    except Exception as exc:
        result["errors"].append(f"Landing page unreachable: {exc}")
    result["status"] = "pass" if not result["errors"] else "fail"
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    errors = validate_registry(data)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    if args.validate_only:
        print(f"Country inventory structurally valid: {len(data['countries'])}")
        return 0
    with ThreadPoolExecutor(max_workers=5) as pool:
        results = list(pool.map(check_country, data["countries"]))
    payload = {
        "observed_at": datetime.now(timezone.utc).isoformat(),
        "method": "External HTTP read-only check from GitHub-hosted runner",
        "countries": results,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    summary = [
        "# Country production smoke results",
        "",
        "Successful CI/CD deploys are distinct from actual external HTTPS response checks.",
        "",
        "| Country | HTTPS, canonical, country branding, core CSS |",
        "|---|---|",
    ]
    for item in results:
        summary.append(
            f"| [{item['country']}]({item['url']}) | "
            + ("PASS" if item["status"] == "pass" else "FAIL: " + "; ".join(item["errors"]).replace("|", "/"))
            + " |"
        )
    text = "\n".join(summary) + "\n"
    print(text)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as output:
            output.write(text)
    return 1 if any(x["status"] != "pass" for x in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())

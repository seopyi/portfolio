"""Check local references and parse inline JS without executing page code."""
from html.parser import HTMLParser
from pathlib import Path
import subprocess
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.references = []
        self.scripts = []
        self.script = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for key in ("href", "src"):
            if attrs.get(key):
                self.references.append(attrs[key])
        if tag == "script":
            kind = attrs.get("type", "")
            if not attrs.get("src") and kind in ("", "text/javascript", "module"):
                self.script = ("module" if kind == "module" else "commonjs", [])

    def handle_data(self, data):
        if self.script is not None:
            self.script[1].append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self.script is not None:
            self.scripts.append((self.script[0], "".join(self.script[1])))
            self.script = None


def main():
    failures = []
    pages = sorted(ROOT.glob("*.html"))
    if not pages:
        raise SystemExit("No HTML documents found")
    for file in pages:
        page = Page()
        page.feed(file.read_text(encoding="utf-8"))
        for reference in page.references:
            url = urlsplit(reference)
            if url.scheme or url.netloc or not url.path:
                continue
            target = ROOT / unquote(url.path.lstrip("/"))
            if not target.is_file():
                failures.append(f"{file.name}: missing {url.path}")
        for index, (kind, script) in enumerate(page.scripts):
            result = subprocess.run(["node", "--check", f"--input-type={kind}"], input=script, text=True, capture_output=True, encoding="utf-8")
            if result.returncode:
                failures.append(f"{file.name}: script {index + 1}\n{result.stderr}")
        print(f"Checked {file.name}: local references and {len(page.scripts)} scripts")
    if failures:
        raise SystemExit("\n".join(failures))


if __name__ == "__main__":
    main()

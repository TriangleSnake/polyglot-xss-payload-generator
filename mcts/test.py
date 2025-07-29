import os
import zipfile
from pathlib import Path

# Directory to store individual HTML files
base_dir = Path("./localtest")
base_dir.mkdir(exist_ok=True)

# List of templates (each with {payload} placeholder)
templates = [
    # 1  CSS comment
    "<!DOCTYPE html><html><head><meta charset=\"utf-8\"><style>/* {payload} */</style></head><body>CSS-comment sink</body></html>",
    # 2  Title
    "<!DOCTYPE html><html><head><meta charset=\"utf-8\"><title>{payload}</title></head><body>Title sink</body></html>",
    # 3  Attr double quoted
    "<!DOCTYPE html><html><head><meta charset=\"utf-8\"></head><body><div id=\"box\" data-dq=\"{payload}\">Double-quoted attr sink</div></body></html>",
    # 4  Attr single quoted
    "<!DOCTYPE html><html><head><meta charset=\"utf-8\"></head><body><div id=\"box\" data-sq='{payload}'>Single-quoted attr sink</div></body></html>",
    # 5  Body onload
    "<!DOCTYPE html><html><head><meta charset=\"utf-8\"></head><body onload=\"{payload}\">Body onload sink</body></html>",
    # 6  innerHTML
    "<!DOCTYPE html><html><head><meta charset=\"utf-8\"></head><body><div id=\"target\">{payload}</div></body></html>",
    # 7  href attribute
    "<!DOCTYPE html><html><head><meta charset=\"utf-8\"></head><body><a href=\"{payload}\">Href sink</a></body></html>",
    # 8  HTML comment
    "<!DOCTYPE html><html><head><meta charset=\"utf-8\"></head><body><!-- {payload} -->Comment sink</body></html>",
    # 9  JS unquoted assignment
    "<!DOCTYPE html><html><head><meta charset=\"utf-8\"></head><body><script>var foo = {payload};</script>Unquoted JS assignment sink</body></html>",
    # 10 JS eval
    "<!DOCTYPE html><html><head><meta charset=\"utf-8\"></head><body><script>eval({payload});</script>JS eval sink</body></html>",
    # 11 JS double quoted string
    "<!DOCTYPE html><html><head><meta charset=\"utf-8\"></head><body><script>var bar = \"{payload}\";</script>Double-quoted JS string sink</body></html>",
    # 12 JS single quoted string
    "<!DOCTYPE html><html><head><meta charset=\"utf-8\"></head><body><script>var baz = '{payload}';</script>Single-quoted JS string sink</body></html>",
    # 13 JS slash quoted string
    "<!DOCTYPE html><html><head><meta charset=\"utf-8\"></head><body><script>var qux = \\\\{payload}\\\\;</script>Slash-quoted JS string sink</body></html>",
    # 14 JS comment
    "<!DOCTYPE html><html><head><meta charset=\"utf-8\"></head><body><script>/* {payload} */</script>JS comment sink</body></html>",
]

for i in range(1, len(templates) + 1):
    template = templates[i - 1]
    # Create a unique filename for each template
    filename = base_dir / f"template_{i}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(template)

    
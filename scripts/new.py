import re
from datetime import datetime
from pathlib import Path
from sys import argv

title = " ".join(argv[1:])

content = f'''
---
title = "{title}"
created_at = "{datetime.now().strftime("%d %B %Y")}"
preview = """

"""
---
'''.strip()

slug = re.sub(r"[^a-z0-9]+", "-", title.lower().replace("'", "")).strip("-")

path = Path("posts") / f"{slug}.md"
_ = path.write_text(content)
print(path)

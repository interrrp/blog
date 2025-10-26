# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "mistletoe",
# ]
# ///

from dataclasses import asdict, dataclass
from pathlib import Path
from shutil import copytree, rmtree
from string import Template
from typing import cast

import mistletoe
import tomllib

TEMPLATES_DIR = Path("templates")
POSTS_DIR = Path("posts")
STATIC_DIR = Path("static")
BUILD_DIR = Path("build")

BUILD_DIR.mkdir(exist_ok=True)

for item in BUILD_DIR.iterdir():
    if item.is_dir():
        rmtree(item)
    else:
        item.unlink()


def build(filename: str, content: str) -> None:
    path = BUILD_DIR / filename
    print(path)
    _ = path.write_text(content)


_ = copytree(STATIC_DIR, BUILD_DIR / "static", dirs_exist_ok=True)
print("static")


@dataclass(frozen=True)
class Post:
    slug: str
    title: str
    created_at: str
    preview: str
    html: str


posts = set[Post]()

for post_file in POSTS_DIR.glob("*.md"):
    slug = post_file.stem
    _, frontmatter, markdown, *_ = post_file.read_text().split("+++")

    frontmatter = cast("dict[str, str]", tomllib.loads(frontmatter))

    html = mistletoe.markdown(markdown)

    post = Post(
        slug,
        frontmatter["title"],
        frontmatter["created_at"],
        frontmatter["preview"],
        html,
    )
    posts.add(post)


def read_template(name: str) -> Template:
    path = TEMPLATES_DIR / f"{name}.html"
    return Template(path.read_text())


index_template = read_template("index")
post_entry_template = read_template("post-entry")
post_template = read_template("post")

entries = ""
for post in posts:
    entries += post_entry_template.substitute(asdict(post))

index_html = index_template.substitute(entries=entries)
build("index.html", index_html)

for post in posts:
    html = post_template.substitute(asdict(post))
    build(f"{post.slug}.html", html)

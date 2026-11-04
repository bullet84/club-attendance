"""Render the existing Markdown journal as a small static GitHub Pages site."""

from html import escape
import json
from pathlib import Path
import re
import shutil
from string import Template

import markdown
from markdown.extensions.toc import slugify_unicode

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SITE = ROOT / "site"
OUTPUT = ROOT / "_site"


def template(name, **values):
    return Template((SITE / "templates" / name).read_text(encoding="utf-8")).substitute(values)


def render():
    config = json.loads((SITE / "config.json").read_text(encoding="utf-8"))
    posts = config["posts"]
    published = [post for post in posts if (DOCS / post["source"]).is_file()]
    if not published:
        raise ValueError("At least one published Markdown article is required.")
    OUTPUT.mkdir(exist_ok=True)
    shutil.copytree(DOCS / "assets", OUTPUT / "assets", dirs_exist_ok=True)
    shutil.copytree(SITE / "assets", OUTPUT / "assets", dirs_exist_ok=True)

    def page(filename, content, title, description, body_class="home", og_type="website"):
        canonical = config["url"].rstrip("/") + "/" + ("" if filename == "index.html" else filename)
        html = template(
            "base.html", content=content, page_title=escape(title), description=escape(description),
            canonical=escape(canonical), body_class=body_class, og_type=og_type,
            author=escape(config["author"]), repository=escape(config["repository"]),
        )
        (OUTPUT / filename).write_text(html, encoding="utf-8")

    rows = []
    for number, post in enumerate(posts, 1):
        source = DOCS / post["source"]
        filename = Path(post["source"]).with_suffix(".html").name
        exists = source.is_file()
        tag = "a" if exists else "div"
        href = f' href="{escape(filename)}"' if exists else ""
        badge = '<span class="published">공개</span>' if exists else '<span class="planned">작성 예정</span>'
        date = escape(post["date"] or "") if exists else ""
        arrow = '<span class="post-arrow" aria-hidden="true">↗</span>' if exists else ""
        rows.append(
            f'<{tag} class="post-row {"published-post" if exists else "upcoming"}"{href}>'
            f'<span class="post-number">{number:02}</span><div>'
            f'<span class="post-category">{escape(post["category"])}</span>'
            f'<h3>{escape(post["title"])}</h3><p>{escape(post["summary"])}</p></div>'
            f'<div class="post-meta">{badge}<span>{date}</span>{arrow}</div></{tag}>'
        )
        if not exists:
            continue
        text = source.read_text(encoding="utf-8-sig")
        text = re.sub(r"\A# [^\n]+\n", "", text, count=1)
        # Keep Markdown navigation useful both on GitHub and on the published site.
        text = text.replace("](index.md)", "](./#journal)")
        text = text.replace("](../README.md)", f']({config["repository"]})')
        text = re.sub(r'\]\((\d{2}-[^)#]+)\.md(#[^)]*)?\)', r'](\1.html\2)', text)
        converter = markdown.Markdown(
            extensions=["extra", "toc", "sane_lists"],
            extension_configs={"toc": {"slugify": slugify_unicode, "toc_depth": "2-3"}},
        )
        body = converter.convert(text)
        body = body.replace("<table>", '<div class="table-scroll" role="region" aria-label="표: 가로로 스크롤할 수 있습니다" tabindex="0"><table>')
        body = body.replace("</table>", "</table></div>")
        body = re.sub(r'<li>\[ \] ', '<li class="task-item"><span class="task-box" aria-label="예정">☐</span> ', body)
        body = re.sub(r'<li>\[[xX]\] ', '<li class="task-item"><span class="task-box" aria-label="완료">☑</span> ', body)
        content = template(
            "article.html", article_title=escape(post["title"]), summary=escape(post["summary"]),
            post_number=f"{number:02}", author=escape(config["author"]), date=escape(post["date"] or ""),
            category=escape(post["category"]), toc=converter.toc, article_content=body,
            source_url=escape(config["repository"] + "/blob/main/docs/" + post["source"]),
        )
        page(filename, content, post["title"] + " | " + config["title"], post["summary"], "article", "article")

    home = template(
        "home.html", post_list="\n".join(rows), repository=escape(config["repository"]),
        first_post=escape(Path(published[0]["source"]).with_suffix(".html").name),
        published_count=str(len(published)),
    )
    page("index.html", home, config["title"] + " | 활동 신청·출석 서비스 개발 기록", config["description"])
    (OUTPUT / ".nojekyll").touch()
    print(f"Built {len(published)} article(s) and homepage in {OUTPUT}")


if __name__ == "__main__":
    render()

from flask import Flask, render_template, abort
import os
import markdown
import json

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html", title="Home")


@app.route("/about")
def about():
    return render_template("about.html", title="About Us")


@app.route("/articles")
def article_list():
    articles = []

    for filename in os.listdir("articles"):
        if filename.endswith(".md"):
            slug = filename[:-3]
            meta_path = os.path.join("articles", f"{slug}.json")
            meta = {
                "title": slug.replace("-", " ").title(),
                "author": "Unknown",
                "date": "N/A",
                "description": "",
            }
            if os.path.exists(meta_path):
                with open(meta_path, "r", encoding="utf-8") as f:
                    meta.update(json.load(f))
            articles.append({"slug": slug, **meta})

    # Sort by date if available
    articles.sort(key=lambda x: x.get("date", ""), reverse=True)

    return render_template("articles.html", title="Articles", articles=articles)


@app.route("/articles/<slug>")
def article(slug):
    filepath = os.path.join("articles", f"{slug}.md")
    meta_path = os.path.join("articles", f"{slug}.json")

    if not os.path.exists(filepath):
        abort(404)

    with open(filepath, "r", encoding="utf-8") as f:
        content = markdown.markdown(f.read())

    meta = {"title": slug.replace("-", " ").title(), "author": "Unknown", "date": "N/A"}
    if os.path.exists(meta_path):
        with open(meta_path, "r", encoding="utf-8") as f:
            meta.update(json.load(f))

    return render_template(
        "article.html", title=meta["title"], content=content, meta=meta
    )


if __name__ == "__main__":
    app.run(debug=True)

import os
from flask import (
    Flask,
    render_template,
    request,
    flash,
    redirect,
    url_for,
)
from dotenv import load_dotenv
from page_analyzer import db, normalize, parser
import validators
import requests

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["DATABASE_URL"] = os.getenv("DATABASE_URL")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/urls")
def urls_get():
    urls_list = db.get_all_urls()
    urls_sorted = sorted(urls_list, key=lambda x: x["id"], reverse=True)
    return render_template("urls.html", urls=urls_sorted, checks=urls_checks)


@app.post("/urls")
def urls_post():
    url_input = request.form.get("url", "").strip()

    if not url_input:
        flash("Заполните это поле", "danger")
        return render_template("index.html", url=url_input), 422

    if not validators.url(url_input) or len(url_input) > 255:
        flash("Некорректный URL", "danger")
        return render_template("index.html", url=url_input), 422

    normalized_url = normalize.normalize_url(url_input)
    url_id, is_new = db.add_url(normalized_url)

    if is_new:
        flash("Страница успешно добавлена", "success")
    else:
        flash("Страница уже существует", "info")
    return redirect(url_for("urls_show", id=url_id))


@app.route("/urls/<int:id>")
def urls_show(id):
    url = db.get_url_by_id(id)
    checks = db.get_url_checks(id)
    return render_template("show.html", url=url, checks=checks)


@app.post("/urls/<int:id>/checks")
def urls_checks(id):
    try:
        url = db.get_url_by_id(id)["name"]
        parsed_data = parser.parse_html(url)
        db.add_url_check(
            id,
            status_code=parsed_data['status_code'],
            h1=parsed_data['h1'],
            title=parsed_data['title'],
            description=parsed_data['description'],
        )
        flash("Страница успешно проверена", "success")
    except requests.RequestException:
        flash("Произошла ошибка при проверке", "danger")
    return redirect(url_for("urls_show", id=id))

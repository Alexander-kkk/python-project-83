import os
from flask import (
    Flask,
    render_template,
    request,
    flash,
    redirect,
    url_for,
    get_flashed_messages,
)
from dotenv import load_dotenv
from page_analyzer import db
import validators

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
    return render_template("urls.html", urls=urls_sorted)


@app.post("/urls")
def urls_post():
    messages = get_flashed_messages(with_categories=True)
    url_input = request.form.get("url", "").strip()

    if not url_input:
        flash("Заполните это поле", "error")
        return render_template("index.html", url=url_input, messages=messages)

    if not validators.url(url_input) or len(url_input) > 255:
        flash("Некорректный URL", "error")
        return render_template("index.html", url=url_input, messages=messages)

    normalize_url = db.normalize_url(url_input)
    url_id, is_new = db.add_url(normalize_url)

    if is_new:
        flash("Страница успешно добавлена", "success")
    else:
        flash("Страница уже существует", "info")
    return redirect(url_for("urls_show", id=url_id, messages=messages))


@app.route("/urls/<int:id>")
def urls_show(id):
    url = db.get_url_by_id(id)
    checks = db.get_url_checks(id)
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        "show.html", url=url, messages=messages, checks=checks
        )


@app.post("/urls/<int:id>/checks")
def urls_checks(id):
    try:
        db.add_url_check(id)
        flash("Страница успешно проверена", "success")
    except Exception as e:
        flash(f"Ошибка при проверке: {str(e)}", "danger")
    return redirect(url_for("urls_show", id=id))

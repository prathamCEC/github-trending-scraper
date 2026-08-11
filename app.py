from flask import Flask, render_template
import psycopg2

app = Flask(__name__)


def get_repositories():

    connection = psycopg2.connect(
        host="psql-db",
        database="github_trending",
        user="postgres",
        password="123456"
    )

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            username,
            repository,
            language,
            stars,
            stars_today,
            url,
            description
        FROM repositories
        ORDER BY stars_today DESC
    """)

    repositories = cursor.fetchall()

    cursor.close()
    connection.close()

    return repositories


@app.route("/")
def home():

    repositories = get_repositories()

    return render_template(
        "index.html",
        repositories=repositories
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )

import requests
import re
import psycopg2
from bs4 import BeautifulSoup


URL = "https://github.com/trending"

headers = {
    "User-Agent": "Mozilla/5.0"
}


# ---------- FETCH GITHUB ----------

response = requests.get(URL, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

repositories = []


# ---------- SCRAPE DATA ----------

for rank, repo in enumerate(soup.select("article.Box-row"), 1):

    link = repo.select_one("h2 a")

    if not link:
        continue

    name = link.get_text(" ", strip=True)
    url = "https://github.com" + link["href"]

    description_tag = repo.select_one("p")

    description = (
        description_tag.get_text(" ", strip=True)
        if description_tag
        else "No description"
    )

    language_tag = repo.select_one(
        '[itemprop="programmingLanguage"]'
    )

    language = (
        language_tag.get_text(strip=True)
        if language_tag
        else "Unknown"
    )

    stars_tag = repo.select_one(
        'a[href$="/stargazers"]'
    )

    stars = (
        stars_tag.get_text(strip=True)
        if stars_tag
        else "0"
    )

    today = re.search(
        r"([\d,]+)\s+stars today",
        repo.get_text(" ", strip=True)
    )

    stars_today = today.group(1) if today else "0"

    repositories.append({
        "rank": rank,
        "repository": name,
        "language": language,
        "stars": stars,
        "stars_today": stars_today,
        "url": url,
        "description": description
    })


# ============================================================
# CLI REPORT
# ============================================================

print("\n" + "=" * 70)
print("              GITHUB TRENDING REPORT")
print("=" * 70)

print(f"\nRepositories found: {len(repositories)}\n")

for repo in repositories:

    print(f"#{repo['rank']}  {repo['repository']}")
    print(f"    Language    : {repo['language']}")
    print(f"    Total Stars : {repo['stars']}")
    print(f"    Today       : +{repo['stars_today']}")
    print(f"    URL         : {repo['url']}")
    print(f"    About       : {repo['description'][:100]}")
    print("-" * 70)


# ============================================================
# POSTGRESQL CONNECTION
# ============================================================

connection = psycopg2.connect(
    host="psql-db",
    database="github_trending",
    user="postgres",
    password="123456"
)

cursor = connection.cursor()


# ============================================================
# CREATE TABLE
# ============================================================

cursor.execute("""
    CREATE TABLE IF NOT EXISTS repositories (
        id SERIAL PRIMARY KEY,
        repository VARCHAR(200),
        description TEXT,
        language VARCHAR(50),
        stars INT,
        stars_today INT,
        url TEXT,
        scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")


# ============================================================
# INSERT DATA
# ============================================================

for repo in repositories:

    stars = int(repo["stars"].replace(",", ""))
    stars_today = int(repo["stars_today"].replace(",", ""))

    cursor.execute("""
        INSERT INTO repositories
        (repository, description, language, stars, stars_today, url)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        repo["repository"],
        repo["description"],
        repo["language"],
        stars,
        stars_today,
        repo["url"]
    ))


connection.commit()

cursor.close()
connection.close()


print("\nData successfully stored in PostgreSQL.")

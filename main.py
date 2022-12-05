import sqlite3
from flask import Flask


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/movie/<title>')
def page_movie(title):
    con = sqlite3.connect("netflix.db")
    cur = con.cursor()

    cur.execute(
        f"""
        SELECT title, country, release_year, type, description
        FROM netflix 
        WHERE title = '{title}'
        ORDER BY  release_year DESC
        """
    )

    result = cur.fetchone()

    data = {
        'title': result[0],
        'country': result[1],
        'release_year': result[2],
        'genre': result[3],
        'description': result[-1]
    }

    con.close()

    return data


@app.route('/movie/<int:year_from>/to/<int:year_to>')
def page_movie_between_years(year_from, year_to):
    con = sqlite3.connect("netflix.db")
    cur = con.cursor()

    cur.execute(
        f"""
        SELECT title, release_year
        FROM netflix
        WHERE release_year BETWEEN '{year_from}' AND '{year_to}'
        ORDER BY release_year ASC 
        LIMIT 100
        """
    )

    result = cur.fetchall()

    data = []
    for row in result:
        movie = {
            'title': row[0],
            'release_year': row[1],
        }
        data.append(movie)

    con.close()

    return data


app.run(host='0.0.0.0', port=800)

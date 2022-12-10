import sqlite3
from flask import Flask, jsonify

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/movie/<title>')
def page_movie(title):
    con = sqlite3.connect("netflix.db")
    cur = con.cursor()

    cur.execute(
        f"""
        SELECT title, country, release_year, listed_in, description
        FROM netflix 
        WHERE title LIKE '%{title}%'
        ORDER BY  release_year DESC
        """
    )

    result = cur.fetchone()

    if result is None:
        return jsonify(status=404)
    else:
        data = {
            'title': result[0],
            'country': result[1],
            'release_year': result[2],
            'genre': result[3],
            'description': result[-1]
        }

        con.close()

        return jsonify(data)


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

    return jsonify(data)


@app.route('/rating/<rating>')
def page_movies_by_rating(rating):
    con = sqlite3.connect("netflix.db")
    cur = con.cursor()

    query = f"""
            SELECT title, rating, description
            FROM netflix
    """

    if rating == 'children':
        query += "WHERE rating = 'G'"
    elif rating == 'family':
        query += "WHERE rating = 'G' OR rating = 'PG' OR rating = 'PG-13'"
    elif rating == 'adult':
        query += "WHERE rating = 'R' OR rating = 'NC-17'"
    else:
        return jsonify(status=404)

    query += "LIMIT 100"

    cur.execute(query)

    result = cur.fetchall()

    data = []
    for row in result:
        movie = {
            'title': row[0],
            'rating': row[1],
            'description': row[2]
        }
        data.append(movie)

    con.close()

    return jsonify(data)


@app.route('/genre/<genre>')
def page_by_genre(genre):
    con = sqlite3.connect("netflix.db")
    cur = con.cursor()

    cur.execute(
        f"""
        SELECT title, description
        FROM netflix
        WHERE  listed_in LIKE '%{genre}%'
        ORDER BY release_year DESC 
        LIMIT 10
        """
    )

    result = cur.fetchall()

    data = []
    for row in result:
        movie = {
            'title': row[0],
            'description': row[1],
        }
        data.append(movie)

    con.close()

    return jsonify(data)


app.run(host='0.0.0.0', port=800)

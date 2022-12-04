import sqlite3
from flask import Flask


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/movie/<title>')
def page_movie(title):
    con = sqlite3.connect("netflix.db")
    cur = con.cursor()

    cur.execute(f"""SELECT title, country, release_year, type, description FROM netflix WHERE title = '{title}' ORDER BY  release_year DESC""")

    result = cur.fetchone()

    data = {'title': result[0], 'country': result[1], 'release_year': result[2], 'genre': result[3],
            'description': result[-1]}
    con.close()
    print(data)
    return data


app.run(host='0.0.0.0', port=800)

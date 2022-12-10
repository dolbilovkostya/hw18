import sqlite3


def check_actors(actor1, actor2):
    con = sqlite3.connect("netflix.db")
    cur = con.cursor()

    cur.execute(f"""
                SELECT `cast`
                FROM netflix
                WHERE `cast` LIKE '%{actor1}%' AND `cast` LIKE '%{actor2}%'
                """
                )

    actors_list = cur.fetchall()

    actors_data = actors_list
    actors_play = {}
    actors_play = set(actors_play)

    """ 
    Проходимся по каждой строке, преобразуем ее во множество и объеденяем со множеством actors_play
    По итогу получаем множество со всеми именами актеров, которые играли с заданными актерами
    """
    for row in actors_data:
        row_list = set(row)
        actors = row_list.union(actors_play)
        actors_play = actors

    result = ', '.join(actors_play)

    """
    Преобразуем полученный результат в строку
    """
    result_q = result.split(', ')

    """
    Проходим по строке и ищем аткера, чье имя не совпадает с переданными в функцию актерами и встречается в строке
    более двух раз
    """
    result_actors = []
    for i in result_q:
        actor = result.count(i)
        if actor > 2 and i not in result_actors and i != actor1 and i != actor2:
            result_actors.append(i)

    """
    Получаем список актеров, которые играли с переданными в функцию актерами более двух раз
    """
    print(result_actors)


check_actors('Rose McIver', 'Ben Lamb')


def get_movies_by_type(type, year, genre):
    con = sqlite3.connect('netflix.db')
    cur = con.cursor()

    query = f"""
            SELECT title, description
            FROM netflix
            WHERE type LIKE '%{type}%' AND release_year = '{year}' AND listed_in LIKE '%{genre}%'
    """

    cur.execute(query)
    result = cur.fetchall()

    for row in result:
        movie = {
            'title': row[0],
            'description': row[1]
        }
        print(movie)


get_movies_by_type('movie', 2020, 'dramas')

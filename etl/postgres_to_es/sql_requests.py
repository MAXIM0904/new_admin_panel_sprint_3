initial_loading = """SELECT fw.id, fw.rating as imdb_rating, array_agg(DISTINCT g.name) as genre, 
        fw.title, fw.description,
        COALESCE (json_agg(DISTINCT jsonb_build_object('name', p.full_name))
        FILTER (WHERE pfw.role = 'director'), '[]') as director,
        COALESCE (json_agg(DISTINCT jsonb_build_object('name', p.full_name)) 
        FILTER (WHERE pfw.role = 'actor'),'[]') as actors_names,
        COALESCE (json_agg(DISTINCT jsonb_build_object('name', p.full_name)) 
        FILTER (WHERE pfw.role = 'writer'), '[]') as writers_names,
        COALESCE (json_agg(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name))
        FILTER (WHERE pfw.role = 'actor'), '[]') as actors, 
        COALESCE (json_agg(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name))
        FILTER (WHERE pfw.role = 'writer'), '[]') as writers
        FROM content.film_work fw
        LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
        LEFT JOIN content.person p ON p.id = pfw.person_id
        LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
        LEFT JOIN content.genre g ON g.id = gfw.genre_id GROUP BY fw.id
        HAVING fw.created > (%s) ORDER BY fw.modified;"""

checking_new_records = """SELECT fw.id, fw.rating as imdb_rating, array_agg(DISTINCT g.name) as genre, 
        fw.title, fw.description,
        COALESCE (json_agg(DISTINCT jsonb_build_object('name', p.full_name))
        FILTER (WHERE pfw.role = 'director'), '[]') as director,
        COALESCE (json_agg(DISTINCT jsonb_build_object('name', p.full_name)) 
        FILTER (WHERE pfw.role = 'actor'),'[]') as actors_names,
        COALESCE (json_agg(DISTINCT jsonb_build_object('name', p.full_name)) 
        FILTER (WHERE pfw.role = 'writer'), '[]') as writers_names,
        COALESCE (json_agg(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name))
        FILTER (WHERE pfw.role = 'actor'), '[]') as actors, 
        COALESCE (json_agg(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name))
        FILTER (WHERE pfw.role = 'writer'), '[]') as writers
        FROM content.film_work fw
        LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
        LEFT JOIN content.person p ON p.id = pfw.person_id
        LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
        LEFT JOIN content.genre g ON g.id = gfw.genre_id GROUP BY fw.id, g.id, gfw.id, p.id, pfw.id
        HAVING fw.created > (%s) or g.created > (%s) or gfw.created > (%s)
        or p.created > (%s) or pfw.created > (%s) ORDER BY fw.modified;"""


changing_entry_film_work = """SELECT fw.id, fw.rating as imdb_rating, array_agg(DISTINCT g.name) as genre, 
        fw.title, fw.description,
        COALESCE (json_agg(DISTINCT jsonb_build_object('name', p.full_name))
        FILTER (WHERE pfw.role = 'director'), '[]') as director,
        COALESCE (json_agg(DISTINCT jsonb_build_object('name', p.full_name)) 
        FILTER (WHERE pfw.role = 'actor'),'[]') as actors_names,
        COALESCE (json_agg(DISTINCT jsonb_build_object('name', p.full_name)) 
        FILTER (WHERE pfw.role = 'writer'), '[]') as writers_names,
        COALESCE (json_agg(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name))
        FILTER (WHERE pfw.role = 'actor'), '[]') as actors, 
        COALESCE (json_agg(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name))
        FILTER (WHERE pfw.role = 'writer'), '[]') as writers
        FROM content.film_work fw
        LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
        LEFT JOIN content.person p ON p.id = pfw.person_id
        LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
        LEFT JOIN content.genre g ON g.id = gfw.genre_id 
        GROUP by fw.id
        HAVING fw.modified > (%s)"""

changing_entry_person = """SELECT fw.id, fw.rating as imdb_rating, array_agg(DISTINCT g.name) as genre, 
        fw.title, fw.description,
        COALESCE (json_agg(DISTINCT jsonb_build_object('name', p.full_name))
        FILTER (WHERE pfw.role = 'director'), '[]') as director,
        COALESCE (json_agg(DISTINCT jsonb_build_object('name', p.full_name)) 
        FILTER (WHERE pfw.role = 'actor'),'[]') as actors_names,
        COALESCE (json_agg(DISTINCT jsonb_build_object('name', p.full_name)) 
        FILTER (WHERE pfw.role = 'writer'), '[]') as writers_names,
        COALESCE (json_agg(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name))
        FILTER (WHERE pfw.role = 'actor'), '[]') as actors, 
        COALESCE (json_agg(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name))
        FILTER (WHERE pfw.role = 'writer'), '[]') as writers
        FROM content.film_work fw
        LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
        LEFT JOIN content.person p ON p.id = pfw.person_id
        LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
        LEFT JOIN content.genre g ON g.id = gfw.genre_id 
        GROUP by p.id, fw.id
        HAVING p.modified > (%s)"""

changing_entry_genre = """SELECT fw.id, fw.rating as imdb_rating, array_agg(DISTINCT g.name) as genre, 
        fw.title, fw.description,
        COALESCE (json_agg(DISTINCT jsonb_build_object('name', p.full_name))
        FILTER (WHERE pfw.role = 'director'), '[]') as director,
        COALESCE (json_agg(DISTINCT jsonb_build_object('name', p.full_name)) 
        FILTER (WHERE pfw.role = 'actor'),'[]') as actors_names,
        COALESCE (json_agg(DISTINCT jsonb_build_object('name', p.full_name)) 
        FILTER (WHERE pfw.role = 'writer'), '[]') as writers_names,
        COALESCE (json_agg(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name))
        FILTER (WHERE pfw.role = 'actor'), '[]') as actors, 
        COALESCE (json_agg(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name))
        FILTER (WHERE pfw.role = 'writer'), '[]') as writers
        FROM content.film_work fw
        LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
        LEFT JOIN content.person p ON p.id = pfw.person_id
        LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
        LEFT JOIN content.genre g ON g.id = gfw.genre_id 
        GROUP by g.id, fw.id
        HAVING g.modified > (%s)"""
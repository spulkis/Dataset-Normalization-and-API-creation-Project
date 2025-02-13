from sqlalchemy import text

def create_view(engine):
    with engine.connect() as connection:
        sql = text("""
        CREATE VIEW movies_and_shows_view AS
        SELECT 
            'movie' AS media_type,
            m.index,
            m.movie_id,
            NULL AS show_id,
            m.title,
            m.release_year,
            m.age_certification,
            m.runtime,
            NULL AS seasons,
            g.genre,
            pc.country,
            d.director AS director,
            a.actor AS actor,
            c.character,
            i.imdb_score,
            i.imdb_votes
        FROM movies m
        LEFT JOIN genres_bridge gb ON m.movie_id = gb.movie_id
        LEFT JOIN genres g ON gb.genre_id = g.genre_id
        LEFT JOIN production_countries_bridge pcb ON m.movie_id = pcb.movie_id
        LEFT JOIN production_countries pc ON pcb.country_id = pc.country_id
        LEFT JOIN directors_bridge db ON m.movie_id = db.movie_id
        LEFT JOIN directors d ON db.director_id = d.director_id
        LEFT JOIN actors_bridge ab ON m.movie_id = ab.movie_id
        LEFT JOIN actors a ON ab.actor_id = a.actor_id
        LEFT JOIN characters_bridge cb ON m.movie_id = cb.movie_id AND ab.actor_id = cb.actor_id
        LEFT JOIN characters c ON cb.character_id = c.character_id
        LEFT JOIN imdb_info i ON m.movie_id = i.movie_id
        UNION ALL
        SELECT 
            'show' AS media_type,
            s.index,
            NULL AS movie_id,
            s.show_id,
            s.title,
            s.release_year,
            s.age_certification,
            s.runtime,
            s.seasons,
            g.genre,
            pc.country,
            d.director AS director,
            a.actor AS actor,
            c.character,
            i.imdb_score,
            i.imdb_votes
        FROM shows s
        LEFT JOIN genres_bridge gb ON s.show_id = gb.show_id
        LEFT JOIN genres g ON gb.genre_id = g.genre_id
        LEFT JOIN production_countries_bridge pcb ON s.show_id = pcb.show_id
        LEFT JOIN production_countries pc ON pcb.country_id = pc.country_id
        LEFT JOIN directors_bridge db ON s.show_id = db.show_id
        LEFT JOIN directors d ON db.director_id = d.director_id
        LEFT JOIN actors_bridge ab ON s.show_id = ab.show_id
        LEFT JOIN actors a ON ab.actor_id = a.actor_id
        LEFT JOIN characters_bridge cb ON s.show_id = cb.show_id AND ab.actor_id = cb.actor_id
        LEFT JOIN characters c ON cb.character_id = c.character_id
        LEFT JOIN imdb_info i ON s.show_id = i.show_id
        """)
        connection.execute(sql)
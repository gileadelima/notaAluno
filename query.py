def select(cursor, filter=0, *attributes):
    if len(attributes) > 0:
        x = ', '.join(attributes)
    else:
        x = '*'

    if filter:
        query_select = f'SELECT {x} FROM alunos WHERE nota > 7'
    else:
        query_select = f'SELECT {x} FROM alunos'

    cursor.execute(query_select)
    return cursor.fetchall()

def insert(cursor, cnx, nome, curso, nota):
    query_insert = "INSERT INTO alunos (nome, curso, nota) VALUES (%s, %s, %s)"
    cursor.execute(query_insert, (nome, curso, nota))
    cnx.commit()

def update(cursor, cnx, id, nome, curso, nota):
    query_update = "UPDATE alunos SET nome = %s, curso = %s, nota = %s WHERE id = %s"
    cursor.execute(query_update, (nome, curso, nota, id))
    cnx.commit()

def delete(cursor, cnx, id):
    query_delete = "DELETE FROM alunos WHERE id = %s"
    cursor.execute(query_delete, (id,))
    cnx.commit()

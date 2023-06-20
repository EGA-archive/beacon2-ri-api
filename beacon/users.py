import asyncio
import asyncpg
import datetime

async def main():
    # Establish a connection to an existing database named "test"
    # as a "postgres" user.
    try:
        conn = await asyncpg.connect('postgresql://admin:secret@idp-db:5432/keycloak?sslmode=disable')
        records = await conn.fetch('''
        SELECT * FROM keycloak_group;
        ''')
        values = [dict(record) for record in records]
        print(values)
        print('Connected!')
    except asyncpg.PostgresError:
        print('error occurred', e)
    # Execute a statement to create a new table.
    

    # Close the connection.
    #await conn.close()

hola = asyncio.get_event_loop().run_until_complete(main())
print(hola)
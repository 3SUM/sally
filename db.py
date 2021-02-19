import psycopg2
from config import Config

params = Config()


def create_table(cur):
    sql = """
        CREATE TABLE IF NOT EXISTS testy (name VARCHAR(255) NOT NULL, rep INTEGER NOT NULL, UNIQUE(name))
        """
    cur.execute(sql)


def insert(cur, name: str, rep: int):
    print(name)
    print(rep)
    sql = """
        INSERT INTO testy (name, rep) VALUES (%s, %s);
        """
    cur.execute(sql, (name, rep))


if __name__ == "__main__":
    # connect to the PostgreSQL server
    print("Connecting to the PostgreSQL database...")
    conn = psycopg2.connect(
        database=params.DATABASE,
        user=params.USER,
        password=params.PASSWORD,
        host=params.HOST,
        port=params.PORT,
    )

    # create a cursor
    cur = conn.cursor()

    create_table(cur)
    insert(cur, "luis", 10)

    # close the communication with the PostgreSQL
    cur.close()

    # commit the changes
    conn.commit()
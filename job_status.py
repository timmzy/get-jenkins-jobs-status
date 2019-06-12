# Import Jenkins Api
import jenkinsapi, sqlite3
from sqlite3 import Error
from datetime import datetime
from jenkinsapi.jenkins import Jenkins

class DatabaseOperation(object):
    def __init__(self, db_name):
        self.db_name = db_name

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
        except Error as e:
            print(e)

    def create_table(self):
        try:
            cur = self.conn.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS jobs (id integer PRIMARY KEY,
                        job text, build text, status text, time_stamp text)""")
            self.conn.commit()
        except Error as e:
            print(e)

    def insert_data(self, data):
        try:
            cur = self.conn.cursor()
            cur.execute("""INSERT INTO jobs(job, build, status, time_stamp ) VALUES(?, ?, ?, ?)""", data)
            self.conn.commit()
        except Error as e:
            print(e)

    def view_all(self):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM jobs")
            rows = cur.fetchall()
            for row in rows:
                print(row)
        except Error as e:
            print(e)

    def close_connection(self):
        self.conn.close()

def main():
    print("Starting...")
    # Load Jenkins instance and authenticate
    J = Jenkins('http://localhost:8080', 'admin', '8488jenkins')
    # Get Job list
    jobs = J.keys()
    # Start database operations
    db = DatabaseOperation("jobs_data.db")
    db.connect()
    db.create_table()
    for job in jobs:
        # Get last build
        build = J[job].get_last_build()
        # Get status
        status = build.get_status()
        time = datetime.now().strftime("%B %d, %Y %I:%M%p")
        data = (job, str(build), status, time)
        db.insert_data(data)
    db.close_connection()

    print("Complete")

if __name__ == '__main__':
    main()

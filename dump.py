import psycopg2
import numpy as np


class Data:
    def __init__(self, config):
        self.cur = psycopg2.connect(config).cursor()
    def fetch(self, sql):
        self.cur.execute(sql)
        return self.cur.fetchall()

if __name__ == "__main__":
    data = Data("dbname=postgres host=localhost port=55432 user=postgres")
    rows = data.fetch("SELECT * FROM export.commits")
    np.savez_compressed("vcc_data.npz", np.array(rows))

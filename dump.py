import psycopg2
import psycopg2.extensions
import numpy as np

psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

class Data:
    def __init__(self, config):
        self.cur = psycopg2.connect(config).cursor()
    def fetch(self, sql):
        self.cur.execute(sql)
        return self.cur.fetchall()

if __name__ == "__main__":
    data = Data("dbname=postgres host=localhost port=55432 user=postgres")
    rows = data.fetch("SELECT * FROM export.commits")
    np.savez_compressed("var/vcc_data.npz", np.array(rows))
    #
    # vcc = data.fetch("SELECT * FROM export.commits WHERE type  = 'blamed_commit' LIMIT 40")
    # ucc = data.fetch("SELECT * FROM export.commits WHERE type != 'blamed_commit' LIMIT 800")
    # sample = np.concatenate([vcc, ucc])
    # np.random.shuffle(sample)
    # np.savez_compressed("var/vcc_sample_40x800.npz", sample)

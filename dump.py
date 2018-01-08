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
    query_all = """
        select
          c.*,
          r.*
        from export.commits as c
        left join export.repositories as r
        on c.repository_id = r.id
    """
    query_vulnerable = """
        select
              c.*,
              r.*
        from export.commits as c
        left join export.repositories as r
        on c.repository_id = r.id
        where c.type = 'blamed_commit'
        limit 40;
    """
    query_unclassified = """
        select
              c.*,
              r.*
        from export.commits as c
        left join export.repositories as r
        on c.repository_id = r.id
        where c.type != 'blamed_commit'
        limit 800;
    """
    data = Data("dbname=postgres host=localhost port=55432 user=postgres")
    # rows = data.fetch(query_all)
    # np.savez_compressed("var/vcc_data.npz", np.array(rows))
    vcc = data.fetch(query_vulnerable)
    ucc = data.fetch(query_unclassified)
    sample = np.concatenate([vcc, ucc])
    np.random.shuffle(sample)
    np.savez_compressed("var/vcc_data_40x800.npz", sample)

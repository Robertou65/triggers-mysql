import os

class QueryLoader:
    def __init__(self, sql_file="queries.sql"):
        self.queries = {}
        self._load_queries(sql_file)

    def _load_queries(self, sqlfile):
        file_path = os.path.join(os.path.dirname(__file__), sqlfile)
        with open(file_path, 'r') as f:
            content = f.read()

        raw_queries = [q.strip() + ';'for q in content.split(';')]

        self.queries['insert_blog'] = raw_queries[0]
        self.queries['find_id_blog'] = raw_queries[1]
        self.queries['find_all_blog'] = raw_queries[2]
        self.queries['delete_blog'] = raw_queries[3]
        self.queries['insert_notification'] = raw_queries[4]
        self.queries['find_id_notification'] = raw_queries[5]
        self.queries['find_all_notification'] = raw_queries[6]
        self.queries['delete_notification'] = raw_queries[7]

    def get(self, query_name) -> str:
        return self.queries.get(query_name)
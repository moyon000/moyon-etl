# contructor del obj db
import db

def insert(table,data):
    sql = list()
    for x in data:
        keys = ["%s" % k for k in x.keys()]
        values = ["%s" % v for v in x.values()]
        sql.append("INSERT INTO %s (" %(table))
        sql.append(", ".join(keys))
        sql.append(") VALUES (")
        sql.append(", ".join(values))
        sql.append(") ON DUPLICATE KEY UPDATE")
        sql.append(";\n")
    return("".join(sql))
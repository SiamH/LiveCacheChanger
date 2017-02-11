import sqlite3

sqlite_file = 'keyVal.sqlite'    # name of the sqlite database file
table_name = 'keyval'  # name of the table to be created
field_key = 'key' # name of the column
field_type = 'TEXT'  # column data type
field_value = 'value' # name of the column

# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

c.execute('DROP TABLE keyval')

# Creating a new SQLite table with 1 column
c.execute('CREATE TABLE {tn} ({nf1} {ft1})'\
        .format(tn=table_name, nf1=field_key, ft1=field_type))
c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
        .format(tn=table_name, cn=field_value, ct=field_type))


dicts = {'Name': 'Zara', 'Age': 'seven', 'Class': 'First'}

c.execute('SELECT * FROM {tn}'.\
        format(tn=table_name))
all_rows = c.fetchall()
print('1):', all_rows)

for k, v in dicts.iteritems():
    try:
        c.execute("INSERT INTO {tn} ({nf1}, {nf2}) VALUES (k, v)".\
            format(tn=table_name, nf1=field_key, nf2=field_value))
    except sqlite3.IntegrityError:
        print'ERROR: ID already exists in PRIMARY KEY column'

# Committing changes and closing the connection to the database file
conn.commit()
conn.close()

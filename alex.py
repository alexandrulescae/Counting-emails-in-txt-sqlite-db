import sqlite3
import re

conn = sqlite3.connect('alex.sqlite')
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS Counts')
cur.execute('CREATE TABLE Counts (org TEXT, count INTEGER)')

fname = 'mbox.txt'
fh = open(fname)
for line in fh:
    if not line.startswith('From: '):continue
    #pieces  = line.split()
    #pieces2 = re.findall('@(.+)', pieces[1])
    #pieces3 = pieces2[0].split('.')
    #organization = pieces3[0]
    pieces = line.split()
    pieces2 = pieces[1].split('@')
    print(pieces2[1])
    cur.execute('SELECT count FROM Counts WHERE org = ? ', (pieces2[1],))
    row = cur.fetchone()
    if row is None:
        cur.execute('INSERT INTO Counts (org, count) VALUES (?, 1)', (pieces2[1],))
    else:
        cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ?', (pieces2[1],))
        conn.commit()


sqlstr = 'SELECT org, count FROM Counts ORDER BY count'
for row in cur.execute(sqlstr):
    print(str(row[0]), row[1])

cur.close()
#!/usr/bin/env python
"""Manages the storage of the values
"""
__author__ = "Artur Balanuta"
__version__ = "1.0.0"
__email__ = "artur.balanuta [at] tecnico.ulisboa.pt"


import sqlite3
import os


def get_last():
	query = '''
			select * 
			from ambient
			order by datetime desc 
			limit 1;
			'''

#Runs only if called
if __name__ == "__main__":
	
	full_path = os.path.realpath(__file__)
	dir_path = os.path.dirname(full_path)
	
	conn = sqlite3.connect(dir_path + '/database.sqlite3.db')
	
	c = conn.cursor()
	
	
	
	# Create table
	try:
		c.execute('''CREATE TABLE ambient (datetime TIMESTAMP, temperature REAL, humidity REAL)''')
	except:
		print "Table Already Exists, Ignoring"
		
		
	# Insert a row of data
	c.execute("INSERT INTO ambient VALUES ('2014-04-16 00:32:49.741009', 27.1, 49)")
	c.execute("INSERT INTO ambient VALUES ('2014-04-20 00:32:49.741009', 27.1, 50)")
	c.execute("INSERT INTO ambient VALUES ('2015-04-15 00:32:49.141009', 25.1, 49)")
	c.execute("INSERT INTO ambient VALUES ('2014-04-15 00:32:49.741001', 27.1, 100)")
	c.execute("INSERT INTO ambient VALUES ('2014-04-15 00:32:49.741019', 27.1, 89)")
	c.execute("INSERT INTO ambient VALUES ('2014-04-15 01:32:49.741109', 27.1, 49)")
	c.execute("INSERT INTO ambient VALUES ('2014-04-15 00:32:49.740009', 23.1, 0)")
	c.execute("INSERT INTO ambient VALUES ('2014-04-15 00:32:49.741009', 27.122, 49)")
	c.execute("INSERT INTO ambient VALUES ('2016-05-15 00:32:41.741009', 21.1, 49)")
	
	query = '''
			SELECT * 
			FROM ambient
			ORDER BY datetime DESC 
			LIMIT 1;
			'''

	c.execute(query)
	all = c.fetchall()
	print all
	
	
	
	
	# Save (commit) the changes
	conn.commit()

	# We can also close the connection if we are done with it.
	# Just be sure any changes have been committed or they will be lost.
	conn.close()

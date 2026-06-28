#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This was based on this.
# https://kamedassou.com/python_sqlite/
#
import sqlite3
import time
import http.server as server
import argparse
import datetime

def exec(db_path, query, param = None):
	"""
	Execute the Query

	Args:
		db_path (str): Database path
		query (str): Query string
		param (tuple): Optional parameter

	"""
	# Connect to the database
	conn = sqlite3.connect(db_path)
	# Get cursor
	cur = conn.cursor()
	# Execute SQL
	if param:
		cur.execute(query,param)
	else:
		cur.execute(query)
	# Commit
	conn.commit()
	# Close connection
	conn.close()

def select(db_path, query, param = None):
	"""
	Execute the Select

	Args:
		db_path (str): Database path
		query (str): Select string
		param (tuple): Optional parameter

	Returns:
		tuple: Result tuple

	"""
	# Connect to the database
	conn = sqlite3.connect(db_path)
	# Get cursor
	cur = conn.cursor()
	# Execute SQL
	if param:
		cur.execute(query,param)
	else:
		cur.execute(query)
		
	# Fetch cursor
	rows = cur.fetchall()
	# Close connection
	conn.close()
	return rows

class MyHandler(server.BaseHTTPRequestHandler):
	def do_POST(self):
		self.send_response(200)
		self.send_header('Content-Type', 'text/plain; charset=utf-8')
		self.end_headers()
		self.wfile.write(b'{"result": "post OK"}')

		print('path=[{}]'.format(self.path))
		if (self.path != "/upload_multipart"): return

		# Get request
		content_len  = int(self.headers.get("content-length"))
		#body = self.rfile.read(content_len).decode('utf-8')
		body = self.rfile.read(content_len)
		print("content_len={}".format(content_len))
		print("type(body)={}".format(type(body)))
		start = body.find(b"\r\n\r\n")
		print("start={}".format(start))
		end = body.find(b"\r\n--X-ESPIDF_MULTIPART--\r\n\r\n")
		print("end={}".format(end))

		image = body[start+4:end]
		#print("---------------------")
		#print(body)
		#print("---------------------")
		#print(image)

		dt = datetime.datetime.now()
		date = dt.strftime('%Y/%m/%d')
		time = dt.strftime('%H:%M:%S')
		print("date={}".format(date))
		print("time={}".format(time))

		# Insert BLOB
		strsql = "INSERT INTO images(date, time, image) VALUES(?, ?, ?)"
		parameters = (date, time, image)
		exec(args.path, strsql, parameters)
		print("Image inserted")

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--path', help='db path', required=True)
	parser.add_argument('--port', type=int, help='http port', default=8080)
	args = parser.parse_args() 
	print("args.path={}".format(args.path))
	print("args.port={}".format(args.port))

	# Create the table if it does not exist
	strsql = "select count(*) from sqlite_master where name = 'images'"
	ret = select(args.path, strsql)
	#print("ret={}".format(ret[0]))
	print("ret={}".format(ret[0][0]))
	#print("ret={}".format(type(ret[0][0])))
	if ret[0][0] == 0:
		print("Create Table")
		strsql = "CREATE TABLE images (id integer primary key autoincrement, date text not null, time text not null, image blob not null)"
		exec(args.path, strsql)

	host = '0.0.0.0'
	httpd = server.HTTPServer((host, args.port), MyHandler)
	#httpd = server.ThreadingHTTPServer((host, port), MyHandler)
	httpd.serve_forever()

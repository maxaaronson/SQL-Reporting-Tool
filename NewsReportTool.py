#!/usr/bin/env python3
#
# Created by Max Aaronson
# 2/13/18

# This python program performs 3 queries on the 'news' Postgres database

import psycopg2
import psycopg2.extras

print("Reporting tool running...\n\n")

# connect to the news db
conn = psycopg2.connect("dbname=news")

# this cursor will create a dictionary as the query result
cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)


print("The three most popular articles of all time are:\n")

# Create the query that will be run on the data
SQL = "select replace(replace(path, '/article/', ''), '-', ' ') as path, " +\
      "count(*) as count from log where path != '/' " +\
      "group by path order by count(*) desc limit 3;"

# run the query on the db
cursor.execute(SQL)

# iterate through the output
for row in cursor:
    print("%s - %d views" % (row['path'], row['count'],))

print("\n\n")


print("The most popular authors of all time are:\n")

SQL = "select sum(A.num::int), authors.name from " +\
      "(select replace(right(left(path, -1), -9), '-', ' ') " +\
      "as title, count(*) as num from log where substr(path, 10) != '' " +\
      "group by path order by count(*) desc) as A, articles, authors " +\
      "where position(lower(A.title) in lower(articles.title)) > 0 " +\
      "and articles.author = authors.id " +\
      "group by authors.id;"

cursor.execute(SQL)

for row in cursor:
    print("%s - %d views" % (row['name'], row['sum'],))

print("\n\n")

print("more than 1% of requests lead to errors on these days:\n")

SQL = "select A.time::date, A.count::float, B.count::float as count2, " +\
      "(B.count/A.count::float)*100 as C from " +\
      "(select time::date, count(*) as count from log group by " +\
      "time::date order by count(*) desc) as A, " +\
      "(select time::date, count(*) as count from log where status = " +\
      "'404 NOT FOUND' group by time::date order by count(*) desc) as B " +\
      "where A.time::date = B.time::date " +\
      "and (B.count/A.count::float)*100 > 1 " +\
      "order by C desc;"

cursor.execute(SQL)

for row in cursor:
    print("date: %s, total reqs: %d, errors: "
          "%d, percent errors: %f" % (row['time'], row['count'],
                                      row['count2'], row['c'],))

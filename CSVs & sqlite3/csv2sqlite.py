#!/usr/bin/env python
# Author: Ansh Chandnani
# May 25 2020
# Python program to read a CSV file and create a coressponding sqlite database

import sqlite3
import csv

def printResult():
	result = cursor.fetchall()
	for row in result:
		for item in row:
			print(item, end="\t")
		print()
	print('-----------------------------------------------------------------------')


dbName = 'HW6.db'
sqlStream = sqlite3.connect(dbName)
cursor = sqlStream.cursor()


try:									# dropping table if exists
	cursor.execute('DROP TABLE CreditCard')
	print('Refreshing Database...\n')
except sqlite3.OperationalError:		# creating dbase
	print('Creating New Database...\n')

# creating table
createTable = "CREATE TABLE CreditCard(ID INT PRIMARY KEY, LIMIT_BAL INT, SEX INT, EDUCATION INT, MARRIAGE INT, AGE INT, PAY_0 INT, PAY_2 INT, PAY_3 INT, PAY_4 INT, PAY_5 INT, PAY_6 INT, BILL_AMT1 INT, BILL_AMT2 INT, BILL_AMT3 INT, BILL_AMT4 INT, BILL_AMT5 INT, BILL_AMT6 INT, PAY_AMT1 INT, PAY_AMT2 INT, PAY_AMT3 INT, PAY_AMT4 INT, PAY_AMT5 INT, PAY_AMT6 INT, default_payment_next_month INT)"
cursor.execute(createTable)


fieldList = ['ID', 'LIMIT_BAL', 'SEX', 'EDUCATION', 'MARIAGE', 'AGE', 'PAY_0', 'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6', 'BILL_AMT1', 'BILL_AMT2', 'BILL_AMT3', 'BILL_AMT4', 'BILL_AMT5', 'BILL_AMT6', 'PAY_AMT1', 'PAY_AMT2', 'PAY_AMT3', 'PAY_AMT4', 'PAY_AMT5', 'PAY_AMT6', 'deafult.payment.next.month']

csvFile = open("UCI_Credit_Card.csv")
csvStream = csv.reader(csvFile)

c = 1
for row in csvStream:								# returns each row of csv as a list
	if c > 1:
		query = "INSERT INTO CreditCard VALUES("
		for i in range(len(row)):					# loop to traverse one row
			query += row[i] + ","
		query = query[:-1]		# removes comma at the end of query
		query += ")"
		cursor.execute(query)
		# print('Executed:', query)
	c += 1

print('\nInserted', c, 'records in table.\n')
print('-----------------------------------------------------------------------')

# Executing queries and analytics

# Update the data so that marriage=2 (single) and marriage=3 (others) are merged into 2 (single).
cursor.execute("UPDATE CreditCard SET MARRIAGE=2 WHERE MARRIAGE = 2 OR MARRIAGE = 3")

# cursor.execute("SELECT * FROM CreditCard WHERE MARRIAGE = 3")
# print(cursor.fetchall())
# Test returns empty set

# Remove all data records with negative BILL_AMT values (in any of the BILL_AMT1 through BILL_AMT6
cursor.execute("DELETE FROM CreditCard WHERE BILL_AMT1 < 0 OR BILL_AMT2 < 0 OR BILL_AMT3 < 0 OR BILL_AMT4 < 0 OR BILL_AMT5 < 0 OR BILL_AMT6 < 0")

# Select and show the first 10 records in the database table, using SELECT … LIMIT… ;
for item in fieldList:
	print(item, end=" ")
print()
cursor.execute("SELECT * FROM CreditCard LIMIT 10")
printResult()

# Select and show all records with a BILL_AMT1 amount greater than 500k;
for item in fieldList:
	print(item, end=" ")
print()
cursor.execute("SELECT * FROM CreditCard WHERE BILL_AMT1 > 500000")
printResult()

# Compute the total number of records, average AGE, min LIMIT_BAL, max LIMIT_BAL in the data;
print("COUNT(*) AVG(AGE) \t MIN(LIMIT_BAL) MAX(LIMIT_BAL)\n")
cursor.execute("SELECT COUNT(*), AVG(AGE), MIN(LIMIT_BAL), MAX(LIMIT_BAL) FROM CreditCard")
printResult()

# Count the # records, average AGE, min LIMIT_BAL, max LIMIT_BAL for default.payment.next.month=0 (no default) vs. default.payment.next.month=1 (default), using GROUP BY;
print("default_payment_next_month COUNT(*) AVG(AGE) \t MIN(LIMIT_BAL) MAX(LIMIT_BAL)\n")
cursor.execute("SELECT default_payment_next_month, COUNT(*), AVG(AGE), MIN(LIMIT_BAL), MAX(LIMIT_BAL) FROM CreditCard WHERE default_payment_next_month = 0 OR default_payment_next_month = 1 GROUP BY default_payment_next_month")
printResult()

# Count the # records, average AGE, min LIMIT_BAL, max LIMIT_BAL for each marriage group (1, 2), again using GROUP BY;
print("MARRIAGE COUNT(*) AVG(AGE) \t MIN(LIMIT_BAL) MAX(LIMIT_BAL)\n")
cursor.execute("SELECT MARRIAGE, COUNT(*), AVG(AGE), MIN(LIMIT_BAL), MAX(LIMIT_BAL) FROM CreditCard WHERE MARRIAGE = 1 OR MARRIAGE = 2 GROUP BY MARRIAGE")
printResult()

# Count the # records in each marriage group who will default (1) vs. not default (0).
print("MARRIAGE COUNT(MARRIAGE) default_payment_next_month")
cursor.execute("SELECT MARRIAGE, COUNT(MARRIAGE), default_payment_next_month FROM CreditCard WHERE default_payment_next_month = 0 OR default_payment_next_month = 1 GROUP BY default_payment_next_month")
printResult()

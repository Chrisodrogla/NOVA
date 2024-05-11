import os
import pyodbc

# Azure SQL Database connection string
connection_string = os.environ.get('SECRET_CHRISTIANSQL_STRING')

# Establish connection
conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

# Data to insert
data = [{'Link': 'https',
  'Link Id': '70',
  'Rental Name': 'Wind',
  'Reviews Count': '8.0',
  'Star Reviews': '4',
  'Date Gathered': '2024-05-10',
  'Date Gathered Hours': '2024-05-10 17:41:52'},
 {'Link': 'htt',
  'Link Id': '70455',
  'Rental Name': 'Stak',
  'Reviews Count': '8.0',
  'Star Reviews': '2',
  'Date Gathered': '2024-05-10',
  'Date Gathered Hours': '2024-05-10 17:41:52'}]  # Your data

overall_impressions = [('December, 2023',
  '0',
  '1,835',
  'http6',
  '76',
  'Wiey',
  '2024-05-10',
  '2024-05-10 17:41:52'),
 ('January, 2024',
  '0',
  '2,365',
  'htts:',
  '70456',
  'WindHiey',
  '2024-05-10',
  '2024-05-10 17:41:52')]  # Your overall_impressions data

# Retrieve insert queries
insert_query1 = os.environ.get('INSERT_QUERY_1')
insert_query2 = os.environ.get('INSERT_QUERY_2')

# Insert data into table1
for item in data:
    cursor.execute(insert_query1, (item['Link'], item['Link Id'], item['Rental Name'], item['Star Reviews'], item['Reviews Count'], item['Date Gathered'], item['Date Gathered Hours']))

# Insert data into table2
for item in overall_impressions:
    cursor.execute(insert_query2, (item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7]))

# Commit changes
conn.commit()

# Close connection
conn.close()

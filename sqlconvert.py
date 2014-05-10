#-*- coding: utf-8 -*-
import xlrd
#import csv
from os import sys

# Example of sql query template:
TEMPLATE_TABLE_1 = 'insert into TABLE_NAME(col1, col2, col3,col4,col5,col6,col7,col8,col9,col10,col11,col12,col13,col14,col15,col16) values("{0}", "{1}", "{2}","{3}","{4}","{5}","{6}","{7}","{8}","{9}","{10}","{11}","{12}","{13}","{14}","{15}");';
# Edit the above line to the required schema

def convert(excel_file):
	try:
		excel = xlrd.open_workbook(excel_file)
	except:
		print 'Error the file {0}, not found ;('.format(excel_file)
		exit(0)

	all_sheets = excel.sheet_names()
	for sheet_name in all_sheets:
		sheet = excel.sheet_by_name(sheet_name)

		my_sql = open(''.join([sheet_name, '.sql']), 'w+')

		#my_csv = open(''.join([sheet_name, '.csv']), 'wb')
		#writer = csv.writer(my_csv, quoting=csv.QUOTE_ALL)

		for row in xrange(sheet.nrows):
			items = []
			for a in sheet.row_values(row):
				items.append(unicode(a).encode('utf-8'))
			#print TEMPLATE_TABLE_1.format(items[0], items[1], items[2])
			my_sql.write(TEMPLATE_TABLE_1.format(items[0], items[1], items[2],items[3],items[4],items[5],items[6],items[7],items[8],items[9],items[10],items[11],items[12],items[13],items[14],items[15]))
			#writer.writerow([unicode(entry).encode("utf-8") for entry in sheet.row_values(row)])
		#my_csv.close()
		my_sql.close()


if __name__ == '__main__':
	if len(sys.argv) == 2:
		convert(sys.argv[1])
	else:
		print 'the xlsx file ?'
#-*- coding: utf-8 -*-
import xlrd
#import csv
from os import sys

# Example of sql query template:
TEMPLATE_TABLE_1 = 'insert into Schools(Slno, Name, kitchen_location,latitude,longitude,type,class,route_code,route_name,range) values("{0}", "{1}", "{2}","{3}","{4}","{5}","{6}","{7}","{8}","{9}");';

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
			my_sql.write(TEMPLATE_TABLE_1.format(items[0], items[1], items[2],items[3],items[4],items[5],items[6],items[7],items[8],items[9])+'\n')
			#writer.writerow([unicode(entry).encode("utf-8") for entry in sheet.row_values(row)])
		#my_csv.close()
		my_sql.close()


if __name__ == '__main__':
	if len(sys.argv) == 2:
		convert(sys.argv[1])
	else:
		print 'the xlsx file ?'
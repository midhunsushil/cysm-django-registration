import csv, os

# csv file path
path = os.path.join("media","chat_mon_game")
# csv file name
filename = "chatlog.csv"
# csv file path
csvfilepath = os.path.join(path, filename)

# initializing the titles and rows list
fields = []
rows = []

# reading csv file
with open(csvfilepath, 'r') as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile)

    # extracting field names through first row
    fields = next(csvreader)

    # extracting each data row one by one
    for row in csvreader:
        rows.append(row)

    # get total number of rows
    print("Total no. of rows: %d"%(csvreader.line_num))

# printing the field names
print('Field names are:' + ', '.join(field for field in fields))

#  printing first 5 rows
print('\nFirst 5 rows are:\n')
for row in rows:
    # parsing each column of a row
    colno = 1
    for col in row:
        if(colno == 1):
            print("%3s"%col,end = ''),
        elif(colno == 2 ):
            print("%10s"%col,end = ''),
        else:
            print("\t",col,end = '')

        colno = colno + 1
    print('')

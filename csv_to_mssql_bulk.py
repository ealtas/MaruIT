import pyodbc #to connect to SQL Server
import re

sqlConnStr = ('DRIVER={SQL Server Native Client 11.0};'+
              'Server=ServerName;Database=dbname;'+
              'Trusted_Connection=YES') 
            
sqlConn = pyodbc.connect(sqlConnStr, autocommit = True)
curs = sqlConn.cursor()

#(?i) to ignore case
#[^/]+ then matches any characters until it comes to the end of the line or a /
fNameRe = re.compile(r'(?i)(?<=/FName )[^/]+')
lNameRe = re.compile(r'(?i)(?<=/LName )[^/]+')

#not making sure it is actually a phone number
phoneRe = re.compile(r'(?i)(?<=/phone )[^/]+')

addressRe = re.compile(r'(?i)(?<=/address )[^/]+')

with open('YOUR_TEXT.txt') as inF:
    for line in inF:
        fName = fNameRe.findall(line)[0]
        fName = fName.strip() #remove any trailing spaces or line breaks
        lName = lNameRe.findall(line)[0]
        lName = lName.strip() 
        phone = phoneRe.findall(line)[0]
        phone = phone.strip()
        address = addressRe.findall(line)[0]
        address = address.strip()
        #generate the SQL to insert into the database
        #parameterize it both to encourage query plan reuse
        #and to protect against potential SQL Injection in the file
        sql = """INSERT INTO dbo.people 
                (FName, LName, phone, address)
                values (?, ?, ?, ?)"""
        
        curs.execute(sql, fName, lName, phone, address)       
        
curs.commit()       
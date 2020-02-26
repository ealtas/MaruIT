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

with open('YOUR_TEXT_PEOPLE.txt') as inF:
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

orderdateRe = re.compile(r'(?i)(?<=/Odate )[^/]+')
orderamountRe = re.compile(r'(?i)(?<=/Oamount )[^/]+')

#not making sure it is actually a phone number
phoneRe = re.compile(r'(?i)(?<=/phone )[^/]+')

taxamountRe = re.compile(r'(?i)(?<=/tamount )[^/]+')

with open('YOUR_TEXT_ORDER.txt') as inF:
    for line in inF:
        orderdate = orderdateRe.findall(line)[0]
        orderdate = orderdate.strip() #remove any trailing spaces or line breaks
        orderamount = orderamountRe.findall(line)[0]
        orderamount = orderamount.strip() 
        phone = phoneRe.findall(line)[0]
        phone = phone.strip()
        taxamount = taxamountRe.findall(line)[0]
        taxamount = taxamount.strip()
        #generate the SQL to insert into the database
        #parameterize it both to encourage query plan reuse
        #and to protect against potential SQL Injection in the file
        sql = """INSERT INTO dbo.orders 
                (phone, order_date, order_amount, tax_amount)
                values (?, ?, ?, ?)"""
        
        curs.execute(sql, phone, orderdate, orderamount, taxamount) 
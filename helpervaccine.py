import csv
import io
import os

class Vaccine:
    def __init__(self, Vaccine_name, diseasename,vaccinemanufacturedate,vaccineexpirydate,purpose,StockInDate,StockInQuantity,StockInQuantityPrice,StockOutDate,StockOutQuantity,BalanceStockQuantity,BalanceStockPrice ):
        self.Vaccine_name = Vaccine_name
        self.diseasename = diseasename
        self.vaccinemanufacturedate = vaccinemanufacturedate
        self.vaccineexpirydate = vaccineexpirydate
        self.purpose = purpose
        self.StockInDate = StockInDate
        self.StockInQuantity = StockInQuantity
        self.StockInQuantityPrice = StockInQuantityPrice
        self.StockOutDate = StockOutDate
        self.StockOutQuantity = StockOutQuantity
        self.BalanceStockQuantity = BalanceStockQuantity
        self.BalanceStockPrice = BalanceStockPrice
    

    def __str__(self):
        return 'Vaccine : [ Name : {}, Disease Name : {}, manufacture_date : {}, expiry_date : {}, purpose : {}, StockInDate : {}, StockInQuantity: {},StockInQuantityPrice:{},StockOutDate: {},StockOutQuantity : {},BalanceStockQuantity : {},BalanceStockPrice :{}]'.format(
            self.Vaccine_name, self.diseasename, self.vaccinemanufacturedate, self.vaccineexpirydate, self.purpose, 
            self.StockInDate, self.StockInQuantity,self.StockInQuantityPrice,self.StockOutDate,self.StockOutQuantity,
            self.BalanceStockQuantity,self.BalanceStockPrice)

def create_vaccineexcel_sheet(path):
    
    file = os.path.join(path, os.environ.get('VACCINE_APP_EXCEL_FILENAME', 'vaccinedata.csv'))

    if not os.path.exists(file):
        print("file not exists...")
        # Create the file with header row if it doesn't exist
        with open(file, 'w') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Vaccine_name', 'diseasename', 'vaccinemanufacturedate','vaccineexpirydate','purpose','StockInDate','StockInQuantity','StockInQuantityPrice','StockOutDate','StockOutQuantity','BalanceStockQuantity','BalanceStockPrice'])


# Define a function to add data to an existing Excel workbook
def add_vaccinedata_to_excel_sheet(path, vac):

    # Load the existing workbook
    file = os.path.join(path, os.environ.get('VACCINE_APP_EXCEL_FILENAME', 'vaccinedata.csv'))

    # Now the file exists, so we can open it in append mode and add new rows
    with open(file, 'a') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([vac.Vaccine_name, vac.diseasename, vac.vaccinemanufacturedate,vac.vaccineexpirydate,vac.purpose,vac.StockInDate,vac.StockInQuantity,vac.StockInQuantityPrice,vac.StockOutDate,vac.StockOutQuantity,vac.BalanceStockQuantity,vac.BalanceStockPrice])

    # Return a response indicating that the file was updated
    return "updated"
    

def get_vaccinedata_from_excel_sheet(path):
    # Load the existing workbook
    file = os.path.join(path, os.environ.get('VACCINE_APP_EXCEL_FILENAME', 'vaccinedata.csv'))
    
    data = []

    # Open the CSV file and read the rows into a list of dictionaries
    with open(file) as csvfile:
        csv_reader = csv.DictReader(csvfile)

        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            data.append(row)

    return data
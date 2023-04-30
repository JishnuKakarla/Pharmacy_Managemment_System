import csv
import io
import os

class Medicine:
    def __init__(self, Medicine_name,Typeofmedicine, medicinemanufacturedate,medicineexpirydate,purpose,StockInDate,StockInQuantity,StockInQuantityPrice,StockOutDate,StockOutQuantity,BalanceStockQuantity,BalanceStockPrice):
        self.Medicine_name = Medicine_name
        self.Typeofmedicine = Typeofmedicine
        self.medicinemanufacturedate = medicinemanufacturedate
        self.medicineexpirydate = medicineexpirydate
        self.purpose = purpose
        self.StockInDate = StockInDate
        self.StockInQuantity = StockInQuantity
        self.StockInQuantityPrice = StockInQuantityPrice
        self.StockOutDate = StockOutDate
        self.StockOutQuantity = StockOutQuantity
        self.BalanceStockQuantity = BalanceStockQuantity
        self.BalanceStockPrice = BalanceStockPrice

    def __str__(self):
        return 'Medicine : [ Name : {}, Type : {}, manufacture_date : {}, expiry_date : {}, purpose : {}, StockInDate : {}, StockInQuantity: {},StockInQuantityPrice:{},StockOutDate: {},StockOutQuantity : {},BalanceStockQuantity : {},BalanceStockPrice :{}]'.format(
            self.Medicine_name, self.Typeofmedicine, self.medicinemanufacturedate, self.medicineexpirydate, self.purpose, 
            self.StockInDate, self.StockInQuantity,self.StockInQuantityPrice,self.StockOutDate,self.StockOutQuantity,
            self.BalanceStockQuantity,self.BalanceStockPrice)

def create_medicineexcel_sheet(path):
    
    file = os.path.join(path, os.environ.get('MEDICINE_APP_EXCEL_FILENAME', 'medicinedata.csv'))

    if not os.path.exists(file):
        print("file not exists...")
        # Create the file with header row if it doesn't exist
        with open(file, 'w') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Medicine_name', 'Typeofmedicine', 'medicinemanufacturedate','medicineexpirydate','purpose',
            'StockInDate','StockInQuantity','StockInQuantityPrice','StockOutDate','StockOutQuantity','BalanceStockQuantity','BalanceStockPrice'])


# Define a function to add data to an existing Excel workbook
def add_medicinedata_to_excel_sheet(path, med):

    # Load the existing workbook
    file = os.path.join(path, os.environ.get('MEDICINE_APP_EXCEL_FILENAME', 'medicinedata.csv'))

    # Now the file exists, so we can open it in append mode and add new rows
    with open(file, 'a') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([med.Medicine_name, med.Typeofmedicine, med.medicinemanufacturedate,med.medicineexpirydate,med.purpose,med.StockInDate,med.StockInQuantity,med.StockInQuantityPrice,med.StockOutDate,med.StockOutQuantity,med.BalanceStockQuantity,med.BalanceStockPrice])

    # Return a response indicating that the file was updated
    return "updated"
    

def get_medicinedata_from_excel_sheet(path):
    # Load the existing workbook
    file = os.path.join(path, os.environ.get('MEDICINE_APP_EXCEL_FILENAME', 'medicinedata.csv'))
    
    data = []

    # Open the CSV file and read the rows into a list of dictionaries
    with open(file) as csvfile:
        csv_reader = csv.DictReader(csvfile)

        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            data.append(row)

    return data
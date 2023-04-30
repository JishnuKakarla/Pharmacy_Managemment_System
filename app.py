from flask import Flask, make_response, render_template, request
from flask import send_from_directory
from helpermedicine import Medicine, create_medicineexcel_sheet, add_medicinedata_to_excel_sheet, get_medicinedata_from_excel_sheet
from helpervaccine import Vaccine, create_vaccineexcel_sheet, add_vaccinedata_to_excel_sheet, get_vaccinedata_from_excel_sheet
import os
import io

app = Flask(__name__)

# Get environment variables or use defaults
host = os.environ.get('FLASK_HOST', '0.0.0.0')
port = os.environ.get('FLASK_PORT', '5000')
debug = os.environ.get('FLASK_DEBUG', False)


@app.route('/', methods= ["GET"])
def index():
    
    return render_template('index.html')

@app.route('/medicines', methods= ["GET"])
def medicines():

    print("main / call")
    path = os.path.join(app.root_path, 'sheets/')
    create_medicineexcel_sheet(path)

    return render_template('medicine.html')

@app.route('/vaccines', methods= ["GET"])
def vaccines():

    print("main / call")
    path = os.path.join(app.root_path, 'sheets/')
    create_vaccineexcel_sheet(path)

    return render_template('vaccine.html')

@app.route('/addmedicine', methods=['POST'])
def addmedicine():
    med = Medicine(
        request.form['Medicine_name'], 
        request.form['Typeofmedicine'], 
        request.form['medicinemanufacturedate'], 
        request.form['medicineexpirydate'], 
        request.form['purpose'], 
        request.form['StockInDate'],
        request.form['StockInQuantity'],
        request.form['StockInQuantityPrice'],
        request.form['StockOutDate'],
        request.form['StockOutQuantity'],
        request.form['BalanceStockQuantity'],
        request.form['BalanceStockPrice']
        
    )
    path = os.path.join(app.root_path, 'sheets/')
    result = add_medicinedata_to_excel_sheet(path, med)

    return result
    
@app.route('/addvaccine', methods=['POST'])
def addvaccine():
    vac = Vaccine(
        request.form['Vaccine_name'], 
        request.form['diseasename'], 
        request.form['vaccinemanufacturedate'], 
        request.form['vaccineexpirydate'], 
        request.form['purpose'], 
        request.form['StockInDate'],
        request.form['StockInQuantity'],
        request.form['StockInQuantityPrice'],
        request.form['StockOutDate'],
        request.form['StockOutQuantity'],
        request.form['BalanceStockQuantity'],
        request.form['BalanceStockPrice'], 
    )
    path = os.path.join(app.root_path, 'sheets/')
    result = add_vaccinedata_to_excel_sheet(path, vac)

    return result
    

@app.route('/listmedicine')
def list_medicinedata():
    
    path = os.path.join(app.root_path, 'sheets/')
    medicinedata = get_medicinedata_from_excel_sheet(path)
    print(medicinedata)

    return render_template('list_medicine.html', data=medicinedata)

@app.route('/listvaccine')
def list_vaccinedata():
    
    path = os.path.join(app.root_path, 'sheets/')
    vaccinedata = get_vaccinedata_from_excel_sheet(path)
    print(vaccinedata)

    return render_template('list_vaccine.html', data=vaccinedata)

if __name__ == '__main__':
    app.run()

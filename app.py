from flask import Flask, make_response, render_template, request
from flask import send_from_directory
from helpermedicine import Medicine, create_medicineexcel_sheet, add_medicinedata_to_excel_sheet, get_medicinedata_from_excel_sheet
from helpervaccine import Vaccine, create_vaccineexcel_sheet, add_vaccinedata_to_excel_sheet, get_vaccinedata_from_excel_sheet
import os
import io
import json

import matplotlib.pyplot as plt
import pandas as pd

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

    path = os.path.join(app.root_path, 'sheets/')
    create_medicineexcel_sheet(path)

    return render_template('medicine.html')

@app.route('/vaccines', methods= ["GET"])
def vaccines():

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
        request.form['stockOutDate'],
        request.form['StockOutQuantity'],
        request.form['BalanceStockQuantity'],
        request.form['BalanceStockPrice']
        
    )
    print(str(med))
    path = os.path.join(app.root_path, 'sheets/')
    result = add_medicinedata_to_excel_sheet(path, med)
    if result == "updated":
        path = os.path.join(app.root_path, 'sheets/')
        medicinedata = get_medicinedata_from_excel_sheet(path)
        return render_template('list_medicine.html', data=medicinedata)
    else:
        return "Failed to update.."
    
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

    if result == "updated":
        path = os.path.join(app.root_path, 'sheets/')
        vaccinedata = get_vaccinedata_from_excel_sheet(path)
        return render_template('list_vaccine.html', data=vaccinedata)
    else:
        return "Failed to update.."
    

@app.route('/listmedicine')
def list_medicinedata():
    
    path = os.path.join(app.root_path, 'sheets/')
    medicinedata = get_medicinedata_from_excel_sheet(path)

    return render_template('list_medicine.html', data=medicinedata)

@app.route('/listmeds')
def list_meds():
    path = os.path.join(app.root_path, 'sheets/')
    medicinedata = get_medicinedata_from_excel_sheet(path)

    return json.dumps(medicinedata)


@app.route('/listvaccine')
def list_vaccinedata():
    path = os.path.join(app.root_path, 'sheets/')
    vaccinedata = get_vaccinedata_from_excel_sheet(path)

    return render_template('list_vaccine.html', data=vaccinedata)

@app.route('/listvacs')
def list_vacs():
    path = os.path.join(app.root_path, 'sheets/')
    vaccinedata = get_vaccinedata_from_excel_sheet(path)

    return json.dumps(vaccinedata)

@app.route('/medicinedatavis')
def visualize():    

    df =  pd.read_csv('./sheets/medicinedata.csv')
    medicineName_data = df["medicine_name"]
    stockInQuantity_data = df["StockInQuantity"]
    balanceStockQuantity_data = df["BalanceStockQuantity"]
    medicinePrice_date =  df["StockInQuantityPrice"]

    #------------- Medicines Name vs Quantity pie chart --------------
    fig1 = plt.figure(figsize=(7,7))
    plt.pie(stockInQuantity_data, labels=medicineName_data, autopct='%.2f')
    fig1.savefig('./static/medicine_pie_chart.png')

    
    #------------- Stock in quantiy vs Available stock by Medicine Name --------------
    # Creating figure and axis objects
    fig2, ax = plt.subplots()

    # Setting axis labels and title
    ax.set_xlabel('Medicines')
    ax.set_ylabel('Stock')
    ax.set_title('Stock of Medicines')

    # Creating bar plots
    ax.bar(medicineName_data, stockInQuantity_data, width=0.4, label='Total Stock')
    ax.bar(medicineName_data, balanceStockQuantity_data, width=0.4, label='Stock Available')

    # Adding legend
    ax.legend()

    # Saving the plot to an image file
    plt.savefig('./static/medicine_bar_graph.png')

    #------------- Medicine price vs Medicine Name --------------
    # plotting the graph
    plt.subplots()
    plt.bar(medicineName_data, medicinePrice_date)
    plt.xlabel('Medicine Name')
    plt.ylabel('Medicine Price')
    plt.title('Medicine Price vs Medicine Name')

    # displaying the graph
    plt.savefig('./static/medicine_price_bar_graph.png')

    
    #------Reading vaccine data---------------
    df =  pd.read_csv('./sheets/vaccinedata.csv')
    vaccineName_data = df["vaccine_name"]
    stockInQuantity_data = df["StockInQuantity"]
    balanceStockQuantity_data = df["BalanceStockQuantity"]
    StockInQuantityPrice_date = df["StockInQuantityPrice"]
    #------------- Vaccine Name vs Quantity pie chart --------------
    
    fig = plt.figure(figsize=(5,5))
    plt.pie(stockInQuantity_data, labels=vaccineName_data, autopct='%.2f')
    fig.savefig('./static/vaccine_pie_chart.png')

    #------------- Stock in quantiy vs Available stock by Vaccine Name --------------
    fig, ax = plt.subplots()

    # Setting axis labels and title
    ax.set_xlabel('Vaccines')
    ax.set_ylabel('Stock')
    ax.set_title('Stock of Vaccines')

    # Creating bar plots
    ax.bar(vaccineName_data, stockInQuantity_data, width=0.4, label='Total Stock')
    ax.bar(vaccineName_data, balanceStockQuantity_data, width=0.4, label='Stock Available')

    # Adding legend
    ax.legend()

    # Saving the plot to an image file
    plt.savefig('./static/vaccines_bar_graph.png')

    #------------- Medicine price vs Medicine Name --------------
    # plotting the graph
    plt.subplots()
    plt.bar(vaccineName_data, StockInQuantityPrice_date)
    plt.xlabel('Vaccine Name')
    plt.ylabel('Vaccine Price')
    plt.title('Vaccine Price vs Vaccine Name')

    # displaying the graph
    plt.savefig('./static/vaccine_price_bar_graph.png')

    return render_template('medicinedatavis.html')
    


if __name__ == '__main__':
    app.run()

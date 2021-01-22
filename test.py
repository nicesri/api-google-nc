import geopy.distance as ps
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

cerds = ServiceAccountCredentials.from_json_keyfile_name("cerds.json", scope)

client = gspread.authorize(cerds)

sheet = client.open("แบบฟอร์มกรอกข้อมูลเพื่อทำการนัดหมายและ Request assistant (Responses)").worksheet('Form Responses 1') # เป็นการเปิดไปยังหน้าชีตนั้นๆ

### web service
from flask import Flask , jsonify, request
app = Flask(__name__)

def loadEmployee():
    data = sheet.get_all_records()
    listdata = pd.DataFrame(data)
    return listdata

def searchEmployee(name):
    data = sheet.get_all_records()
    listdata = pd.DataFrame(data)
    employee = listdata[ listdata['Name'] == name ]
    return employee

@app.route('/getEmployee' , methods=['GET'])
def getEmployee():
    try:
        name = request.args.get('name')
        res = searchEmployee(name)
        msg = ''
        for i in range(len(res)):
            show = res.iloc[i]
            msg = msg + "บ้านเลขที่ "+ str(show['บ้านเลขที่']) + "\n"
        if msg == '':
            msg = "ไม่มีคนที่คุณค้นหา"

        return jsonify({'message' : msg })
    except Exception as e:
        return jsonify({'message' : 'error นะดูใหม่อีกที'})

if __name__ == '__main__':
    app.run(debug=True)

from datetime import datetime, timedelta
import mysql.connector
import json
from flask import make_response, jsonify
import jwt
from Configuration.config import dbconfig

class book_model():
    def __init__(self):
        self.con = mysql.connector.connect(host=dbconfig['host'],user=dbconfig['username'],password=dbconfig['password'],database=dbconfig['database'])
        self.con.autocommit=True
        self.cur = self.con.cursor(dictionary=True)
        
    def all_book_model(self):
        self.cur.execute("SELECT * FROM books")
        result = self.cur.fetchall()
        print(result)
        if len(result)>0:
            return make_response({"payload":result},200)
        else:
            return json.dumps([])
    
    def add_book_model(self,data):
        self.cur.execute(f"INSERT INTO books(category, name, author) VALUES('{data['category']}', '{data['name']}','{data['author']}')")        
        return make_response({"message":"CREATED_SUCCESSFULLY"},201)
    
    def delete_book_model(self,id):
        self.cur.execute(f"DELETE FROM books WHERE id={id}")
        if self.cur.rowcount>0:
            return make_response({"message":"DELETED_SUCCESSFULLY"},202)
        else:
            return make_response({"message":"CONTACT_DEVELOPER"},500)
        
    
    def update_book_model(self,data, id):
        self.cur.execute(f"UPDATE books SET name='{data['name']}', category='{data['category']}', author='{data['author']}' WHERE id={id}")
        if self.cur.rowcount>0:
            return make_response({"message":"UPDATED_SUCCESSFULLY"},201)
        else:
            return make_response({"message":"NOTHING_TO_UPDATE"},204)

    def patch_book_model(self, data):
        qry = "UPDATE books SET "
        for key in data:
            if key!='id':
                qry += f"{key}='{data[key]}',"
        qry = qry[:-1] + f" WHERE id = {data['id']}"
        self.cur.execute(qry)
        if self.cur.rowcount>0:
            return make_response({"message":"UPDATED_SUCCESSFULLY"},201)
        else:
            return make_response({"message":"NOTHING_TO_UPDATE"},204)
        

    def user_login_model(self, username, password):
        self.cur.execute(f"SELECT id, role, email, name, phone from users WHERE name='{username}' and password='{password}'")
        result = self.cur.fetchall()
        if len(result)==1:
            exptime = datetime.now() + timedelta(minutes=30)
            exp_epoc_time = exptime.timestamp()
            data = {
                "payload":result[0],
                "exp":int(exp_epoc_time)
            }
            print(int(exp_epoc_time))
            jwt_token = jwt.encode(data, dbconfig["secretKey"], algorithm="HS256")
            return make_response({"token":jwt_token}, 200)
        else:
            return make_response({"message":"NO SUCH USER"}, 204)
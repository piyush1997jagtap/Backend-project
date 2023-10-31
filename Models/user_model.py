from datetime import datetime, timedelta
import mysql.connector
import json
from flask import make_response, jsonify
import jwt
from Configuration.config import dbconfig

class user_model():
    def __init__(self):
        self.con = mysql.connector.connect(host=dbconfig['host'],user=dbconfig['username'],password=dbconfig['password'],database=dbconfig['database'])
        self.con.autocommit=True
        self.cur = self.con.cursor(dictionary=True)
        
    def get_all_users_data(self):
        self.cur.execute("SELECT * FROM users")
        result = self.cur.fetchall()
        print(result)
        if len(result)>0:
            return make_response({"payload":result},200)
        else:
            return "No Data Found"
        
    def get_user_data(self, id):
        self.cur.execute(f"SELECT * FROM users WHERE id={id}")
        result = self.cur.fetchall()
        print(result)
        if len(result)>0:
            return make_response({"payload":result},200)
        else:
            return "User does not exist"
        
    def add_user_data(self,data):
        self.cur.execute(f"INSERT INTO users(name, email, phone, role, password) VALUES('{data['name']}', '{data['email']}', '{data['phone']}', '{data['role']}', '{data['password']}')")
        return make_response({"message":"CREATED_SUCCESSFULLY"},201)

    def delete_user_data(self,id):
        self.cur.execute(f"DELETE FROM users WHERE id={id}")
        if self.cur.rowcount>0:
            return make_response({"message":"DELETED_SUCCESSFULLY"},202)
        else:
            return make_response({"message":"Server Error"},500)
    
    def update_user_data(self,data, id):
        self.cur.execute(f"UPDATE users SET name='{data['name']}', email='{data['email']}', phone='{data['phone']}', role='{data['role']}',password='{data['password']}', avatar='{data['avatar']}' WHERE id={id}")
        if self.cur.rowcount>0:
            return make_response({"message":"UPDATED_SUCCESSFULLY"},201)
        else:
            return make_response({"message":"NOTHING_TO_UPDATE"},204)

    def patch_user_model(self, data):
        qry = "UPDATE users SET "
        for key in data:
            if key!='id':
                qry += f"{key}='{data[key]}',"
        qry = qry[:-1] + f" WHERE id = {data['id']}"
        self.cur.execute(qry)
        if self.cur.rowcount>0:
            return make_response({"message":"UPDATED_SUCCESSFULLY"},201)
        else:
            return make_response({"message":"NOTHING_TO_UPDATE"},204)

    def upload_avatar_data(self, uid, db_path):
        try:
            self.cur.execute(f"UPDATE users SET avatar='{db_path}' WHERE id={uid}")
        except Exception as e:
            print(str(e))
        if self.cur.rowcount>0:
            return make_response({"message":"FILE_UPLOADED_SUCCESSFULLY", "path":db_path},201)
        else:
            return make_response({"message":"NOTHING_TO_UPDATE"},204)

    def get_avatar_path_data(self, uid):
        self.cur.execute(f"SELECT avatar FROM users WHERE id={uid}")
        result = self.cur.fetchall()
        if len(result)>0:
            print(type(result))
            return {"payload":result}
        else:
            return make_response({"message": "No data found"}, 204)  
        
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
            return make_response({"message":"INVALID CREDENTIALS"}, 204)
            
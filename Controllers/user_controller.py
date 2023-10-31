import flask
from flask import make_response, request, send_file
from app import app
from Models.user_model import user_model
from Models.auth_model import auth_model
import os
from datetime import datetime
obj = user_model()
auth = auth_model()
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
# max size of uploaded file must be less than 1MB

@app.route("/user/all")
# The endpoint for token_auth() is automatically getting calculated in the auth_model.token_auth() method
@auth.token_auth()
def all_users():
    return obj.all_user_model()

@app.route("/user/<id>", methods=["GET"])
def get_user(id):
    return obj.get_user_model(id)

@auth.token_auth()
@app.route("/user/add", methods=["POST"])
def add_user():
    return obj.add_user_model(request.form)

@app.route("/user/addmultiple", methods=["POST"])
def add_multiple_users():
    return obj.add_multiple_users_model(request.json)

@app.route("/user/delete/<id>", methods=["DELETE"])
def delete_user(id):
    print(request.form)
    print(id)
    return obj.delete_user_model(id)

@app.route("/user/update/<id>", methods=["PUT"])
def update_user():
    print(request.form)
    return obj.update_user_model(request.form, id)

@app.route("/user/patch", methods=["PATCH"])
def patch_user():
    return obj.patch_user_model(request.form)

@app.route("/user/page/<pno>/limit/<limit>", methods=["get"])
def pagination(pno, limit):
    return obj.pagination_model(pno, limit)

@app.route("/user/<uid>/avatar/upload", methods=["PATCH"])
def upload_avatar(uid):
    file = request.files['avatar']
    print(file.__sizeof__)
    new_filename =  str(datetime.now().timestamp()).replace(".", "") # Generating unique name for the file
    split_filename = file.filename.split(".") # Spliting ORIGINAL filename to seperate extenstion
    ext_pos = len(split_filename)-1 # Canlculating last index of the list got by splitting the filname
    ext = split_filename[ext_pos] # Using last index to get the file extension
    if(ext != "jpg" or ext != "jpeg"):
          return make_response({"message": "File must be in jpg or jpeg format"}, 413)
    else:
        db_path = f"uploads/{new_filename}.{ext}"
        file.save(f"uploads/{new_filename}.{ext}")
        return obj.upload_avatar_model(uid, db_path)

@app.route("/user/avatar/<uid>", methods=["GET"])
def get_avatar(uid):
    data = obj.get_avatar_path_model(uid)
    print(data)
    print(app.instance_path)
    root_dir = os.path.dirname(app.instance_path)
    print(root_dir)

    return send_file(f"{root_dir}/{data['payload'][0]['avatar']}")

@app.errorhandler(413)
def too_large(e):
    return make_response({"message": "File is too large"}, 413)


@app.route("/user/login",methods=["POST"])
def user_login():
    auth_data = request.form
    print(auth_data)
    return obj.user_login_model(auth_data['username'], auth_data['password'])
import flask
from flask import make_response, request, send_file
from app import app
from Models.user_model import user_model
from Models.auth_model import auth_model
import os
from datetime import datetime
userObject = user_model()
auth = auth_model()
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
# max size of uploaded file must be less than 1MB

@app.route("/user/all")
# The endpoint for token_auth() is calculated in the auth_model.token_auth() method
@auth.token_auth()
def get_all_users():
    return userObject.get_all_users_data()

@app.route("/user/<id>", methods=["GET"])
def get_user(id):
    return userObject.get_user_data(id)

@auth.token_auth()
@app.route("/user/add", methods=["POST"])
def add_user():
    return userObject.add_user_data(request.form)

@app.route("/user/delete/<id>", methods=["DELETE"])
def delete_user(id):
    print(request.form)
    print(id)
    return userObject.delete_user_data(id)

@app.route("/user/update/<id>", methods=["PUT"])
def update_user():
    print(request.form)
    return userObject.update_user_data(request.form, id)

@app.route("/user/patch", methods=["PATCH"])
def patch_user():
    return userObject.patch_user_model(request.form)

@app.route("/user/<uid>/avatar/upload", methods=["PATCH"])
def upload_avatar(uid):
    file = request.files['avatar']
    new_filename =  str(datetime.now().timestamp()).replace(".", "") # Generating unique name for the file
    split_filename = file.filename.split(".") # Spliting Original filename to seperate extenstion
    ext_pos = len(split_filename)-1 # Canlculating last index of the list got by splitting the filname
    extension = split_filename[ext_pos] # Using last index to get the file extension
    allowedExtensions = ["jpg", "jpeg"]
    if extension not in allowedExtensions:
          return make_response({"message": "File must be in jpg or jpeg format"}, 413)
    else:
        db_path = f"uploads/{new_filename}.{extension}"
        file.save(f"uploads/{new_filename}.{extension}")
        return userObject.upload_avatar_data(uid, db_path)

@app.route("/user/avatar/<uid>", methods=["GET"])
def get_avatar(uid):
    data = userObject.get_avatar_path_data(uid)
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
    return userObject.user_login_model(auth_data['username'], auth_data['password'])
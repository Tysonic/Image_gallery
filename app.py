from flask import Flask, redirect, request, flash, render_template, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

App = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
App.config['SECRET_KEY'] = "THIS IS LOVELY"
App.config['IMAGE_UPLOADER'] = "static\images"
App.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, "imageDB")
App.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
upload = os.path.join(basedir, App.config["IMAGE_UPLOADER"])
Allowed_image_type = ["JPG", 'JPEG', 'PNG', 'GIF']
db = SQLAlchemy(App)
Migrate(App, db)


class ImageUploader(FlaskForm):
    image = FileField("Select Image")
    submit = SubmitField("Upload")


class ImageDB(db.Model):
    _id = db.Column(db.Integer, primary_key=True, index=True, autoincrement=True)
    image_name = db.Column(db.String)

    def __init__(self, image_name):
        self.image_name = image_name

    def __repr__(self):
        return f"{self.image_name}"

    @property
    def id(self):
        return self._id


@App.route('/', methods=['POST', 'GET'])
def upload_image():
    form = ImageUploader()
    if request.method == 'POST' and form.validate_on_submit():
        file = request.files['image']
        filename = secure_filename(file.filename)
        new_image = ImageDB(image_name=filename)
        db.session.add(new_image)
        db.session.commit()
        file.save(os.path.join(upload, filename))
        # return redirect(url_for("images"))
    return render_template("home.html", form=form)


@App.route("/images", methods=['POST', 'GET'])
def images():
    images = ImageDB.query.all()

    return render_template("images.html", images=images)


@App.route("/image list <filename>")
def send_image(filename):
    return send_from_directory("static/images", filename)


if __name__ == '__main__':
    App.run(debug=True)

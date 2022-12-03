from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from application import app

if __name__ == '__main__':
    app.run(debug=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
db = SQLAlchemy(app)


class User(db.Model):
    password_hash = db.Column(db.String(length=60), nullable=False)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True, primary_key=True)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def __init__(self, username, email):
        self.password_hash = username
        self.email_address = email

    def __repr__(self):
        return '<User %r>' % self.email_address

with app.app_context():
    db.create_all()

    db.session.add(User('Pass123', 'career@tech387.com'))
    db.session.commit()

    users = User.query.all()
    print(users)
from flask_wtf import Form
from wtforms import StringField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField
from wtforms import validators, ValidationError

class loginForm(Form):
    UserName = StringField("Username", [validators.DataRequired("Please enter your name.")])
    PWLength = StringField("Length of the password", [validators.DataRequired("Please enter length of Password from 1-40.")])
    retention = StringField("Number of days to retain password", [validators.DataRequired("Please enter a number of days to retain password")])
    Number = StringField("Retrieval Code", [validators.DataRequired("Please enter your Retreival code")])
    submit = SubmitField("Send")
from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, EmailField
from wtforms.validators import InputRequired, Length, Email 

class AgentForm(FlaskForm):
    firstname = StringField('firstname', 
                    validators=[InputRequired(), Length(min=4, max=20)], 
                    render_kw={'placeholder':'First Name'})
    
    lastname = StringField('lastname', 
                    validators=[InputRequired(), Length(min=4, max=20)], 
                    render_kw={'placeholder':'Last Name'})

    email = EmailField('email', 
                    validators=[InputRequired(), Length(min=10, max=100), 
                    Email(message="Invalid Email!")], 
                    render_kw={'placeholder':'Email'})

    password = PasswordField('password', 
                    validators=[InputRequired(), Length(min=4,max=100)], 
                    render_kw={'placeholder':'Password'})

    submit = SubmitField('Add New Agent!')


    #create forms
class SignUpForm(FlaskForm):
    user = StringField('user', 
                    validators=[InputRequired(), Length(min=4, max=20)], 
                    render_kw={'placeholder':'Username'})

    email = EmailField('email', 
                    validators=[InputRequired(), Length(min=10, max=100), 
                    Email(message="Invalid Email!",check_deliverability=True)], 
                    render_kw={'placeholder':'Email'})

    password = PasswordField('password', 
                    validators=[InputRequired(), Length(min=4,max=100)], 
                    render_kw={'placeholder':'Password'})

    submit = SubmitField('Sign Up')


    # def validate_email(self, email):
    #     existing_user_email = Users.query.filter_by(email=email.data).first()
    #     if existing_user_email:
    #         flash("That email already exists! Try a different one.", "info")
            

class LoginForm(FlaskForm):
    email = EmailField('email', 
                        validators=[InputRequired(), Length(min=10, max=100), 
                        Email(message="Invalid Email!",check_deliverability=True)], 
                        render_kw={'placeholder':'Email'})

    password = PasswordField('password', 
                        validators=[InputRequired(), Length(min=4,max=100)], 
                        render_kw={'placeholder':'Password'})

    submit = SubmitField('Sign In')


class TaskForm(FlaskForm):
    types = SelectField(label='Task Type', 
                        choices=[('To Do','To Do'), ('Doing','Doing'), ('Done','Done')], 
                        render_kw={'placeholder':'Enter task label'})

    title = StringField(label='Task Label', 
                        validators=[InputRequired(), Length(min=4, max=20)], 
                        render_kw={'placeholder':'Enter task label'})

    description = TextAreaField(label='Description', 
                        validators=[InputRequired(), Length(min=4, max=100)], 
                        render_kw={'placeholder':'Enter your task description'})

    submit = SubmitField('Submit')
# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField,IntegerField,SelectField
# from wtforms.validators import DataRequired, Length, ValidationError, EqualTo
# from app.models import User
# class signUpForm(FlaskForm):
#     user= StringField('User', validators=[DataRequired(), Length(min=5, message=('Your user is too short.'))])    
#     password = PasswordField('Password',  validators=[DataRequired(), Length(min=8, message=('Your password is too short.'))])
#     rePassword = PasswordField('reType Password',  validators=[DataRequired(), EqualTo('password', message='Passwords must match')]) 
#     checkbox = RadioField('Bạn là:', choices = ['Sinh viên', 'Giảng viên']) 
    
#     submit = SubmitField('Sign Up')
   
#     def validate_user(self,user):
#       user = User.query.filter_by(user=user.data).first()
#       if user is not None:
#             raise ValidationError('username has been already used! Please use a different username.')
# class sinhvienForm(FlaskForm):
#    mssv= StringField('Mã số sinh viên')
#    ten = StringField('Họ và tên')
#    lop= StringField('Lớp')
#    khoa= StringField('Khoa')
#    submit = SubmitField('Ok')
# class giangvienForm(FlaskForm):
#    msgv= StringField('Mã số giảng viên')
#    ten = StringField('Họ và tên')
#    khoa= StringField('Khoa')
#    submit = SubmitField('Ok')
# class loginForm(FlaskForm):
#     user= StringField('User', validators=[DataRequired()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     remember_me = BooleanField('Remember me')
#     submit = SubmitField('Sign In') 
# class monhocForm(FlaskForm):
#    mamh= StringField('Mã số môn học')
#    ten = StringField('Tên môn học')
#    sotin= IntegerField('Số tín chỉ')
#    conlai= IntegerField('Sĩ số còn lại')
#    giangvien =SelectField('Giảng viên', choices=[])
#    submit = SubmitField('Thêm') 

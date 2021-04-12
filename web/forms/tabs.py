from flask_wtf import FlaskForm
from wtforms import FileField, IntegerField, StringField
from wtforms.validators import DataRequired


class UploadForm(FlaskForm):

    upload_file = FileField('Guitar Pro File', validators=[DataRequired()])

    band = StringField('Band', validators=[DataRequired()])
    album = StringField('Album', validators=[DataRequired()])
    song = StringField('Song', validators=[DataRequired()])
    track = IntegerField('Track', default=0)


class ReplaceFileForm(FlaskForm):

    upload_file = FileField('Guitar Pro File', validators=[DataRequired()])


class EditForm(FlaskForm):

    band = StringField('Band', validators=[DataRequired()])
    album = StringField('Album', validators=[DataRequired()])
    song = StringField('Song', validators=[DataRequired()])
    track = IntegerField('Track', default=0)

import flask.ext.wtf 
from wtforms import DecimalField, TextField, SelectField, FieldList, \
                    FormField, SubmitField, Form, IntegerField, HiddenField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, NumberRange
from .models import Frequency, Year, Status

class EntryForm(flask.ext.wtf.Form):
    """ Initial form to narrow down type of tax to be calculated """
    frequency = QuerySelectField(u'Frequency', 
                                 query_factory=Frequency.get_frequency, 
                                 get_label='frequency')
    year = QuerySelectField(u'Year', query_factory=Year.get_year,
                                 get_label='year')
    status = QuerySelectField(u'Status', 
                             query_factory=Status.get_status,
                             get_label='status')

class DForm(Form):
    d_name = TextField(label="Deduction Name", 
                       validators=[DataRequired()])
    d_amount = DecimalField(label="Deduction Amount", 
                            places=2, 
                            default=0.00, 
                            validators=[DataRequired()])
    d_deferred = SelectField(choices=[('no', 'NOT DEFERRED'), 
                                      ('yes', 'DEFERRED')])

class LevelForm(Form):
    num = IntegerField(label="Unknown Deduction", 
                       default=0, validators=[NumberRange(min=0,max=10)])
    level_id = HiddenField()
    def __init__(self, *args, **kwargs):
        super(LevelForm, self).__init__(*args, **kwargs)
        if '_label' in kwargs and kwargs['_label'] is not None:
            self.num.label.text = "Number of {} deductions".format(kwargs['_label'])
        if '_level_id' in kwargs and kwargs['_level_id'] is not None:
            self.level_id.data = kwargs['_level_id']

class PaycheckForm(Form):
    """ Form capturing input from paycheck """
    earnings = DecimalField(label="Paycheck Earning", 
                            places=2, 
                            default=0.00, 
                            validators=[DataRequired()])

    allowances = FieldList(FormField(LevelForm), min_entries=1)
    
class DeductionsForm(flask.ext.wtf.Form):
    paycheck = FormField(PaycheckForm)

    pre_deductions =  FieldList(FormField(DForm), min_entries=1, max_entries=15)
    pre_deduction_add = SubmitField(label="Add Pre Tax Deduction")

    post_deductions =  FieldList(FormField(DForm), min_entries=1, max_entries=15)
    post_deduction_add = SubmitField(label="Add Post Tax Deduction")


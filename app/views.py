from flask import render_template, flash, redirect, url_for
from app import app
from .forms import DeductionsForm, EntryForm
from .models import Entry, Year, Frequency, Status, Withholding, Level

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',
                           title='Home')

@app.route('/begin', methods=['GET', 'POST'])
def begin():
    form = EntryForm()
    if form.validate_on_submit():
        return redirect(url_for('calculate', 
                                year=form.year.data.year, 
                                frequency=form.frequency.data.frequency,
                                status=form.status.data.status))
    else: 
        return render_template('begin.html',
                               title='Select Year and Frequency',
                               form=form)
         
@app.route('/calculate/<year>/<frequency>/<status>', methods=['GET', 'POST'])
def calculate(year, frequency, status):

    paycheck_allowances = [{'_label': l.level, '_level_id': l.id} 
                           for l in Level.query.all()]
    form = DeductionsForm(paycheck = dict(allowances=paycheck_allowances))

    # Validate user choices exist
    entry_id = Entry.query.with_entities(Entry.id) \
            .join(Year).filter_by(year = year) \
            .join(Frequency).filter_by(frequency = frequency) \
            .scalar()

    if entry_id == None:
        flash('Invalid Year/Frequency Combination')
        return redirect('/begin')

    s = Status.query.filter_by(status=status).first()
    if s == None:
        flash('Invalid Status')
        return redirect('/begin')

    # TEMP - add additonal entry fields for pre and post tax deductions if
    # requested by the user
    if form.pre_deduction_add.data:
        form.pre_deductions.append_entry()
    if form.post_deduction_add.data:
        form.post_deductions.append_entry()

    if form.validate_on_submit():
        entry = Entry.query.filter_by(id = entry_id).first()
        entry_info = {
            'year' : year,
            'frequency': frequency,
            'status': status
        }
        # Capture user paycheck as int
        earnings = int(form.paycheck.earnings.data * 100)
        
        # Capture user allowances as dictionar where each key is corresponds to
        # allowance "level"
        user_allowances = {allowance['level_id']: allowance['num'] 
                           for allowance in form.paycheck.allowances.data }

        # Group user deductions by type
        deductions = {}
        deductions['pre'] = { 'deferred' : sum([int(l['d_amount'] * 100) 
                                                for l in form.pre_deductions.data if l['d_deferred'] == 'yes']),
                              'not_deferred' : sum([int(l['d_amount'] * 100) 
                                                    for l in form.pre_deductions.data if l['d_deferred'] == 'no']),
                              'all' : sum([int(l['d_amount'] * 100) 
                                           for l in form.pre_deductions.data]),
        }
        deductions['post'] = { 'all' : sum([int(l['d_amount'] * 100) 
                                            for l in form.post_deductions.data])    
        }
        deductions['all'] = deductions['pre']['all'] + deductions['post']['all']

        # Calculate all information based for entry based on user input
        calcs = entry.calculate(earnings, deductions, s, user_allowances)

        user_info = { 'allowances' : user_allowances,
                      'earnings' : earnings,
                      'deductions' : deductions,
                      'calcs' : calcs,
                      'entry' : entry_info
        }
        
        return render_template('calculate.html',
                               title='calculate',
                               form=form,
                               info=user_info)
    else:
        return render_template('calculate.html',
                               title='calculate',
                               form=form,
                               info=None)

@app.route('/table/<year>/<frequency>/<status>', methods=['GET'])
def table(year, frequency, status):
    entry = Entry.query \
                .join(Year).filter_by(year = year) \
                .join(Frequency).filter_by(frequency = frequency) \
                .first()
    if entry:
        return render_template('table.html',
                               title='table',
                               entry=entry)
    else: 
        flash('Entry Not Found')
        return redirect('/begin')


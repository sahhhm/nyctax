from app import db
from decimal import Decimal
from sqlalchemy import and_

class Frequency(db.Model):
    __tablename__ = 'frequency'
    id = db.Column(db.Integer, primary_key=True)
    frequency = db.Column(db.String(20), unique=True)

    def __repr__(self):
        return '<Frequency %r>' % (self.frequency)

    @staticmethod
    def get_frequency():
        """ Used in forms.py to populate SelectField """
        f = Frequency.query
        return f


class Status(db.Model):
    __tablename__ = 'status'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20), unique=True)

    def __repr__(self):
        return '<Status %r>' % (self.status)

    @staticmethod
    def get_status():
        """ Used in forms.py to populate SelectField """
        s = Status.query
        return s

class Level(db.Model):
    __tablename__ = 'level'
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.String(20), unique=True)

    def __repr__(self):
        return '<Status %r>' % (self.level)
    def title(self):
        return str(self.level)

class Year(db.Model):
    __tablename__ = 'year'
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, unique=True)

    medicare = db.relationship("Medicare", uselist=False)
    social_security = db.relationship("SocialSecurity", uselist=False)

    def __repr__(self):
        return '<Year %r>' % (self.year)

    @staticmethod
    def get_year():
        """ Used in forms.py to populate SelectField """
        y = Year.query
        return y

class Entry(db.Model):
    __tablename__ = 'entry'
    id = db.Column(db.Integer, primary_key=True)

    frequency_id = db.Column(db.Integer, db.ForeignKey('frequency.id'), nullable=False)
    frequency = db.relationship("Frequency")

    year_id = db.Column(db.Integer, db.ForeignKey('year.id'), nullable=False)
    year = db.relationship("Year")
    
    withholdings = db.relationship("Withholding", backref="entry", lazy="dynamic")

    __table_args__ = (db.UniqueConstraint('year_id', 
                                          'frequency_id', 
                                          name='_year_frequency_uc'),)

    def __repr__(self):
        return '<Entry %r - (%r)>' % (self.year.year, self.frequency.frequency)

    def calculate(self, earnings, deductions, status, allowances):
        wages = self.calculate_wages(earnings, deductions)
        taxes = self.calculate_taxes(wages, status, allowances)
        pay = self.calculate_pay(wages, deductions, taxes)
        return { "wages" : wages,
                 "taxes" : taxes,
                 "pay" : pay}

    def calculate_wages(self, earnings, deductions):
        # Dictionary of wages
        wages = {}
        
        # Normal earnings as entered by user
        wages['total_wages']  = {
            "name" : "Total Wages",
            "amount" : earnings
        }

        # Federal Taxable Wages (including deferred)
        wages['taxable_wages_w_d'] = {
            "name" : "Federal Taxable Wages (including deferred)",
            "amount" : earnings - deductions['pre']['all']
        }

        # Taxable Wages (excluding deferred)
        wages['taxable_wages_wo_d'] = {
            "name" : "Federal Taxable Wages (including deferred)",
            "amount" : earnings - deductions['pre']['not_deferred']
        }
        return wages

    def calculate_taxes(self, wages, status, allowances):
        taxable_w_deferred = wages['taxable_wages_w_d']['amount']
        taxable_wo_deferred = wages['taxable_wages_wo_d']['amount']

        # List of dictionaries consisting of various taxes
        taxes = {}

        # Entry containing all calculated taxes 
        taxes['all'] = {
            "name"  : "All Taxes",
            "amount":  0
        }
        
        # Social security tax - need to divide by 10000 because we are
        # multiplying by a percent
        taxes['social'] = {
            "name"  : "Social Security",
            "amount":  (self.year.social_security.tax_rate *
                        taxable_wo_deferred) / 10000
        }
        taxes['all']['amount'] += taxes['social']['amount']

        # Medicare tax - need to divide by 10000 because we are multiplying by a
        # percent
        taxes['medicare'] = {
            "name"  : "Medicare",
            "amount": (self.year.medicare.tax_rate *
                       taxable_wo_deferred) / 10000
        }
        taxes['all']['amount'] += taxes['medicare']['amount']

        # Withholding tax on all applicable levels. Number of allowances as
        # entered by the user is passed as dictionary where each key represents
        # the level id
        withholdings = self.withholdings.filter(and_(Withholding.status == status,
                                                     Withholding.at_least <= taxable_w_deferred,
                                                     Withholding.but_less_than > taxable_w_deferred))

        for w in withholdings.all():
            taxes[w.level.level] = {
                "name"   : w.level.level,
                "amount" : w.calculate_withholding(taxable_w_deferred,
                                                   allowances[w.level.id])

            }
            taxes['all']['amount'] += taxes[w.level.level]['amount']
        return taxes

    def calculate_pay(self, wages, deductions, taxes):
        pay = {} 
        pay['net'] = {
            "name" : "Net Pay",
            "amount" : wages['total_wages']['amount'] - deductions['all'] -
                       taxes['all']['amount']
        }
        return pay
        
class Medicare(db.Model):
    __tablename__ = 'medicare'
    id = db.Column(db.Integer, primary_key=True)
    tax_rate = db.Column(db.Integer, nullable=False)
    year_id = db.Column(db.Integer, db.ForeignKey('year.id'))

    def __repr__(self):
        return '<Medicare $%r>' % (self.tax_rate)

class SocialSecurity(db.Model):
    __tablename__ = 'socialsecurity'
    id = db.Column(db.Integer, primary_key=True)
    tax_rate = db.Column(db.Integer, nullable=False)
    wage_limit = db.Column(db.Integer, nullable=False)
    year_id = db.Column(db.Integer, db.ForeignKey('year.id'))

    def __repr__(self):
        return '<Social Security $%r>' % (self.tax_rate)

class Allowance(db.Model):
    __tablename__ = 'allowance'

    id = db.Column(db.Integer, primary_key=True)
    deduction_allowance = db.Column(db.Integer, nullable=False)
    exemption_allowance = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Allowance $%r>' % (self.exemption_allowance)

class Withholding(db.Model):
    __tablename__ = 'withholding'
    id = db.Column(db.Integer, primary_key=True)
    
    allowance_id = db.Column(db.Integer, db.ForeignKey('allowance.id'))
    allowance = db.relationship("Allowance")

    at_least = db.Column(db.Integer, index=True, nullable=False)
    but_less_than = db.Column(db.Integer, index=True, nullable=False)
    amount_subtract = db.Column(db.Integer, nullable=False)
    amount_multiply = db.Column(db.Integer, nullable=False)
    amount_add = db.Column(db.Integer, nullable=False)

    entry_id = db.Column(db.Integer, db.ForeignKey('entry.id'))

    status_id = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False)
    status = db.relationship("Status")

    level_id = db.Column(db.Integer, db.ForeignKey('level.id'), nullable=False, index=True)
    level = db.relationship("Level")

    def __repr__(self):
        return '< Withholding for%r- %r over %r>' % (self.level.level,
                                                     self.status.status,
                                                     self.at_least)

    def calculate_withholding(self, wage, num_allowances):
        wage = wage - self.allowance.deduction_allowance - \
                     (self.allowance.exemption_allowance * num_allowances)
        mult = Decimal(self.amount_multiply) / 10000
        return int(round((wage - self.amount_subtract) * mult, 0)) + self.amount_add


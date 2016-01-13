import jinja2
import flask
import decimal
import locale

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8') 

blueprint = flask.Blueprint('filters', __name__)

@jinja2.contextfilter
@blueprint.app_template_filter()
def to_currency(context, value):
    return locale.currency(decimal.Decimal(value) / 100)

@jinja2.contextfilter
@blueprint.app_template_filter()
def to_currency_via_percent(context, value):
    return locale.currency(round(decimal.Decimal(value) / 1000000, 2))


@jinja2.contextfilter
@blueprint.app_template_filter()
def to_percent(context, value):
    return "{0}%".format(decimal.Decimal(value) / 100)

@jinja2.contextfilter
@blueprint.app_template_filter()
def to_thousandth(context, value):
    return decimal.Decimal(value) / 10000


#!venv/bin/python
from app import db, models
import sys

status_single = models.Status(status="SINGLE")
status_married = models.Status(status="MARRIED")
db.session.add(status_single)
db.session.add(status_married)
db.session.commit()

level_federal = models.Level(level="FEDERAL")
level_state = models.Level(level="STATE")
level_city = models.Level(level="CITY")
db.session.add(level_federal)
db.session.add(level_state)
db.session.add(level_city)
db.session.commit()



freq_weekly = models.Frequency(frequency="WEEKLY")
freq_biweekly = models.Frequency(frequency="BIWEEKLY")
freq_semimonthly = models.Frequency(frequency="SEMIMONTHLY")
db.session.add(freq_weekly)
db.session.add(freq_biweekly)
db.session.add(freq_semimonthly)
db.session.commit()

year_2015 = models.Year(year=2015)
medicare_2015 = models.Medicare(tax_rate=145)
year_2015.medicare = medicare_2015
social_security_2015 = models.SocialSecurity(tax_rate=620, wage_limit=11850000)
year_2015.social_security = social_security_2015
db.session.add(year_2015)
db.session.commit()

## 2015 Biweekly ##
entry1 = models.Entry(frequency=freq_biweekly, year=year_2015)
"""
fw1a = models.FederalWithholding(entry_id = entry1.id,
                                 status = status_single,
                                 over = 0000,
                                 but_not_over = 8800,
                                 withhold_amount = 0,
                                 withhold_percentage = 0,
                                 withhold_excess = 0000)

fw1b = models.FederalWithholding(entry_id = entry1.id,
                                 status = status_single,
                                 over = 8800,
                                 but_not_over = 44300,
                                 withhold_amount = 000,
                                 withhold_percentage = 1000,
                                 withhold_excess = 8800)
fw1c = models.FederalWithholding(entry_id = entry1.id,
                                 status = status_single,
                                 over = 44300,
                                 but_not_over = 152900,
                                 withhold_amount = 3550,
                                 withhold_percentage = 1500,
                                 withhold_excess = 44300)
fw1d = models.FederalWithholding(entry_id = entry1.id,
                                 status = status_single,
                                 over = 152900,
                                 but_not_over = 357900,
                                 withhold_amount = 19840,
                                 withhold_percentage = 2500,
                                 withhold_excess = 152900)
fw1e = models.FederalWithholding(entry_id = entry1.id,
                                 status = status_single,
                                 over = 357900,
                                 but_not_over = 736900,
                                 withhold_amount = 71090,
                                 withhold_percentage = 2800,
                                 withhold_excess = 357900)
fw1f = models.FederalWithholding(entry_id = entry1.id,
                                 status = status_single,
                                 over = 736900,
                                 but_not_over = 1591500,
                                 withhold_amount = 177210,
                                 withhold_percentage = 3300,
                                 withhold_excess = 736900)
fw1g = models.FederalWithholding(entry_id = entry1.id,
                                 status = status_single,
                                 over = 1591500,
                                 but_not_over = 1598100,
                                 withhold_amount = 459228,
                                 withhold_percentage = 3500,
                                 withhold_excess = 1591500)
fw1h = models.FederalWithholding(entry_id = entry1.id,
                                 status = status_single,
                                 over = 1598100,
                                 but_not_over = sys.maxint,
                                 withhold_amount = 461539,
                                 withhold_percentage = 3960,
                                 withhold_excess = 1598100)

entry1.federal_withholdings = [fw1a, fw1b, fw1c, fw1d, fw1e, fw1f, fw1g, fw1h]
"""
entry1_fa_single = models.Allowance(
                                    deduction_allowance = 0,
                                    exemption_allowance = 15380)
entry1_fa_married = models.Allowance(
                                     deduction_allowance = 0,
                                     exemption_allowance = 15380)
entry1_sa_single = models.Allowance(
                                    deduction_allowance = 28270,
                                    exemption_allowance = 3850)
entry1_sa_married = models.Allowance(
                                     deduction_allowance = 30190,
                                     exemption_allowance = 3850)
entry1_ca_single = models.Allowance(
                                    deduction_allowance = 19230,
                                    exemption_allowance = 3850)
entry1_ca_married = models.Allowance(
                                     deduction_allowance = 21150,
                                     exemption_allowance = 3850)

entry1.allowances = [entry1_fa_single,
                     entry1_fa_married,
                     entry1_sa_single,
                     entry1_sa_married,
                     entry1_ca_single,
                     entry1_ca_married]


db.session.add(entry1)
db.session.commit()


## 2015 Semimonthly ##
semimonthly_2015 = models.Entry(frequency=freq_semimonthly, year=year_2015)

semimonthly_2015_fa_all = models.Allowance(
                                              deduction_allowance = 0,
                                              exemption_allowance = 16670)

semimonthly_2015_sa_single = models.Allowance( 
                                              deduction_allowance = 30625,
                                              exemption_allowance = 4165)
semimonthly_2015_sa_married = models.Allowance(
                                               deduction_allowance = 32710,
                                               exemption_allowance = 4165)
semimonthly_2015_ca_single = models.Allowance( 
                                              deduction_allowance = 20835,
                                              exemption_allowance = 4165)
semimonthly_2015_ca_married = models.Allowance(
                                               deduction_allowance = 22915,
                                               exemption_allowance = 4165)

db.session.add(semimonthly_2015_fa_all)
db.session.add(semimonthly_2015_sa_single)
db.session.add(semimonthly_2015_sa_married)
db.session.add(semimonthly_2015_ca_single)
db.session.add(semimonthly_2015_ca_married)

semimonthly_2015_sw1 = models.Withholding(entry_id = semimonthly_2015.id,
                                          allowance = semimonthly_2015_sa_single,
                                          level = level_state,
                                          status = status_single,
                                          at_least = 0000,
                                          but_less_than = 35000,
                                          amount_subtract = 0,
                                          amount_multiply = 400,
                                          amount_add = 0000)

semimonthly_2015_sw2 = models.Withholding(entry_id = semimonthly_2015.id,
                                          allowance = semimonthly_2015_sa_single,
                                          level = level_state,
                                          status = status_single,
                                          at_least = 35000,
                                          but_less_than = 48300,
                                          amount_subtract = 35000,
                                          amount_multiply = 450,
                                          amount_add = 1400)

semimonthly_2015_sw3 = models.Withholding(entry_id = semimonthly_2015.id,
                                          allowance = semimonthly_2015_sa_single,
                                          level = level_state,
                                          status = status_single,
                                          at_least = 48300,
                                          but_less_than = 57300,
                                          amount_subtract = 48300,
                                          amount_multiply = 525,
                                          amount_add = 2000)

semimonthly_2015_sw4 = models.Withholding(entry_id = semimonthly_2015.id,
                                          allowance = semimonthly_2015_sa_single,
                                          level = level_state,
                                          status = status_single,
                                          at_least = 57300,
                                          but_less_than = 88100,
                                          amount_subtract = 57300,
                                          amount_multiply = 590,
                                          amount_add = 2471)

semimonthly_2015_sw5 = models.Withholding(entry_id = semimonthly_2015.id,
                                          allowance = semimonthly_2015_sa_single,
                                          level = level_state,
                                          status = status_single,
                                          at_least = 88100,
                                          but_less_than = 331700,
                                          amount_subtract = 88100,
                                          amount_multiply = 645,
                                          amount_add = 4288)

semimonthly_2015_sw6 = models.Withholding(entry_id = semimonthly_2015.id,
                                          allowance = semimonthly_2015_sa_single,
                                          level = level_state,
                                          status = status_single,
                                          at_least = 331700,
                                          but_less_than = 398100,
                                          amount_subtract = 331700,
                                          amount_multiply = 665,
                                          amount_add = 20000)

semimonthly_2015_sw7 = models.Withholding(entry_id = semimonthly_2015.id,
                                          allowance = semimonthly_2015_sa_single,
                                          level = level_state,
                                          status = status_single,
                                          at_least = 398100,
                                          but_less_than = 442500,
                                          amount_subtract = 398100,
                                          amount_multiply = 758,
                                          amount_add = 24417)

semimonthly_2015_sw8 = models.Withholding(entry_id = semimonthly_2015.id,
                                          allowance = semimonthly_2015_sa_single,
                                          level = level_state,
                                          status = status_single,
                                          at_least = 442500,
                                          but_less_than = 664000,
                                          amount_subtract = 442500,
                                          amount_multiply = 808,
                                          amount_add = 27779)

semimonthly_2015_sw9 = models.Withholding(entry_id = semimonthly_2015.id,
                                          allowance = semimonthly_2015_sa_single,
                                          level = level_state,
                                          status = status_single,
                                          at_least = 664000,
                                          but_less_than = 885400,
                                          amount_subtract = 664000,
                                          amount_multiply = 715,
                                          amount_add = 45675)

semimonthly_2015_sw10 = models.Withholding(entry_id = semimonthly_2015.id,
                                           allowance = semimonthly_2015_sa_single,
                                           level = level_state,
                                           status = status_single,
                                           at_least = 885400,
                                           but_less_than = 1106700,
                                           amount_subtract = 885400,
                                           amount_multiply = 815,
                                           amount_add = 61508)

semimonthly_2015_sw11 = models.Withholding(entry_id = semimonthly_2015.id,
                                           allowance = semimonthly_2015_sa_single,
                                           level = level_state,
                                           status = status_single,
                                           at_least = 1106700,
                                           but_less_than = 4427700,
                                           amount_subtract = 1106700,
                                           amount_multiply = 735,
                                           amount_add = 79542)

semimonthly_2015_sw12 = models.Withholding(entry_id = semimonthly_2015.id,
                                           allowance = semimonthly_2015_sa_single,
                                           level = level_state,
                                           status = status_single,
                                           at_least = 4427700,
                                           but_less_than = 4649400,
                                           amount_subtract = 4427700,
                                           amount_multiply = 4902,
                                           amount_add = 323638)

semimonthly_2015_sw13 = models.Withholding(entry_id = semimonthly_2015.id,
                                           allowance = semimonthly_2015_sa_single,
                                           level = level_state,
                                           status = status_single,
                                           at_least = 4649400,
                                           but_less_than = sys.maxint,
                                           amount_subtract = 469400,
                                           amount_multiply = 962,
                                           amount_add = 432300)


semimonthly_2015_cw1 = models.Withholding(entry_id = semimonthly_2015.id,
                                          allowance = semimonthly_2015_ca_single,
                                          level = level_city,
                                          status = status_single,
                                          at_least = 0000,
                                          but_less_than = 33300,
                                          amount_subtract = 0000,
                                          amount_multiply = 190,
                                          amount_add = 0000)

semimonthly_2015_cw2 = models.Withholding(entry_id = semimonthly_2015.id,
                                          allowance = semimonthly_2015_ca_single,
                                          level = level_city,
                                          status = status_single,
                                          at_least = 33300,
                                          but_less_than = 36200,
                                          amount_subtract = 33300,
                                          amount_multiply = 265,
                                          amount_add = 633)

semimonthly_2015_cw3 = models.Withholding(entry_id = semimonthly_2015.id,
                                          allowance = semimonthly_2015_ca_single,
                                          level = level_city,
                                          status = status_single,
                                          at_least = 36200,
                                          but_less_than = 62500,
                                          amount_subtract = 36200,
                                          amount_multiply = 310,
                                          amount_add = 713)

semimonthly_2015_cw4 = models.Withholding(entry_id = semimonthly_2015.id,
                                          allowance = semimonthly_2015_ca_single,
                                          level = level_city,
                                          status = status_single,
                                          at_least = 62500,
                                          but_less_than = 104200,
                                          amount_subtract = 62500,
                                          amount_multiply = 370,
                                          amount_add = 1525)

semimonthly_2015_cw5 = models.Withholding(entry_id = semimonthly_2015.id,
                                          allowance = semimonthly_2015_ca_single,
                                          level = level_city,
                                          status = status_single,
                                          at_least = 104200,
                                          but_less_than = 250000,
                                          amount_subtract = 104200,
                                          amount_multiply = 390,
                                          amount_add = 3067)

semimonthly_2015_cw6 = models.Withholding(entry_id = semimonthly_2015.id,
                                          allowance = semimonthly_2015_ca_single,
                                          level = level_city,
                                          status = status_single,
                                          at_least = 250000,
                                          but_less_than = 2083300,
                                          amount_subtract = 250000,
                                          amount_multiply = 400,
                                          amount_add = 8754)

semimonthly_2015_cw7 = models.Withholding(entry_id = semimonthly_2015.id,
                                          allowance = semimonthly_2015_ca_single,
                                          level = level_city,
                                          status = status_single,
                                          at_least = 2083300,
                                          but_less_than = sys.maxint,
                                          amount_subtract = 2083300,
                                          amount_multiply = 425,
                                          amount_add = 90182)

semimonthly_2015_fw1 = models.Withholding(entry_id = semimonthly_2015.id,
                                          allowance = semimonthly_2015_fa_all,
                                          level = level_federal,
                                          status = status_single,
                                          at_least = 0000,
                                          but_less_than = 9600,
                                          amount_add = 0,
                                          amount_multiply = 0,
                                          amount_subtract = 0000)
semimonthly_2015_fw2 = models.Withholding(entry_id = semimonthly_2015.id,
                                          allowance = semimonthly_2015_fa_all,
                                          level = level_federal,
                                          status = status_single,
                                          at_least = 9600,
                                          but_less_than = 48000,
                                          amount_add = 0,
                                          amount_multiply = 1000,
                                          amount_subtract = 9600)
semimonthly_2015_fw3 = models.Withholding(entry_id = semimonthly_2015.id,
                                          allowance = semimonthly_2015_fa_all,
                                          level = level_federal,
                                          status = status_single,
                                          at_least = 48000,
                                          but_less_than = 165600,
                                          amount_add = 3840,
                                          amount_multiply = 1500,
                                          amount_subtract = 48000)
semimonthly_2015_fw4 = models.Withholding(entry_id = semimonthly_2015.id,
                                          allowance = semimonthly_2015_fa_all,
                                          level = level_federal,
                                          status = status_single,
                                          at_least = 165600,
                                          but_less_than = 387700,
                                          amount_add = 21480,
                                          amount_multiply = 2500,
                                          amount_subtract = 165600)
semimonthly_2015_fw5 = models.Withholding(entry_id = semimonthly_2015.id,
                                          allowance = semimonthly_2015_fa_all,
                                          level = level_federal,
                                          status = status_single,
                                          at_least = 387700,
                                          but_less_than = 798300,
                                          amount_add = 77005,
                                          amount_multiply = 2800,
                                          amount_subtract = 387700)
semimonthly_2015_fw6 = models.Withholding(entry_id = semimonthly_2015.id,
                                          allowance = semimonthly_2015_fa_all,
                                          level = level_federal,
                                          status = status_single,
                                          at_least = 798300,
                                          but_less_than = 1724200,
                                          amount_add =191973,
                                          amount_multiply = 3300,
                                          amount_subtract = 798300)
semimonthly_2015_fw7 = models.Withholding(entry_id = semimonthly_2015.id,
                                          allowance = semimonthly_2015_fa_all,
                                          level = level_federal,
                                          status = status_single,
                                          at_least = 1724200,
                                          but_less_than = 1731300,
                                          amount_add = 497520,
                                          amount_multiply = 3500,
                                          amount_subtract = 1724200)
semimonthly_2015_fw8 = models.Withholding(entry_id = semimonthly_2015.id,
                                          allowance = semimonthly_2015_fa_all,
                                          level = level_federal,
                                          status = status_single,
                                          at_least = 1731300,
                                          but_less_than = sys.maxint,
                                          amount_add = 500005,
                                          amount_multiply = 3560,
                                          amount_subtract = 1731300)

semimonthly_2015.withholdings = [semimonthly_2015_fw1,
                                 semimonthly_2015_fw2,
                                 semimonthly_2015_fw3,
                                 semimonthly_2015_fw4,
                                 semimonthly_2015_fw5,
                                 semimonthly_2015_fw6,
                                 semimonthly_2015_fw7,
                                 semimonthly_2015_fw8,
                                 semimonthly_2015_sw1,
                                 semimonthly_2015_sw2,
                                 semimonthly_2015_sw3,
                                 semimonthly_2015_sw4,
                                 semimonthly_2015_sw5,
                                 semimonthly_2015_sw6,
                                 semimonthly_2015_sw7,
                                 semimonthly_2015_sw8,
                                 semimonthly_2015_sw9,
                                 semimonthly_2015_sw10,
                                 semimonthly_2015_sw11,
                                 semimonthly_2015_sw12,
                                 semimonthly_2015_sw13,
                                 semimonthly_2015_cw1,
                                 semimonthly_2015_cw2,
                                 semimonthly_2015_cw3,
                                 semimonthly_2015_cw4,
                                 semimonthly_2015_cw5,
                                 semimonthly_2015_cw6,
                                 semimonthly_2015_cw7]

db.session.add(semimonthly_2015)
db.session.commit()



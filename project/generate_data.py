import random
from random import choice
import sys
import os
from collections import Counter
import pandas as pd
from random import shuffle

doctor_name_list = []
with open(r"C:\Users\admin\Desktop\3170_data\doctor_name.txt","r") as f:
    for line in f:
        doctor_name_list.append(line[:-1])

#print(doctor_name_list)

random_gender_list = ["male","female"]
random_type_list = ["doctor","nurse"]
random_first_part_phone = ["139","183","188","138","131","187","136","190","175","176"]
random_insurance = ["True","False"]
random_doctor_salary = []
random_nurse_salary = []
nurse_salary_base = 4000
while nurse_salary_base != 10000:
    nurse_salary_base += 1000
    random_nurse_salary.append(nurse_salary_base)
doctor_salary_base = 10000
while doctor_salary_base != 50000:
    doctor_salary_base += 1000
    random_doctor_salary.append(doctor_salary_base)

#print(random_salary)

depart_name_list = []
doctor_id_list = []
doctor_dept_list = []
type_list = []
gender_list = []
phone_list = []
salary_list = []



with open(r"C:\Users\admin\Desktop\3170_data\dept_name.txt","r") as f:
    for line in f:
        depart_name_list.append(line[:-12])
#print(depart_name_list)
for i in range(1000):
    phone = ""
    while True:
        str = "1"
        for j in range(5):
            ch = chr(random.randrange(ord('0'),ord('9') + 1))
            str += ch
        if str in doctor_id_list:
            continue
        else:
            doctor_id_list.append(str)
            break
    random_type = choice(random_type_list)
    random_gender = choice(random_gender_list)
    gender_list.append(random_gender)
    type_list.append(random_type)
    random_fisrt = choice(random_first_part_phone)
    phone += random_fisrt
    random_dept = choice(depart_name_list)
    doctor_dept_list.append(random_dept)
    for j in range(8):
        ch = chr(random.randrange(ord('0'),ord('9') + 1))
        phone += ch
    phone_list.append(phone)
    if random_type == "nurse":
        random_salary = choice(random_nurse_salary)
        salary_list.append(random_salary)
    else:
        random_salary = choice(random_doctor_salary)
        salary_list.append(random_salary)
#print(doctor_id_list)
#print(len(doctor_dept_list))
#print(len(doctor_id_list))
#print(len(patient_id_list))
#print(len(type_list))
#print(len(gender_list))
#print(len(phone_list))
#print(len(type_list))
#print(len(salary_list))


column_list = ["doctor_id","name","dep_name","gender","type","phone","salary"]
total_list = []
#print(doctor_dept_list)
for i in range(1000):
    new_list = [doctor_id_list[i],doctor_name_list[i],doctor_dept_list[i],gender_list[i],type_list[i],phone_list[i],salary_list[i]]
    total_list.append(new_list)

doctor = pd.DataFrame(columns=column_list,data=total_list)
doctor.to_csv(r"C:\Users\admin\Desktop\3170_data\doctor.csv",encoding='utf-8')

dept_phone_list = []
for i in range(20):
    phone_number = "1"
    for j in range(6):
        ch = chr(random.randrange(ord('0'),ord('9') + 1))
        phone_number += ch
    dept_phone_list.append(phone_number)

dept_column_list = ["dept_name","dept_phone"]
dept_total_list = []
for i in range(20):
    new_list = [depart_name_list[i],dept_phone_list[i]]
    dept_total_list.append(new_list)
dept = pd.DataFrame(columns=dept_column_list,data=dept_total_list)
dept.to_csv(r"C:\Users\admin\Desktop\3170_data\dept.csv",encoding='utf-8')

patient_id_list = []
patient_name_list = []
patient_phone_list = []
patient_gender_list = []
medi_insurance_list = []

for i in range(10000):
    while True:
        str = "1"
        for j in range(9):
            ch = chr(random.randrange(ord('0'),ord('9') + 1))
            str += ch
        if str in patient_id_list:
            continue
        else:
            patient_id_list.append(str)
            break
    phone = ""
    random_fisrt = choice(random_first_part_phone)
    phone += random_fisrt
    for j in range(8):
        ch = chr(random.randrange(ord('0'),ord('9') + 1))
        phone += ch
    patient_phone_list.append(phone)
    random_gender = choice(random_gender_list)
    patient_gender_list.append(random_gender)
    insurance = choice(random_insurance)
    medi_insurance_list.append(insurance)
with open(r"C:\Users\admin\Desktop\3170_data\patient_name.txt","r") as f:
    for line in f:
        patient_name_list.append(line[:-1])
#print(len(patient_name_list))
patient_column_list = ["patient_id","patient_name","patient_phone","patient_gender","medi_insurance"]
patient_total_list = []
for i in range(10000):
    new_list = [patient_id_list[i],patient_name_list[i],patient_phone_list[i],patient_gender_list[i],medi_insurance_list[i]]
    patient_total_list.append(new_list)
patient = pd.DataFrame(columns=patient_column_list,data=patient_total_list)
patient.to_csv(r"C:\Users\admin\Desktop\3170_data\patient.csv",encoding='utf-8')

treat_id_list = []
treat_date_list = []
treat_doctor_id_list = []
treat_patient_id_list = []
treat_date_list = []
treat_describe_list = []

random_month_list = []
for i in range(1,13):
    random_month_list.append(i)
random_day_list = []
for i in range(1,28):
    random_day_list.append(i)

random_treat_describ_list = []
with open(r"C:\Users\admin\Desktop\3170_data\describe.txt","r") as f:
    for line in f:
        random_treat_describ_list.append(line[:-1])

random_number_list = [1,2,3,4]



for i in range(20000):
    while True:
        str = "1"
        for j in range(9):
            ch = chr(random.randrange(ord('0'),ord('9') + 1))
            str += ch
        if str in treat_id_list:
            continue
        else:
            treat_id_list.append(str)
            break
    treat_doctor = choice(doctor_id_list)
    treat_doctor_id_list.append(treat_doctor)
    if i < 10000:
        treat_patient_id_list.append(patient_id_list[i])
    else:
        treat_patient = choice(patient_id_list)
        treat_patient_id_list.append(treat_patient)
    month = choice(random_month_list)
    day = choice(random_day_list)

    date = "2019.%d.%d"%(month,day)
    treat_date_list.append(date)

    number = choice(random_number_list)
    temp_list = []
    for i in range(number):
        while True:
            describe = choice(random_treat_describ_list)
            if describe in temp_list:
                continue
            else:
                temp_list.append(describe)
                break
    describe_string = " ".join(temp_list)
    treat_describe_list.append(describe_string)
shuffle(treat_patient_id_list)

treat_column_list = ["treat_id","doctor_id","patient_id","date","describe"]
treat_total_list = []
for i in range(20000):
    new_list = [treat_id_list[i],treat_doctor_id_list[i],treat_patient_id_list[i],treat_date_list[i],treat_describe_list[i]]
    treat_total_list.append(new_list)
treat = pd.DataFrame(columns=treat_column_list,data=treat_total_list)
treat.to_csv(r"C:\Users\admin\Desktop\3170_data\treat.csv",encoding='utf-8')

random_bed_type = ["normal","normal","normal","normal","ICU"]
random_bed_status = ["available","occupied","occupied","occupied","occupied"]
random_days_list = []
for i in range(1,61):
    random_days_list.append(i)

bed_id_list = []
bed_type_list = []
bed_status_list = []
bed_treat_list = []
bed_days_list = []

for i in range(1000):
    while True:
        str = "1"
        for j in range(4):
            ch = chr(random.randrange(ord('0'),ord('9') + 1))
            str += ch
        if str in bed_id_list:
            continue
        else:
            bed_id_list.append(str)
            break
    bed_type = choice(random_bed_type)
    bed_type_list.append(bed_type)
    bed_status = choice(random_bed_status)
    bed_status_list.append(bed_status)
    if bed_status == "occupied":
        bed_treat_id = choice(treat_id_list)
        bed_days = choice(random_days_list)
        bed_treat_list.append(bed_treat_id)
        bed_days_list.append(bed_days)
    else:
        bed_treat_id = None
        bed_days = None
        bed_treat_list.append(bed_treat_id)
        bed_days_list.append(bed_days)
bed_column_list = ["bed_id","bed_type","bed_status","treat_id","days_in_bed"]
bed_total_list = []
for i in range(1000):
    new_list = [bed_id_list[i],bed_type_list[i],bed_status_list[i],bed_treat_list[i],bed_days_list[i]]
    bed_total_list.append(new_list)
bed = pd.DataFrame(columns=bed_column_list,data=bed_total_list)
bed.to_csv(r"C:\Users\admin\Desktop\3170_data\bed.csv",encoding='utf-8')

equipment_level_1_list = []
equipment_level_10_list = []

with open(r"C:\Users\admin\Desktop\3170_data\equip_1.txt","r") as f:
    for line in f:
        equipment_level_1_list.append(line[:-1])

with open(r"C:\Users\admin\Desktop\3170_data\equip_10.txt","r") as f:
    for line in f:
        equipment_level_10_list.append(line[:-1])

equipment_id_list = []
equipment_name_list = []
equipment_check_date = []

for i in range(205):
    while True:
        str = "1"
        for j in range(4):
            ch = chr(random.randrange(ord('0'),ord('9') + 1))
            str += ch
        if str in equipment_id_list:
            continue
        else:
            equipment_id_list.append(str)
            break
    if i <= 54:
        index = int(i / 5)
        equipment_name = equipment_level_1_list[index]
        equipment_name_list.append(equipment_name)
    else:
        index = int((i - 55) / 50)
        equipment_name = equipment_level_10_list[index]
        equipment_name_list.append(equipment_name)
    check_month = choice(random_month_list)
    check_day = choice(random_day_list)
    chekc_date = "2019.%d.%d"%(check_month,check_day)
    equipment_check_date.append(chekc_date)

equip_column_list = ["equip_id","equip_name","last_check_date"]
equip_total_list = []
for i in range(205):
    new_list = [equipment_id_list[i],equipment_name_list[i],equipment_check_date[i]]
    equip_total_list.append(new_list)
equip = pd.DataFrame(columns=equip_column_list,data=equip_total_list)
equip.to_csv(r"C:\Users\admin\Desktop\3170_data\equip.csv",encoding='utf-8')

equip_cost_1_list = []
equip_cost_10_list = []
for i in range(11):
    cost = random.randint(50,100)
    new_cost = int(cost*1000)
    equip_cost_1_list.append(new_cost)
for i in range(3):
    cost = random.randint(50,100)
    new_cost = int(cost*100)
    equip_cost_10_list.append(new_cost)
equip_purchase_date_list = []
equip_purchase_cost_list = []

for i in range(205):
    purchase_month = choice(random_month_list)
    purchase_day = choice(random_day_list)
    purchase_date = "2018.%d.%d"%(purchase_month,purchase_day)
    equip_purchase_date_list.append(purchase_date)
    if i <= 54:
        index = int(i / 5)
        equip_purchase_cost = equip_cost_1_list[index]
        equip_purchase_cost_list.append(equip_purchase_cost)
    else:
        index = int((i - 55) / 50)
        equip_purchase_cost = equip_cost_10_list[index]
        equip_purchase_cost_list.append(equip_purchase_cost)

equip_purchase_column_list = ["equip_id","purchase_date","purchase_cost"]
equip_purchase_total_list = []
for i in range(205):
    new_list = [equipment_id_list[i],equip_purchase_date_list[i],equip_purchase_cost_list[i]]
    equip_purchase_total_list.append(new_list)
equip_purchase = pd.DataFrame(columns=equip_purchase_column_list,data=equip_purchase_total_list)
equip_purchase.to_csv(r"C:\Users\admin\Desktop\3170_data\equip_purchase.csv",encoding='utf-8')

treat_program_id_list = []
treat_treat_id_list = []
treat_equip_id_list = []
treat_program_cost_list = []


for i in range(10000):
    while True:
        str = "1"
        for j in range(7):
            ch = chr(random.randrange(ord('0'),ord('9') + 1))
            str += ch
        if str in treat_program_id_list:
            continue
        else:
            treat_program_id_list.append(str)
            break
    treat_treat_id = choice(treat_id_list)
    treat_equip_id = choice(equipment_id_list)
    treat_treat_id_list.append(treat_treat_id)
    treat_equip_id_list.append(treat_equip_id)
    program_cost = random.randint(100,1000)
    treat_program_cost_list.append(program_cost)
treat_program_column_list = ["program_id","treat_id","equip_id","program_cost"]
treat_program_total_list = []
for i in range(10000):
    new_list = [treat_program_id_list[i],treat_treat_id_list[i],treat_equip_id_list[i],treat_program_cost_list[i]]
    treat_program_total_list.append(new_list)
treat_program = pd.DataFrame(columns=treat_program_column_list,data=treat_program_total_list)
treat_program.to_csv(r"C:\Users\admin\Desktop\3170_data\treat_program.csv",encoding='utf-8')


finance_month_list = []
finance_income_list = []
finance_expense_list = []
finance_profit_list = []
for i in range(1,13):
    finance_month_list.append(i)
    income = random.randint(10000000,20000000)
    expense = random.randint(5000000,10000000)
    profit = income - expense
    finance_income_list.append(income)
    finance_expense_list.append(expense)
    finance_profit_list.append(profit)

finance_column_list = ["month","income","expense","profit"]
finance_total_list = []
for i in range(12):
    new_list = [finance_month_list[i],finance_income_list[i],finance_expense_list[i],finance_profit_list[i]]
    finance_total_list.append(new_list)
finance = pd.DataFrame(columns=finance_column_list,data=finance_total_list)
finance.to_csv(r"C:\Users\admin\Desktop\3170_data\finance.csv",encoding='utf-8')

random_supplier_list = ["McKesson","CARDINAL","AmerisourceBergen"]
drug_list = []
with open(r"C:\Users\admin\Desktop\3170_data\drug.txt","r") as f:
    for line in f:
        drug_list.append(line[:-1])

medicine_id_list = []
medicine_name_list = []
medicine_supplier_list = []
medicine_stock_list = []
for i in range(2000):
    for j in range(3):
        medicine_supplier_list.append(random_supplier_list[j])

for i in range(6000):
    while True:
        str = "1"
        for j in range(5):
            ch = chr(random.randrange(ord('0'),ord('9') + 1))
            str += ch
        if str in medicine_id_list:
            continue
        else:
            medicine_id_list.append(str)
            break
    index = int(i / 3)
    medicine_name = drug_list[index]
    medicine_name_list.append(medicine_name)
    stock = random.randint(1,200)
    medicine_stock_list.append(stock)

medicine_column_list = ["medicine_id","medicine_name","medicine_supplier","stock"]
medicine_total_list = []
for i in range(6000):
    new_list = [medicine_id_list[i],medicine_name_list[i],medicine_supplier_list[i],medicine_stock_list[i]]
    medicine_total_list.append(new_list)
shuffle(medicine_total_list)
medicine = pd.DataFrame(columns=medicine_column_list,data=medicine_total_list)
medicine.to_csv(r"C:\Users\admin\Desktop\3170_data\medicine.csv",encoding='utf-8')

medicine_buy_date_list = []
medicine_buy_amount_list = []
medicine_price_list = []
medicine_price = 0
for i in range(6000):
    buy_month = choice(random_month_list)
    buy_day = choice(random_day_list)
    buy_date = "2018.%d.%d"%(buy_month,buy_day)
    medicine_buy_date_list.append(buy_date)
    medicine_buy_amount = medicine_stock_list[i] * 2
    medicine_buy_amount_list.append(medicine_buy_amount)
    if (i % 3 == 0) or (i == 0):
        medicine_price = random.randint(10,300)
        medicine_price_list.append(medicine_price)
    else:
        medicine_price = medicine_price + random.randint(-5,5)
        medicine_price_list.append(medicine_price)
medicine_purchase_column_list = ["medicine_id","purchase_date","purchase_amount","purchase_price"]
medicine_purchase_total_list = []
for i in range(6000):
    new_list = [medicine_id_list[i],medicine_buy_date_list[i],medicine_buy_amount_list[i],medicine_price_list[i]]
    medicine_purchase_total_list.append(new_list)
medicine_purchase = pd.DataFrame(columns=medicine_purchase_column_list,data=medicine_purchase_total_list)
medicine_purchase.to_csv(r"C:\Users\admin\Desktop\3170_data\medicine_purchase.csv",encoding='utf-8')

consumption_id_list = []
consumption_treat_id_list = []
consumption_medicine_id_list = []
consumption_medicine_amount_list = []
consumption_price_list = []

for i in range(10000):
    while True:
        str = "1"
        for j in range(5):
            ch = chr(random.randrange(ord('0'),ord('9') + 1))
            str += ch
        if str in consumption_id_list:
            continue
        else:
            consumption_id_list.append(str)
            break
    consumption_treat_id = choice(treat_id_list)
    consumption_medicine_id = choice(medicine_id_list)
    consumption_treat_id_list.append(consumption_treat_id)
    consumption_medicine_id_list.append(consumption_medicine_id)
    consumption_medicine_amount = random.randint(1,5)
    consumption_medicine_amount_list.append(consumption_medicine_amount)
    consumption_price = consumption_medicine_amount * medicine_price_list[medicine_id_list.index(consumption_medicine_id)] * 1.5
    consumption_price_list.append(consumption_price)
medicine_consumption_column_list = ["consumption_id","treat_id","medicine_id","medicine_amount","total_price"]
medicine_consumption_total_list = []
for i in range(6000):
    new_list = [consumption_id_list[i],consumption_treat_id_list[i],consumption_medicine_id_list[i],consumption_medicine_amount_list[i],consumption_price_list[i]]
    medicine_consumption_total_list.append(new_list)
medicine_consumption = pd.DataFrame(columns=medicine_consumption_column_list,data=medicine_consumption_total_list)
medicine_consumption.to_csv(r"C:\Users\admin\Desktop\3170_data\medicine_consumption.csv",encoding='utf-8')















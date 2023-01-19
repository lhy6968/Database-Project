# back-end
from bokeh.io import show, curdoc
from bokeh.plotting import figure
from bokeh.layouts import widgetbox as wb, layout
from bokeh.models import widgets as wd, ColumnDataSource
from bokeh.core.properties import value
from functools import partial
import pymysql
import string
import random

# front-end
from bokeh.io import show, curdoc
from bokeh.plotting import figure
from bokeh.layouts import widgetbox as wb, layout, row
from bokeh.models import widgets as wd, ColumnDataSource
from bokeh.core.properties import value
from functools import partial
# import MySQLdb
import string

# variable declaration
dataBed = {
    'bed_id': [],
    'type': [],
    'status': [],
    'treat_id': [],
    'days_in_bed': []
}

#label list
medicine_purchase_list = ['medicine_id', 'date', 'purchase_amount', 'purchase_price']
medicine_list = ['medicine_id', 'name', 'supplier', 'stock']
medicine_consumption_list = ['treat_id', 'medicine_id', 'consumption_amount', 'sell_price']
equipment_list = ['equip_id', 'name', 'last_check_date']
treatment_record_list = ['treat_id', 'doctor_id', 'patient_id','date', 'symptom']
department_list = ['name', 'dep_phone']
finance_list = ['month', 'income', 'expense', 'profit']
patient_list = []


def connect():
    db = pymysql.connect(
        host="rm-bp1rwi5w2f4irf5q5ro.mysql.rds.aliyuncs.com",
        user="csc3170",
        password="csc3170@",
        port=3306,
        db="csc3170"
    )
    cursor = db.cursor()
    return db, cursor


db, cursor = connect()


### front-end embedded memory
# dataBed = {
#     'bed_id': [],
#     'type': [],
#     'status': [],
#     'treat_id': [],
#     'days_in_bed': []
# }

# columnsBed = [
#     wd.TableColumn(field='bed_id', title = 'Bed_id'),
#     wd.TableColumn(field='type', title = 'Type'),
#     wd.TableColumn(field='status', title = 'Status'),
#     wd.TableColumn(field='treat_id', title = 'Treat_id'),
#     wd.TableColumn(field='days_in_bed', title = 'Days_in_bed'),
# ]
# sourceBed = ColumnDataSource(data=dataBed)
# bed_id_value = ''

### front-end info receiving
# def click(name=None):
#     if name=="bed_query":
#         results = bed_query()
#         refresh_table(results, dataBed, sourceBed)

#     elif name =="bed_checkout":

#         bed_checkout(titleBedIdInput.value)
#         print("The value is ",titleBedIdInput.value)

# def textchange(attr, old, new, name=None):
#     pass

### front-end info presentation
## refresh table
# def refresh_table(rows, data, source):
#     print("table is refreshed")
#     # for row in rows:
#     #     for item in row.items():
#     #         data[item[0]] = data.get(item[0], []) + [item[1]]

#     data['course_id'] = [r['course_id'] for r in rows]
#     data['title'] = [r['title'] for r in rows]
#     data['dept_name'] = [r['dept_name'] for r in rows]
#     data['credits'] = [r['credits'] for r in rows]
#     data['instructor'] = [r['instructor'] for r in rows]
#     source.data = data

####### basic back-end info processing
# 执行 cursor.execute()
# 返回元组 cursor.fetchall()
# 返回单挑数据 cursor.fetchone()
def select_stat(content, table, spe_command='', as_dict=True):
    command_str = "select " + content + " from " + table + spe_command + ";"
    print(command_str)
    # with cursor(as_dict=as_dict) as cursor:
    cursor.execute(command_str)
    results = cursor.fetchall()
    return results


def insert_stat(table, content):
    command_str = "insert into " + table + " values " + content + ";"
    print(command_str)
    cursor.execute(command_str)
    db.commit()


def delete_stat(table, spe_command=''):
    command_str = "delete from " + table + spe_command + ";"
    print(command_str)
    cursor.execute(command_str)
    db.commit()


def update_stat(table, content, spe_command=''):
    command_str = "update " + table + " set " + content + spe_command + ";"
    print(command_str)
    cursor.execute(command_str)
    db.commit()


def name_transfer(condition_index, patient_name):  # input patient name, the index of the filter
    if condition_index != -1 and patient_name:
        if condition_index == 0:
            format1 = ''
            format2 = '%'
        elif condition_index == 1:
            format1 = '%'
            format2 = '%'
        elif condition_index == 2:
            format1 = '%'
            format2 = ''
        patient_name = format1 + patient_name + format2
    else:
        patient_name = ''
    return patient_name


######################################################
############# specific implementation ################
######################################################
def bed_query():
    global dataBed
    rows = select_stat("*", "sickbed")
    # print("bed_query execute")
    # print(rows)

    data = {}
    for row in rows:
        data['bed_id'] = data.get('bed_id', []) + [row[0]]
        data['type'] = data.get('type', []) + [row[1]]
        data['status'] = data.get('status', []) + [row[2]]
        data['treat_id'] = data.get('treat_id', []) + [row[3]]
        data['days_in_bed'] = data.get('days_in_bed', []) + [row[4]]

    sourceBed.data = data

    # return rows


def bed_checkout():
    # print(titleBedIdInput.value)
    # print(bed_id)
    if select_stat('count(*)', 'sickbed', ' where bed_id=' + titleBedIdInput.value + ' and status="occupied"') != 0:
        delete_stat('sickbed', ' where bed_id=' + titleBedIdInput.value)
        paragraphBedSuccess.text = "The patient who occupies the sickbed " + titleBedIdInput.value + " checked out successfully."
    else:
        paragraphBedSuccess.text = "The corresponding sickbed is empty. Checkout fails."
    # print("bed_checkout execute")
    # return text


def doctor_query_name():  # input : doctor name
    temp = name_transfer(1, titleDoctorInput.value)
    if temp:
        rows = select_stat('*', 'doctor', ' where name like "' + temp + '"')
    else:
        rows = select_stat('*', 'doctor')

    data = {}
    for row in rows:
        data['dctor_id'] = data.get('dctor_id', []) + [row[0]]
        data['name'] = data.get('name', []) + [row[1]]
        data['dep_name'] = data.get('dep_name', []) + [row[2]]
        data['gender'] = data.get('gender', []) + [row[3]]
        data['type'] = data.get('type', []) + [row[4]]
        data['phone'] = data.get('phone', []) + [row[5]]
        data['salary'] = data.get('salary', []) + [row[6]]

    sourceDoctor.data = data

    # print("doctor query name execute")
    # return rows


def doctor_query_dpt(attr, old, new):  # input department name
    rows = select_stat('*', 'doctor',
                       ' where doctor.dep_name = "{}"'.format(new))

    data = {}
    for row in rows:
        data['dctor_id'] = data.get('dctor_id', []) + [row[0]]
        data['name'] = data.get('name', []) + [row[1]]
        data['dep_name'] = data.get('dep_name', []) + [row[2]]
        data['gender'] = data.get('gender', []) + [row[3]]
        data['type'] = data.get('type', []) + [row[4]]
        data['phone'] = data.get('phone', []) + [row[5]]
        data['salary'] = data.get('salary', []) + [row[6]]

    sourceDoctor.data = data

    # print("doctor query dpt execute")
    return rows


def doctor_insert():
    docname = titleDoctorEntryName.value
    depname = titleDoctorEntryDept.value
    gender = titleDoctorEntryGend.value
    doctype = titleDoctorEntryType.value
    phone = titleDoctorEntryPhone.value
    salary = titleDoctorEntryWage.value

    rows = select_stat('max(doctor_id)', 'doctor')
    curmax = int(rows[0][0])
    rows = select_stat('count(*)', 'doctor', ' where name=' + '"' + docname + '"')
    # print(rows)
    flag = int(rows[0][0])
    # print(flag)
    if flag >= 1:
        paragraphDoctorEntrySuccess.text = "The doctor already exists."
        return 0
    insert_stat('doctor',
                '({}, "{}", "{}", "{}", "{}", "{}", {})'.format(curmax + 1, docname, depname, gender, doctype, phone,
                                                                salary))
    # print("doctor insert execute")
    paragraphDoctorEntrySuccess.text = "Insertion successful."


def doctor_delete():
    docname = titleDoctorDimiName.value
    delete_stat('doctor', ' where name="{}"'.format(docname))
    paragraphDoctorDimiSuccess.text = "Dimission successful"


def doctor_select():
    rows = select_stat('*', 'doctor',
                       ' where doctor.name = "{}"'.format(titleDoctorUpdName.value))
    row = rows[0]
    # print(rows)
    titleDoctorUpdDept.value = rows[0][2]
    titleDoctorUpdGend.value = rows[0][3]
    titleDoctorUpdType.value = rows[0][4]
    titleDoctorUpdPhone.value = str(rows[0][5])
    titleDoctorUpdWage.value = str(rows[0][6])

    # print("doctor_select query dpt execute")


def doctor_update():
    docname = titleDoctorUpdName.value
    dept_name = titleDoctorUpdDept.value
    gender = titleDoctorUpdGend.value
    doctype = titleDoctorUpdType.value
    phone = titleDoctorUpdPhone.value
    salary = titleDoctorUpdWage.value
    update_stat('doctor',
                'name="{}", dep_name="{}", gender="{}", type="{}", phone="{}", salary={}'.format(docname, dept_name,
                                                                                                 gender, doctype, phone,
                                                                                                 salary),
                ' where name="{}"'.format(docname))
    paragraphDoctorUpdSuccess.text = "Update Successful"

################################################
# def treatment_query():  # input patient id
#     rows = select_stat('*', 'treatment_record', " where patient_id = {}".format(titleTreatInput.value))
#
#     data = {}
#     for row in rows:
#         data['program_id'] = data.get('program_id', []) + [row[0]]
#         data['equip_id'] = data.get('equip_id', []) + [row[1]]
#         data['program_cost'] = data.get('program_cost', []) + [row[2]]
#
#     sourcePatientProg.data =data
#     print("treament query execute")
#     # return rows

def treatment_query(): # input patient id
    #rows = select_stat('patient_id','patient',' where name like "{}"'.format(patient_name))
    #p_id = int(rows[0][0])
    p_id = titlePatientHistoryInput.value
    rows = select_stat('*','treatment_record'," where patient_id = {}".format(p_id))

    data = {}
    for row in rows:
        data['treat_id'] = data.get('treat_id', []) + [row[0]]
        data['doctor_id'] = data.get('doctor_id', []) + [row[1]]
        data['patient_id'] = data.get('patient_id', []) + [row[2]]
        data['date'] = data.get('date', []) + [row[3]]
        data['symptom'] = data.get('symptom', []) + [row[4]]

    sourcePatientHistory.data = data

    # print("treatment query execute")
    return rows


def treatment_query_one():
    p_id = titleTreatInput.value
    rows = select_stat('treat_id','treatment_record',' where patient_id = {} order by date desc limit 0,1'.format(p_id))
    treat_id = rows[0][0]
 
    prog_rows = select_stat('*', 'program', ' where treat_id = {}'.format(treat_id))
    med_rows = select_stat('*', 'medicine_consumption', ' where treat_id={}'.format(treat_id))

    prog_data = {}

    for row in prog_rows:
        prog_data['treat_id'] = prog_data.get('treat_id', []) + [row[0]]
        prog_data['program_id'] = prog_data.get('program_id', []) + [row[1]]
        prog_data['equip_id'] = prog_data.get('equip_id', []) + [row[2]]
        prog_data['program_cost'] = prog_data.get('program_cost', []) + [row[3]]

    sourcePatientProg.data =prog_data

    med_data = {}

    for row in med_rows:
        med_data['treat_id'] = med_data.get('treat_id', []) + [row[0]]
        med_data['medicine_id'] = med_data.get('medicine_id', []) + [row[1]]
        med_data['consumption_amount'] = med_data.get('consumption_amount', []) + [row[2]]
        med_data['sell_price'] = med_data.get('sell_price', []) + [row[3]]

    sourcePatientMed.data = med_data

    # return med_rows, prog_rows


def treatment_insert_program():
    treat_id = titlePatientProgID.value
    equip_id = titlePatientProgEqui.value
    cost = titlePatientProgCost.value

    rows = select_stat('max(program_id)', 'program')
    maxpg_id = int(rows[0][0])

    insert_stat('program', '({},{},{},{})'.format(treat_id, maxpg_id + 1, equip_id, cost))

    paragraphPatientProgSuccess.text = "Add Successfully."




def treatment_insert_medicine():
    treat_id = titlePatientMedTreatID.value
    medi_id = titlePatientMedMedID.value
    ammount = titlePatientMedAmt.value

    x = random.random()
    price = int(x * 100)
    rows = select_stat('stock', 'medicine', ' where medicine_id={}'.format(medi_id))
    stock = int(rows[0][0])
    insert_stat('medicine_consumption', '({},{},{},{})'.format(treat_id, medi_id, ammount, int(ammount)* price))
    update_stat('medicine', 'stock={}'.format(stock - int(ammount)), ' where medicine_id={}'.format(medi_id))

    paragraphPatientMedSuccess.text = "Add Successfully."


def treatment_insert(docname, patient_name, describe='null'):
    rows = select_stat('max(treat_id)', 'treatment_record')
    maxrow = int(rows[0][0])
    rows = select_stat('patient_id', 'patient', ' where name="{}"'.format(patient_name))
    p_id = int(rows[0][0])
    rows = select_stat('doctor_id', 'doctor', ' where name="{}"'.format(docname))
    d_id = int(rows[0][0])
    insert_stat('treatment_record', '({},{},{}, curdate(), "{}")'.format(maxrow + 1, p_id, d_id, describe))


def patient_query():
    patient_name = name_transfer(1, titlePlistInput.value)
    if patient_name:
        rows = select_stat('*', 'patient', ' where name like "{}"'.format(patient_name))
    else:
        rows = select_stat('*', 'patient')

    data = {}
    for row in rows:
        data['patient_id'] = data.get('patient_id', []) + [row[0]]
        data['name'] = data.get('name', []) + [row[1]]
        data['phone'] = data.get('phone', []) + [row[2]]
        data['gender'] = data.get('gender', []) + [row[3]]
        data['has_medi_insurance'] = data.get('has_medi_insurance', []) + [row[4]]

    sourcePlist.data = data

    # print("patient query execute")
    # return rows
######################################################################################################

def patient_insert():
    patient_name = titlePAddName.value
    phone = titlePAddPhone.value
    gender = titlePAddGender.value
    insurance = titlePAddInsur.value

    rows = select_stat('max(patient_id)', 'patient')
    maxrow = int(rows[0][0])
    insert_stat('patient', '({},"{}","{}","{}","{}")'.format(maxrow + 1, patient_name, phone, gender, insurance))
    paragraphPAddSuccess.text = "Insertion successful."

def patient_update():
    patient_id = titlePUpdID.value
    phone = titlePUpdPhone.value
    gender = titlePUpdGend.value
    insurance = titlePUpdinsur.value

    update_stat('patient',
                'phone="{}", gender="{}", has_medi_insurance="{}"'.format(phone, gender, insurance),
                ' where patient_id={}'.format(patient_id))

    paragraphPUpdSuccess.text = "Update Successful."

def patient_select():
    rows = select_stat('*', 'patient',
                       ' where patient.patient_id = {}'.format(titlePUpdID.value))
    row = rows[0]
    #print(rows)
    titlePUpdName.value = str(rows[0][1])
    titlePUpdPhone.value = str(rows[0][2])
    titlePUpdGend.value = rows[0][3]
    titlePUpdinsur.value = str(rows[0][4])

    # print("patient_select query dpt execute")

def patient_delete():
    patient_id = titlePDelID.value
    delete_stat('patient', ' where patient_id = {}'.format(patient_id))
    paragraphPDelSuccess.text = "Dimission successful."


def medicine_query():
    name = titleMedInput.value
    name = name_transfer(1, name)
    if name:
        rows = select_stat('*', 'medicine', ' where name like "{}"'.format(name))
    else:
        rows = select_stat('*', 'medicine')

    data = {}
    for row in rows:
        data['medicine_id'] = data.get('medicine_id', []) + [row[0]]
        data['name'] = data.get('name', []) + [row[1]]
        data['supplier'] = data.get('supplier', []) + [row[2]]
        data['stock'] = data.get('stock', []) + [row[3]]

    sourceMedList.data = data

    # return rows


def medicine_purchase():
    m_id = titleMedPurID.value
    number = titleMedPurQuant.value
    rows = select_stat('stock', 'medicine', ' where medicine_id={}'.format(m_id))
    stock = int(rows[0][0])
    update_stat('medicine', ' stock={}'.format(int(stock) + int(number)), ' where medicine_id={}'.format(m_id))

    paragraphMedPurSuccess.text = "Purchase Successfully."


def medicine_insert():
    name = titleMedAddName.value
    supplier = titleMedAddSupp.value
    num = titleMedAddQuant.value
    rows = select_stat('max(medicine_id)', 'medicine')
    max_mid = int(rows[0][0])
    insert_stat('medicine', '({},"{}","{}",{})'.format(max_mid + 1, name, supplier, num))

    paragraphMedAddSuccess.text = "Insertion successful."


def medicine_delete():
    m_id = titleMedDelID.value
    delete_stat('medicine', ' where medicine_id = {}'.format(m_id))

    paragraphMedDelSuccess.text = "Deletion successful."


def equipment_query():
    name = titleEquiInput.value
    name = name_transfer(1, name)
    if name:
        rows = select_stat('*', 'equipment', ' where name like "{}"'.format(name))
    else:
        rows = select_stat('*', 'equipment')

    data = {}
    for row in rows:
        data['equip_id'] = data.get('equip_id', []) + [row[0]]
        data['name'] = data.get('name', []) + [row[1]]
        data['last_check_date'] = data.get('last_check_date', []) + [row[2]]

    sourceEquiList.data = data

    # return rows


def equipment_insert():
    name = titleEquiAddName.value
    rows = select_stat('max(equip_id)', 'equipment')
    max_eid = int(rows[0][0])
    insert_stat('equipment', '({},"{}", curdate())'.format(max_eid + 1, name))

    paragraphEquiAddSuccess.text ="Insertion Successful. "


def equipment_maintain():
    equip_id = titleEquiMainName.value
    update_stat('equipment', 'last_check_date=curdate()', ' where equip_id={}'.format(equip_id))

    paragraphEquiMainSuccess.text = "Maintain Successfully."

def finance_statistics():
    select_stat('*','finance')

# rows=medicine_query('')
# print(rows)

# medicine_insert('csc3170poison','cuhksz',1)
# medicine_delete(199972)
# medicine_purchase(199972, 10)

# rows=select_stat('max(treat_id)','treatment_record')
# pid = rows[0][0]
# treatment_insert_medicine(pid,199972,5)
# rows=medicine_query('csc3170')
# print(rows)


# equipment_insert('csc3170poison')
# rows=equipment_query('csc3170')
# print(rows)

# patient_insert('csc3170poison','null','null','null')
# rows=patient_query('csc3170')
# print(rows)
# pat

# rows = treatment_query('%a')
# row = medicine_query('')
# print(rows)
# print("select * from equipment where name like '%perating-lamp%';")
# cursor.execute(r"select * from equipment where name like '%ope%';")
# print(cursor.fetchall())


# db.close()

# bed_query_button = wd.Button(label = 'Bad status')
# discharge_button = wd.Button(label = 'Discharge')
# doctor_query_button = wd.Button(label = 'Doctor information')
# doctor_insert_button = wd.Button(label = 'Doctor registration')
# doctor_delete_button = wd.Button(label = 'Doctor resigns')
# doctor_update_button = wd.Button(label = 'Doctor transfer')


######## front end layout/widgets
# divBed = wd.Div(text="""<h2>\nBed Usage Status</h2>""", width = 1000)
# btnRefreshBed = wd.Button(label='Refresh')
# tableBed = wd.DataTable(source=sourceBed, columns=columnsBed, width=865)

# divCheckoutBed = wd.Div(text="""<h2>Hospitalized Patient Check Out</h2>""", width=1000)
# titleBedIdInput = wd.TextInput(title='Bed ID:', value='', placeholder='Bed ID', width=275)
# btnCheckOutBed = wd.Button(label='Check Out')
# paragraphSuccess = wd.Paragraph(text=' ')

# btnCheckOutBed.on_click(partial(click,name="bed_query"))
# btnRefreshBed.on_click(partial(click,name="bed_checkout"))


# layBed = layout(
#     [
#         [wb(divBed)],
#         [wb(btnRefreshBed, width=100)],
#         [wb(tableBed)],
#         [wb(divCheckoutBed)],
#         [wb(titleBedIdInput, width=400)],
#         [wb(btnCheckOutBed, paragraphSuccess, width=100)]
#     ]
# )

# tabBed = wd.Panel(child=layBed, title="Bed MGT")

# tabs = wd.Tabs(tabs=[tabBed])


# curdoc().add_root(tabs)


# Tab Bed
columnsBed = [
    wd.TableColumn(field='bed_id', title='Bed ID'),
    wd.TableColumn(field='type', title='Type'),
    wd.TableColumn(field='status', title='Status'),
    wd.TableColumn(field='treat_id', title='Treat ID'),
    wd.TableColumn(field='days_in_bed', title='Days in Bed'),
]

sourceBed = ColumnDataSource(data=dataBed)

bed_query()

divBed = wd.Div(text="""<h2>\nSick Bed Usage Status</h2>""", width=1000)
btnRefreshBed = wd.Button(label='Refresh', width=100)
tableBed = wd.DataTable(source=sourceBed, columns=columnsBed, width=865)

divCheckoutBed = wd.Div(text="""<h2>Hospitalized Patient Check Out</h2>""", width=1000)
titleBedIdInput = wd.TextInput(title='Bed ID:', value='', placeholder='Bed ID', width=275)
btnCheckOutBed = wd.Button(label='Check Out', width=100)
paragraphBedSuccess = wd.Paragraph(text=' ')

# Tab Doctor

# Doctor search

dataDoctor = {
    'dctor_id': [],
    'name': [],
    'dep_name': [],
    'gender': [],
    'type': [],
    'phone': [],
    'salary': []
}

columnsDoctor = [
    wd.TableColumn(field='dctor_id', title='Doctor ID'),
    wd.TableColumn(field='name', title='Name'),
    wd.TableColumn(field='dep_name', title='Department'),
    wd.TableColumn(field='gender', title='Gender'),
    wd.TableColumn(field='type', title='type'),
    wd.TableColumn(field='phone', title='Phone'),
    wd.TableColumn(field='salary', title='Salary'),

]
sourceDoctor = ColumnDataSource(data=dataDoctor)

doctorDepts = ['Burns',
               'Cardiology',
               'Dermatology',
               'Endocrinology',
               'Gastroenterology',
               'General Surgery',
               'Gynecology',
               'Hematology',
               'Infection',
               'Neurology',
               'Neurosurgery',
               'Obstetrics',
               'Orthopedics',
               'Otolaryngolog',
               'Pediatrics',
               'Respiratory Medicine',
               'Stomatology',
               'Urinary Surgery',
               'Urologic']

doctor_query_dpt(0, 0, doctorDepts[0])

divDoctor = wd.Div(text="""<h2>\nDoctor Infomation</h2>""", width=1000)
selectDoctor = wd.Select(title='Department:', value='', options=doctorDepts, width=250)
titleDoctorInput = wd.TextInput(title='Doctor name:', value='', placeholder='Doctor', width=250)
btnRefreshDoctor = wd.Button(label='Refresh', width=250)
tableDoctor = wd.DataTable(source=sourceDoctor, columns=columnsDoctor, width=865)

# Doctor entry

divDoctorEntry = wd.Div(text="""<h2>\nDoctor Entry</h2>""", width=1000)
titleDoctorEntryName = wd.TextInput(title='Doctor name:', value='', placeholder='Name', width=150)
titleDoctorEntryDept = wd.TextInput(title='Doctor Department:', value='', placeholder='Department', width=150)
titleDoctorEntryGend = wd.TextInput(title='Doctor Gender:', value='', placeholder='Gender', width=150)
titleDoctorEntryType = wd.TextInput(title='Doctor Type:', value='', placeholder='Type', width=150)
titleDoctorEntryPhone = wd.TextInput(title='Doctor Phone:', value='', placeholder='Phone', width=150)
titleDoctorEntryWage = wd.TextInput(title='Doctor Salary:', value='', placeholder='Salary', width=150)
btnDoctorEntry = wd.Button(label='Insert', width=100)
paragraphDoctorEntrySuccess = wd.Paragraph(text=' ')

# Doctor dimission

divDoctorDimi = wd.Div(text="""<h2>\nDoctor Dimission</h2>""", width=1000)
titleDoctorDimiName = wd.TextInput(title='Doctor name:', value='', placeholder='Name', width=250)
btnDoctorDimi = wd.Button(label='Process', width=100)
paragraphDoctorDimiSuccess = wd.Paragraph(text=' ')

# Doctor update

divDoctorUpd = wd.Div(text="""<h2>\nDoctor Update</h2>""", width=1000)
titleDoctorUpdName = wd.TextInput(title='Doctor name:', value='', placeholder='Name', width=250)
btnDoctorUpdShow = wd.Button(label='Show', width=100)
titleDoctorUpdDept = wd.TextInput(title='Doctor Department:', value='', placeholder='Department', width=150)
titleDoctorUpdGend = wd.TextInput(title='Doctor Gender:', value='', placeholder='Gender', width=150)
titleDoctorUpdType = wd.TextInput(title='Doctor Type:', value='', placeholder='Type', width=150)
titleDoctorUpdPhone = wd.TextInput(title='Doctor Phone:', value='', placeholder='Phone', width=150)
titleDoctorUpdWage = wd.TextInput(title='Doctor Salary:', value='', placeholder='Salary', width=150)
btnDoctorUpdUpdate = wd.Button(label='Update', width=100)
paragraphDoctorUpdSuccess = wd.Paragraph(text=' ')

# Tab Outpatient

dataPatientProg = {
    'program_id': [],
    'equip_id': [],
    'program_cost': []
}

columnsPatientProg = [
    wd.TableColumn(field='treat_id', title='Treatment ID'),
    wd.TableColumn(field='program_id', title='Program ID'),
    wd.TableColumn(field='equip_id', title='Equipment ID'),
    wd.TableColumn(field='program_cost', title='Program Cost')
]

sourcePatientProg = ColumnDataSource(data=dataPatientProg)

dataPatientMed = {
    # 'treat_id': [],
    'medicine_id': [],
    'consumption_amount': [],
    'sell_price': []
}

columnsPatientMed = [
    wd.TableColumn(field='treat_id', title='Treat ID'),
    wd.TableColumn(field='medicine_id', title='Medicine ID'),
    wd.TableColumn(field='consumption_amount', title='Consumption Amount'),
    wd.TableColumn(field='sell_price', title='Sell Price')
]

sourcePatientMed = ColumnDataSource(data=dataPatientMed)

divOpSession = wd.Div(text="""<h2>\nThis Outpatient Service Session</h2>""", width=1000)
titleTreatInput = wd.TextInput(title='Patient ID:', value='', placeholder='Patient ID', width=250)
btnSearchpatient = wd.Button(label='Search', width=250)
paragraphProg = wd.Paragraph(text='Programs:')
paragraphMed = wd.Paragraph(text='Medicine:')
tablePatientProg = wd.DataTable(source=sourcePatientProg, columns=columnsPatientProg, width=500, height=200)
tablePatientMed = wd.DataTable(source=sourcePatientMed, columns=columnsPatientMed, width=500, height=200)

# Add program

divPatientProgSession = wd.Div(text="""<h3>\nAdd Program</h3>""", width=1000)
titlePatientProgID = wd.TextInput(title='Treatement ID:', value='', placeholder='Treatment ID', width=150)
titlePatientProgEqui = wd.TextInput(title='Equipment:', value='', placeholder='Equipment', width=150)
titlePatientProgCost = wd.TextInput(title='Cost:', value='', placeholder='Cost', width=150)
btnPatientProgAdd = wd.Button(label='Add', width=100)
paragraphPatientProgSuccess = wd.Paragraph(text=' ')

# Add medicine

divPatientMedSession = wd.Div(text="""<h3>\nAdd Medicine</h3>""", width=1000)
titlePatientMedTreatID = wd.TextInput(title='Treatement ID:', value='', placeholder='Treatment ID', width=150)
titlePatientMedMedID = wd.TextInput(title='Medicine ID:', value='', placeholder='Medicine ID', width=150)
titlePatientMedAmt = wd.TextInput(title='Amount:', value='', placeholder='Amount', width=150)
btnPatientMedAdd = wd.Button(label='Add', width=100)
paragraphPatientMedSuccess = wd.Paragraph(text=' ')

# Patient History

dataPatientHistory = {
    'treat_id': [],
    'doctor_id': [],
    'patient_id': [],
    'date': [],
    'symptom': []
}
columnsPatientHistory = [
    wd.TableColumn(field='treat_id', title='Treatment ID'),
    wd.TableColumn(field='doctor_id', title='Doctor ID'),
    wd.TableColumn(field='patient_id', title='Patient ID'),
    wd.TableColumn(field='date', title='Date'),
    wd.TableColumn(field='symptom', title='Symptom'),
]
sourcePatientHistory = ColumnDataSource(data=dataPatientHistory)

divOpSessionHistory = wd.Div(text="""<h2>\nOutpatient History Record</h2>""", width=1000)
titlePatientHistoryInput = wd.TextInput(title='Patient ID:', value='', placeholder='Patient ID', width=250)
btnSearchpatientHistory = wd.Button(label='Search', width=250)
tablePatientHistory = wd.DataTable(source=sourcePatientHistory, columns=columnsPatientHistory)

# Tab PatientList

# Patient Search
dataPlist = {
    'patient_id': [],
    'name': [],
    'phone': [],
    'gender': [],
    'has_medi_insurance': []
}

columnsPlist = [
    wd.TableColumn(field='patient_id', title='Patient ID'),
    wd.TableColumn(field='name', title='Name'),
    wd.TableColumn(field='phone', title='phone'),
    wd.TableColumn(field='gender', title='gender'),
    wd.TableColumn(field='has_medi_insurance', title='has_medi_insurance'),
]
sourcePlist = ColumnDataSource(data=dataPlist)


divPSession = wd.Div(text="""<h2>\nPatient Search</h2>""", width=1000)
titlePlistInput = wd.TextInput(title='Patient Name:', value='', placeholder='Patient Name', width=250)
btnSearchPlist = wd.Button(label='Search', width=250)
tablePlist = wd.DataTable(source=sourcePlist, columns=columnsPlist, width=865)

patient_query()

# Patient Add
divPAdd = wd.Div(text="""<h2>\nAdd Patient</h2>""", width=1000)
titlePAddName = wd.TextInput(title='Patient Name:', value='', placeholder='Name', width=150)
titlePAddPhone = wd.TextInput(title='Patient Phone:', value='', placeholder='Phone', width=150)
titlePAddGender = wd.TextInput(title='Patient Gender:', value='', placeholder='Gender', width=150)
titlePAddInsur = wd.TextInput(title='Patient Insurance:', value='', placeholder='insurance', width=150)
btnPAdd = wd.Button(label='Add', width=100)
paragraphPAddSuccess = wd.Paragraph(text=' ')

# Patient Update

divPUpd = wd.Div(text="""<h2>\nUpdate Patient</h2>""", width=1000)
titlePUpdID = wd.TextInput(title='Patient ID:', value='', placeholder='Patient ID', width=250)
btnPUpdShow = wd.Button(label='Show', width=100)
titlePUpdName = wd.TextInput(title='Patient Name:', value='', placeholder='Name', width=150)
titlePUpdPhone = wd.TextInput(title='Patient Phone:', value='', placeholder='Phone', width=150)
titlePUpdGend = wd.TextInput(title='Patient Gender:', value='', placeholder='Gender', width=150)
titlePUpdinsur = wd.TextInput(title='Patient Insurance:', value='', placeholder='Insurance', width=150)
btnPUpdUpdate = wd.Button(label='Update', width=100)
paragraphPUpdSuccess = wd.Paragraph(text=' ')

# Patient Delete

divPDel = wd.Div(text="""<h2>\nDelete Patient</h2>""", width=1000)
titlePDelID = wd.TextInput(title='Patient ID:', value='', placeholder='Patient ID', width=250)
btnPDel = wd.Button(label='Process', width=100)
paragraphPDelSuccess = wd.Paragraph(text=' ')

# Tab Medicine

# Medicine Search'

dataMedList = {
    'medicine_id': [],
    'name': [],
    'supplier': [],
    'stock': []
}

columnsMedList = [
    wd.TableColumn(field='medicine_id', title='MedicineID'),
    wd.TableColumn(field='name', title='Name'),
    wd.TableColumn(field='supplier', title='Supplier'),
    wd.TableColumn(field='stock', title='Stock')
]
sourceMedList = ColumnDataSource(data=dataMedList)


divMedSearch = wd.Div(text="""<h2>\nMedicine Search</h2>""", width=1000)
titleMedInput = wd.TextInput(title='Medicine Name:', value='', placeholder='Medicine Name', width=250)
btnSearchMed = wd.Button(label='Search', width=250)
tableMed = wd.DataTable(source=sourceMedList, columns=columnsMedList, width=865)

medicine_query()

# Medicine Purchase

divMedPur = wd.Div(text="""<h2>\nMedicine Purchase</h2>""", width=1000)
titleMedPurID = wd.TextInput(title='Medicine ID:', value='', placeholder='ID', width=150)
titleMedPurQuant = wd.TextInput(title='Quantity:', value='', placeholder='Quantity', width=150)
btnMedPur = wd.Button(label='Purchase', width=100)
paragraphMedPurSuccess = wd.Paragraph(text=' ')

# Medicine Add

divMedAdd = wd.Div(text="""<h2>\nAdd Medicine</h2>""", width=1000)
titleMedAddName = wd.TextInput(title='Medicine Name:', value='', placeholder='Name', width=150)
titleMedAddSupp = wd.TextInput(title='Medicine Supplier:', value='', placeholder='Supplier', width=150)
titleMedAddQuant = wd.TextInput(title='Quantity:', value='', placeholder='Quantity', width=150)
btnMedAdd = wd.Button(label='Add', width=100)
paragraphMedAddSuccess = wd.Paragraph(text=' ')

# Medicine Delete

divMedDel = wd.Div(text="""<h2>\nDelete Medicine</h2>""", width=1000)
titleMedDelID = wd.TextInput(title='Medicine ID:', value='', placeholder='ID', width=250)
btnMedDel = wd.Button(label='Process', width=100)
paragraphMedDelSuccess = wd.Paragraph(text=' ')

# Tab Equipment

# Equipment Search

dataEquiList = {
    'equip_id': [],
    'name': [],
    'last_check_date': [],
}

columnsEquiList = [
    wd.TableColumn(field='equip_id', title='Equip ID'),
    wd.TableColumn(field='name', title='Name'),
    wd.TableColumn(field='last_check_date', title='Last Check Date'),
]
sourceEquiList = ColumnDataSource(data=dataEquiList)


divEquiSearch = wd.Div(text="""<h2>\nEquipment Search</h2>""", width=1000)
titleEquiInput = wd.TextInput(title='Equipment Name:', value='', placeholder='Equipment Name', width=250)
btnSearchEqui = wd.Button(label='Search', width=250)
tableEqui = wd.DataTable(source=sourceEquiList, columns=columnsEquiList, width=865)

equipment_query()

# Equipment Add

divEquiAdd = wd.Div(text="""<h2>\nAdd Equipment</h2>""", width=1000)
titleEquiAddName = wd.TextInput(title='Equipment Name:', value='', placeholder='Name', width=150)
btnEquiAdd = wd.Button(label='Add', width=100)
paragraphEquiAddSuccess = wd.Paragraph(text=' ')

# Equipment Maintenance

divEquiMain = wd.Div(text="""<h2>\nEquipment Maintenance</h2>""", width=1000)
titleEquiMainName = wd.TextInput(title='Equipment ID:', value='', placeholder='ID', width=150)
btnEquiMain = wd.Button(label='Update', width=100)
paragraphEquiMainSuccess = wd.Paragraph(text=' ')

# Tab Accounting

# actDepts = []

# divAct = wd.Div(text="""<h2>\nBalance Figure</h2>""", width=1000)
# selectAct = wd.Select(title='Department:', value='', options=actDepts, width=250)

# month = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
# dataChart = {
#     'month': month,
#     'balance': []
# }

# # getActDepts();
# sourceChart = ColumnDataSource(data=dataChart)

# figureAct = figure(x_range=month, plot_height=600, title='Accounting Info', toolbar_location=None, tools='')
# figureAct.vbar_stack(['balance'], x='month', width=0.9, color=['#e84d60'], source=sourceChart, legend=['Balance'])
# figureAct.y_range.start = 0
# figureAct.y_range.end = 10000000

layBed = layout(
    [
        [wb(divBed)],
        [wb(btnRefreshBed, tableBed)],
        [wb(divCheckoutBed)],
        [wb(titleBedIdInput, btnCheckOutBed, paragraphBedSuccess, width=400)]
    ]
)

layDoctor = layout(
    [
        [wb(divDoctor)],
        [wb(titleDoctorInput, btnRefreshDoctor, width=400), wb(selectDoctor)],
        [wb(tableDoctor)],
        [wb(divDoctorEntry)],
        [wb(titleDoctorEntryName, btnDoctorEntry, paragraphDoctorEntrySuccess, width=200),
         wb(titleDoctorEntryDept, width=200), wb(titleDoctorEntryGend, width=200), wb(titleDoctorEntryType, width=200),
         wb(titleDoctorEntryPhone, width=200), wb(titleDoctorEntryWage, width=200)],
        [wb(divDoctorDimi)],
        [wb(titleDoctorDimiName, btnDoctorDimi, paragraphDoctorDimiSuccess, width=400)],
        [wb(divDoctorUpd)],
        [wb(titleDoctorUpdName, btnDoctorUpdShow)],
        [wb(titleDoctorUpdDept, btnDoctorUpdUpdate, paragraphDoctorUpdSuccess, width=200),
         wb(titleDoctorUpdGend, width=200), wb(titleDoctorUpdType, width=200), wb(titleDoctorUpdPhone, width=200),
         wb(titleDoctorUpdWage, width=200)],
    ]
)

layPatient = layout(
    [
        [wb(divOpSession)],
        [wb(titleTreatInput, btnSearchpatient)],
        [wb(paragraphProg, tablePatientProg, width=600), wb(paragraphMed, tablePatientMed)],
        [wb(divPatientProgSession)],
        [wb(titlePatientProgID, btnPatientProgAdd, paragraphPatientProgSuccess, width=200),
         wb(titlePatientProgEqui, width=200), wb(titlePatientProgCost, width=200)],
        [wb(divPatientMedSession)],
        [wb(titlePatientMedTreatID, btnPatientMedAdd, paragraphPatientMedSuccess, width=200),
         wb(titlePatientMedMedID, width=200), wb(titlePatientMedAmt, width=200)],
        [wb(divOpSessionHistory)],
        [wb(titlePatientHistoryInput, btnSearchpatientHistory)],
        [wb(tablePatientHistory)]
    ]
)

layPlist = layout(
    [
        [wb(divPSession)],
        [wb(titlePlistInput, btnSearchPlist)],
        [wb(tablePlist)],
        [wb(divPAdd)],
        [wb(titlePAddName, btnPAdd, paragraphPAddSuccess, width=200), wb(titlePAddPhone, width=200),
         wb(titlePAddGender, width=200), wb(titlePAddInsur, width=200)],
        [wb(divPUpd)],
        [wb(titlePUpdID, btnPUpdShow)],
        [wb(titlePUpdName, btnPUpdUpdate, paragraphPUpdSuccess, width=200), wb(titlePUpdPhone, width=200),
         wb(titlePUpdGend, width=200), wb(titlePUpdinsur, width=200)],
        [wb(divPDel)],
        [wb(titlePDelID, btnPDel, paragraphPDelSuccess, width=400)]
    ]
)

layMed = layout(
    [
        [wb(divMedSearch)],
        [wb(titleMedInput, btnSearchMed)],
        [wb(tableMed)],
        [wb(divMedPur)],
        [wb(titleMedPurID, btnMedPur, paragraphMedPurSuccess, width=200), wb(titleMedPurQuant, width=200)],
        [wb(divMedAdd)],
        [wb(titleMedAddName, btnMedAdd, paragraphMedAddSuccess, width=200), wb(titleMedAddSupp, width=200),
         wb(titleMedAddQuant, width=200)],
        [wb(divMedDel)],
        [wb(titleMedDelID, btnMedDel, paragraphMedDelSuccess, width=400)]
    ]
)

layEqui = layout(
    [
        [wb(divEquiSearch)],
        [wb(titleEquiInput, btnSearchEqui)],
        [wb(tableEqui)],
        [wb(divEquiAdd)],
        [wb(titleEquiAddName, btnEquiAdd, paragraphEquiAddSuccess, width=200)],
        [wb(divEquiMain)],
        [wb(titleEquiMainName, btnEquiMain, paragraphEquiMainSuccess, width=200)],
    ]
)

# layAct = layout(
#     [
#         [wb(divAct)],
#         [wb(selectAct, width=300), figureAct]
#     ]
# )

tabBed = wd.Panel(child=layBed, title="Bed MGT")
tabDoctor = wd.Panel(child=layDoctor, title="Doctor MGT")
tabPatient = wd.Panel(child=layPatient, title="Outpatient")
tabPlist = wd.Panel(child=layPlist, title="Patient MGT")
tabMed = wd.Panel(child=layMed, title="Medicine MGT")
tabEqui = wd.Panel(child=layEqui, title="Equipment MGT")
# tabAct = wd.Panel(child=layAct, title="Accounting")

tabs = wd.Tabs(tabs=[tabDoctor, tabPlist, tabPatient, tabBed, tabMed, tabEqui])

btnRefreshBed.on_click(bed_query)
btnCheckOutBed.on_click(bed_checkout)

btnRefreshDoctor.on_click(doctor_query_name)
selectDoctor.on_change('value', doctor_query_dpt)
btnDoctorEntry.on_click(doctor_insert)
btnDoctorDimi.on_click(doctor_delete)
btnDoctorUpdShow.on_click(doctor_select)
btnDoctorUpdUpdate.on_click(doctor_update)

btnSearchpatient.on_click(treatment_query_one)
btnPatientProgAdd.on_click(treatment_insert_program)
btnPatientMedAdd.on_click(treatment_insert_medicine)
btnSearchpatientHistory.on_click(treatment_query)

btnSearchPlist.on_click(patient_query)
btnPAdd.on_click(patient_insert)
btnPUpdShow.on_click(patient_select)
btnPUpdUpdate.on_click(patient_update)
btnPDel.on_click(patient_delete)

btnSearchMed.on_click(medicine_query)
btnMedPur.on_click(medicine_purchase)
btnMedAdd.on_click(medicine_insert)
btnMedDel.on_click(medicine_delete)
btnSearchEqui.on_click(equipment_query)

btnEquiAdd.on_click(equipment_insert)
btnEquiMain.on_click(equipment_maintain)

# selectAct.on_change('value', )



curdoc().add_root(tabs)

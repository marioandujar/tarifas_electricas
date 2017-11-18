from xlrd import open_workbook
from datetime import datetime
from endesa import Endesa
from viesgo import Viesgo

# Valle 22h a 12h
winter_from_month = 10
winter_from_day = 29
winter_to_month = 3
winter_to_day = 24

# Valle 23h a 13h
summer_from_month = 3
summer_from_day = 25
summer_to_month = 10
summer_to_day = 28

potencia_contratada = 4.6

dh = {
    "Nocturna": {
        "Summer": {
            "Valle": [23, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            "Punta": [13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
        },
        "Winter": {
            "Valle": [22, 23, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
            "Punta": [12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
        }
    },
    "SuperValle": {
        "SuperValle": [1, 2, 3, 4, 5, 6],
        "Valle": [7, 8, 9, 10, 11, 12, 23, 0],
        "Punta": [13, 14, 15, 16, 17, 18, 19, 20, 21, 22],
    }
}

rates = {
    "Endesa": {
        "PVPC": {
            "Amount": 0.120152,
            "AmountPotencia": 38.043426 + 3.113,
            "PercentDiscount": 0
        },
        "OneLuz": {
            "Normal": {
                "Amount": 0.115412,
                "AmountPotencia": 3.429702 * 12,
                "PercentDiscount": 0
            },
            "Nocturna": {
                "AmountValle": 0.061361,
                "AmountPunta": 0.140343,
                "AmountPotencia": 3.429702 * 12,
                "PercentDiscount": 0
            },
        },
        "Tempo": {
            "Nocturna": {
                "AmountValle": 0.072765,
                "AmountPunta": 0.149153,
                "AmountPotencia": 3.773192 * 12,
                "PercentDiscount": 0.05
            },
            "SuperValle": {
                "AmountValle": 0.087415,
                "AmountPunta": 0.156462,
                "AmountSuperValle": 0.067102,
                "AmountPotencia": 3.351737 * 12,
                "PercentDiscount": 0.05
            }
        }
    },
    "Viesgo": {
        "Online": {
            "Normal": {
                "Amount": 0.109813,
                "AmountPotencia": 0.117556 * 365,
                "PercentDiscountEnergy": 0.27
            },
            "Nocturna": {
                "AmountValle": 0.069223,
                "AmountPunta": 0.135682,
                "AmountPotencia": 0.117556 * 365,
                "PercentDiscountEnergy": 0.25
            }
        }
    }
}


def check_rate_night(group, hour, date_str):
    wh = float(group[hour])
    hour = int(hour)
    date = datetime.strptime(date_str, "%Y-%m-%d")
    if datetime(year=date.year, month=summer_from_month, day=summer_from_day) < date < datetime(year=date.year,
                                                                                                month=summer_to_month,
                                                                                                day=summer_to_day):  # summer
        if hour in dh["Nocturna"]["Summer"]["Valle"]:  # Valle
            group["Nocturna"]["Valle"] += wh
        else:  # Punta
            group["Nocturna"]["Punta"] += wh
    else:
        if hour in dh["Nocturna"]["Winter"]["Valle"]:  # Valle
            group["Nocturna"]["Valle"] += wh
        else:  # Punta
            group["Nocturna"]["Punta"] += wh


def check_rate_super_night(group, hour):
    wh = float(group[hour])
    hour = int(hour)
    if hour in dh["SuperValle"]["SuperValle"]:  # SuperValle
        group["SuperValle"]["SuperValle"] += wh
    elif hour in dh["SuperValle"]["Valle"]:  # Punta
        group["SuperValle"]["Punta"] += wh
    else:
        group["SuperValle"]["Valle"] += wh


class RecDay(object):
    def __init__(self, date, hour, wh):
        self.date = date
        self.hour = hour
        self.wh = wh

    def __str__(self):
        return ("RecDay object:\n"
                "  date = {0}\n"
                "  hour = {1}\n"
                "  wh = {2}"
                .format(self.date, self.hour, self.wh))


wb = open_workbook('consumption.xls')
for sheet in wb.sheets():
    number_of_rows = sheet.nrows
    number_of_columns = sheet.ncols
    items = []

    rows = []
    for row in range(0, number_of_rows):
        values = []
        for col in range(number_of_columns):
            value = (sheet.cell(row, col).value)
            try:
                value = str(int(value))
            except ValueError:
                pass
            finally:
                if value != "":
                    values.append(value)
        if len(values) > 0:
            item = RecDay(*values)
            items.append(item)

group = {}
total = {
    "total": 0,
    "Nocturna": {"Punta": 0, "Valle": 0},
    "SuperValle": {"SuperValle": 0, "Punta": 0, "Valle": 0}
}
min_date = None
max_date = None
for item in items:
    if item.date not in group:
        group[item.date] = {
            "Nocturna": {"Punta": 0, "Valle": 0},
            "SuperValle": {"SuperValle": 0, "Punta": 0, "Valle": 0}
        }
    if min_date is None or datetime.strptime(item.date, "%Y-%m-%d") < min_date:
        min_date = datetime.strptime(item.date, "%Y-%m-%d")
    if max_date is None or datetime.strptime(item.date, "%Y-%m-%d") > max_date:
        max_date = datetime.strptime(item.date, "%Y-%m-%d")

    group[item.date][item.hour] = item.wh
    check_rate_night(group[item.date], item.hour, item.date)
    check_rate_super_night(group[item.date], item.hour)

    total["total"] += (float(item.wh) / 1000)

for date in group:
    total["Nocturna"]["Punta"] += (group[date]["Nocturna"]["Punta"] / 1000)
    total["Nocturna"]["Valle"] += (group[date]["Nocturna"]["Valle"] / 1000)

    total["SuperValle"]["SuperValle"] += (
        group[date]["SuperValle"]["SuperValle"] / 1000)
    total["SuperValle"]["Punta"] += (group[date]["SuperValle"]["Punta"] / 1000)
    total["SuperValle"]["Valle"] += (group[date]["SuperValle"]["Valle"] / 1000)

days = len(group)
endesa = Endesa(total, rates["Endesa"], potencia_contratada, days)
viesgo = Viesgo(total, rates["Viesgo"], potencia_contratada, days)

print("Periodo de {} a {}".format(min_date.strftime("%d-%m-%Y"), max_date.strftime("%d-%m-%Y")))
print("")
endesa.print_endesa_pvpc_sin_dh()
endesa.print_endesa_one_luz()
endesa.print_endesa_one_luz_nocturna()
endesa.print_endesa_tempo_nocturna()
endesa.print_endesa_tempo_super_valle()

viesgo.print_viesgo_online()
viesgo.print_viesgo_online_nocturna()

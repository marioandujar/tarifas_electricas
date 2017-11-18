# coding=utf-8
class Endesa:
    def __init__(self, total, rates, potencia_contratada, days):
        self.total = total
        self.rates = rates
        self.potencia_contratada = potencia_contratada
        self.days = days

    def print_endesa_pvpc_sin_dh(self):
        print('TARIFA ENDESA: PVPC SIN DH')
        print(' - Total kW {0:.2f}'.format(self.total["total"]))
        suma_consumo = self.total["total"] * self.rates["PVPC"]["Amount"]
        suma_potencia = self.potencia_contratada * self.rates["PVPC"]["AmountPotencia"] * self.days / 365
        total_factura = suma_consumo + suma_potencia
        print(" Importe por consumo: {0:.2f} €".format(suma_consumo))
        print(" Importe por potencia: {0:.2f} €".format(suma_potencia))
        print(
            " Total factura: {0:.2f} € ({1:.2f} € con IVA)".format(total_factura, total_factura + total_factura * 0.21))
        print("")

    def print_endesa_one_luz(self):
        print('TARIFA ENDESA: ONE LUZ')
        print(' - Total kW {0:.2f}'.format(self.total["total"]))
        suma_consumo = self.total["total"] * self.rates["OneLuz"]["Normal"]["Amount"]
        suma_potencia = self.potencia_contratada * self.rates["OneLuz"]["Normal"]["AmountPotencia"] * self.days / 365
        total_factura = suma_consumo + suma_potencia
        print(" Importe por consumo: {0:.2f} €".format(suma_consumo))
        print(" Importe por potencia: {0:.2f} €".format(suma_potencia))
        print(
            " Total factura: {0:.2f} € ({1:.2f} € con IVA)".format(total_factura, total_factura + total_factura * 0.21))
        print("")

    def print_endesa_one_luz_nocturna(self):
        print('TARIFA ENDESA: ONE LUZ (NOCTURNA)')
        print(' - {0:.2f} total kW Valle y {1:.2f} total kW Punta'.format(
            self.total["Nocturna"]["Valle"], self.total["Nocturna"]["Punta"]
        ))
        total_amount_night_valle = self.total["Nocturna"]["Valle"] * \
                                   self.rates["OneLuz"]["Nocturna"][
                                       "AmountValle"]
        total_amount_night_punta = self.total["Nocturna"]["Punta"] * \
                                   self.rates["OneLuz"]["Nocturna"][
                                       "AmountPunta"]
        print(' - {0:.2f} € total importe consumo en Valle y {1:.2f} € total importe consumo en Punta'.format(
            total_amount_night_valle, total_amount_night_punta))
        suma_consumo = total_amount_night_valle + total_amount_night_punta
        suma_potencia = self.potencia_contratada * self.rates["OneLuz"]["Nocturna"]["AmountPotencia"] * self.days / 365
        total_factura = suma_consumo + suma_potencia
        print(" Importe por consumo: {0:.2f} €".format(suma_consumo))
        print(" Importe por potencia: {0:.2f} €".format(suma_potencia))
        print(
            " Total factura: {0:.2f} € ({1:.2f} € con IVA)".format(total_factura, total_factura + total_factura * 0.21))
        print("")

    def print_endesa_tempo_nocturna(self):
        print('TARIFA ENDESA: TEMPO (NOCTURNA)')
        print(' - {0:.2f} total kW Valle y {1:.2f} total kW Punta'.format(
            self.total["Nocturna"]["Valle"], self.total["Nocturna"]["Punta"]
        ))
        total_amount_night_valle = self.total["Nocturna"]["Valle"] * self.rates["Tempo"]["Nocturna"][
            "AmountValle"]
        total_amount_night_punta = self.total["Nocturna"]["Punta"] * self.rates["Tempo"]["Nocturna"][
            "AmountPunta"]
        sum_tempo = total_amount_night_valle + total_amount_night_punta
        sum_potencia = self.potencia_contratada * self.rates["Tempo"]["Nocturna"]["AmountPotencia"] * self.days / 365
        discount = sum_tempo * self.rates["Tempo"]["Nocturna"]["PercentDiscount"]
        discount_potencia = sum_potencia * self.rates["Tempo"]["Nocturna"]["PercentDiscount"]
        suma_consumo = sum_tempo - discount
        suma_potencia = sum_potencia - discount_potencia
        total_factura = suma_consumo + suma_potencia
        print(' - {0:.2f} € total importe consumo en Valle y {1:.2f} € total importe consumo en Punta'.format(
            total_amount_night_valle, total_amount_night_punta))
        print(" Importe por consumo: {0:.2f} € (Descuento de {1:.2f}% aplicado)".format(suma_consumo,
                                                                                        self.rates["Tempo"][
                                                                                            "Nocturna"][
                                                                                            "PercentDiscount"] * 100))
        print(" Importe por potencia: {0:.2f} (Descuento de {1:.2f}% aplicado)€".format(suma_potencia,
                                                                                        self.rates["Tempo"][
                                                                                            "Nocturna"][
                                                                                            "PercentDiscount"] * 100))
        print(
            " Total factura: {0:.2f} € ({1:.2f} € con IVA)".format(total_factura, total_factura + total_factura * 0.21))
        print("")

    def print_endesa_tempo_super_valle(self):
        print('TARIFA ENDESA: TEMPO (SUPER VALLE)')
        print(' - {0:.2f} total kW SuperValle, {1:.2f} total kW Valle y {2:.2f} total kW Punta'.format(
            self.total["SuperValle"]["SuperValle"], self.total["SuperValle"]["Valle"],
            self.total["SuperValle"]["Punta"]
        ))
        total_amount_super_supervalle = self.total["SuperValle"]["SuperValle"] * \
                                        self.rates["Tempo"]["SuperValle"]["AmountSuperValle"]
        total_amount_super_valle = self.total["SuperValle"]["Valle"] * \
                                   self.rates["Tempo"]["SuperValle"][
                                       "AmountValle"]
        total_amount_super_punta = self.total["SuperValle"]["Punta"] * \
                                   self.rates["Tempo"]["SuperValle"][
                                       "AmountPunta"]
        sum_tempo = total_amount_super_supervalle + total_amount_super_valle + total_amount_super_punta
        sum_potencia = self.potencia_contratada * self.rates["Tempo"]["SuperValle"]["AmountPotencia"] * self.days / 365
        discount = sum_tempo * self.rates["Tempo"]["SuperValle"]["PercentDiscount"]
        discount_potencia = sum_potencia * self.rates["Tempo"]["SuperValle"]["PercentDiscount"]
        suma_consumo = sum_tempo - discount
        suma_potencia = sum_potencia - discount_potencia
        total_factura = suma_consumo + suma_potencia
        print(
            ' - {0:.2f} € total importe consumo en Valle, {1:.2f} € total importe consumo en Valle y {2:.2f} € total importe consumo en Punta'.format(
                total_amount_super_supervalle, total_amount_super_valle, total_amount_super_punta))
        print(" Importe por consumo: {0:.2f} € (Descuento de {1:.2f}% aplicado)".format(suma_consumo,
                                                                                        self.rates["Tempo"][
                                                                                            "SuperValle"][
                                                                                            "PercentDiscount"] * 100))
        print(" Importe por potencia: {0:.2f} (Descuento de {1:.2f}% aplicado)€".format(suma_potencia,
                                                                                        self.rates["Tempo"][
                                                                                            "SuperValle"][
                                                                                            "PercentDiscount"] * 100))
        print(
            " Total factura: {0:.2f} € ({1:.2f} € con IVA)".format(total_factura, total_factura + total_factura * 0.21))
        print("")

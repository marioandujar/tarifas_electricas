# coding=utf-8
class Viesgo:
    def __init__(self, total, rates, potencia_contratada, days):
        self.total = total
        self.rates = rates
        self.potencia_contratada = potencia_contratada
        self.days = days
    
    def print_viesgo_online(self):
        print('TARIFA VIESGO: 100% ONLINE')
        print(' - Total kW {0:.2f}'.format(self.total["total"]))
        suma_consumo = self.total["total"] * self.rates["Online"]["Normal"]["Amount"]
        suma_potencia = self.potencia_contratada * self.rates["Online"]["Normal"]["AmountPotencia"] * self.days / 365
        total_factura = suma_consumo + suma_potencia
        print(" Importe por consumo: {0:.2f} €".format(suma_consumo))
        print(" Importe por potencia: {0:.2f} €".format(suma_potencia))
        print(
            " Total factura: {0:.2f} € ({1:.2f} € con IVA)".format(total_factura, total_factura + total_factura * 0.21))
        print("")
        
    def print_viesgo_online_nocturna(self):
        print('TARIFA VIESGO: 100% ONLINE (NOCTURNA)')
        print(' - {0:.2f} total kW Valle y {1:.2f} total kW Punta'.format(
            self.total["Nocturna"]["Valle"], self.total["Nocturna"]["Punta"]
        ))
        total_amount_night_valle = self.total["Nocturna"]["Valle"] * \
                                   self.rates["Online"]["Nocturna"][
                                       "AmountValle"]
        total_amount_night_punta = self.total["Nocturna"]["Punta"] * \
                                   self.rates["Online"]["Nocturna"][
                                       "AmountPunta"]
        print(' - {0:.2f} € total importe consumo en Valle y {1:.2f} € total importe consumo en Punta'.format(
            total_amount_night_valle, total_amount_night_punta))
        suma_consumo = total_amount_night_valle + total_amount_night_punta
        suma_potencia = self.potencia_contratada * self.rates["Online"]["Nocturna"]["AmountPotencia"] * self.days / 365
        total_factura = suma_consumo + suma_potencia
        print(" Importe por consumo: {0:.2f} €".format(suma_consumo))
        print(" Importe por potencia: {0:.2f} €".format(suma_potencia))
        print(
            " Total factura: {0:.2f} € ({1:.2f} € con IVA)".format(total_factura, total_factura + total_factura * 0.21))
        print("")

class TempProps:
    def __init__(self, start_temperature, grad_temperature, temperature_coefficient):
        self.start_temp = start_temperature
        self.grad_temp = grad_temperature
        self.temp_coeff = temperature_coefficient

    def __str__(self):
        out_str = ""
        out_str += "start temp: " + str(self.start_temp)
        out_str += "\tgrad temp: " + str(self.grad_temp)
        out_str += "\ttemp coefficient: " + str(self.temp_coeff)
        return out_str

    def is_empty(self):
        if self.start_temp == 0 and self.grad_temp == 0 and self.temp_coeff == 0:
            return True
        return False

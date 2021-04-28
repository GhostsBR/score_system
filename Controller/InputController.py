from validate_docbr import CPF
import string
from Controller import StatusController


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class InputControl:
    sc = StatusController.StatusControl
    def verify_inputs(self, fullname, birth, cpf, debt) -> sc:
        if not self.validate_name(fullname):
            return self.sc("Error: Invalid name.", 400)
        if not self.validate_cpf(cpf):
            return self.sc("Error: Invalid cpf.", 400)
        if not self.validade_date(birth):
            return self.sc("Error: Invalid birth.", 400)
        if not self.validade_debt(debt):
            return self.sc("Error: Invalid debt")
        return self.sc("Sucess: valid data!", 200)

    def validate_name(self, fullname) -> bool:
        for i in fullname:
            if not i.lower() in string.ascii_letters and not i == " ":
                return False
        return True

    def validate_cpf(self, cpf) -> bool:
        if CPF().validate(cpf):
            return True
        else:
            return False

    def validade_date(self, date) -> bool:
        date = date.split("/")
        if not len(date) == 3:
            return False
        if not len(date[0]) == 2:
            return False
        if not len(date[1]) == 2:
            return False
        if not len(date[2]) == 4:
            return False
        return True
    
    def validade_debt(self, debt) -> bool:
        if not type(debt) == (float):
            return False
        return True

    def verify_age(self) -> bool:
        pass
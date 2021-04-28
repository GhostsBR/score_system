import pymongo
from datetime import date
from Controller import StatusController
from Controller import InputController
from Controller import ScoreController


class DatabaseControl:
    MYCLIENT = pymongo.MongoClient("mongodb+srv://system:F4vv3EVqUCIkhxFM@cluster0.8fnql.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    SYSTEM = MYCLIENT["server"]

class SystemControl(DatabaseControl):
    sc = StatusController.StatusControl
    users = DatabaseControl.SYSTEM["users"]
    debts = DatabaseControl.SYSTEM["debts"]
    
    def user_register(self, data: dict) -> sc:
        data['cpf'] = data['cpf'].replace("-", "")
        data['cpf'] = data['cpf'].replace(".", "")
        if not type(data) == dict:
            return self.sc("Error: Expected a dict with user data.", 500)
        if not 'fullname' in data:
            return self.sc("Error: User data need has a fullname.", 400)
        if not 'cpf' in data:
            return self.sc("Error: User data need has a cpf.", 400)
        if not 'birth' in data:
            return self.sc("Error: User data need has a birth.", 400)
        if not 'debt' in data:
            return self.sc("Error: User data need has a debt.", 400)
        try:
            data['debt'] = float(data['debt'])
        except:
            return self.sc("Error: Invalid debt value", 200)
        input_verify = InputController.InputControl().verify_inputs(data['fullname'], data['birth'], data['cpf'], data['debt'])
        if input_verify and not input_verify.code == 200:
            return input_verify
        data['score'] = ScoreController.ScoreControl().get_score(data['debt'])
        try:
            self.users.insert_one(data)
        except:
            return self.sc("Error: Cannot insert user in database.", 500)
        return self.sc("Success: User registered with success!", 200)
    
    def user_get(self, cpf) -> sc:
        cpf = cpf.replace("-", "")
        cpf = cpf.replace(".", "")
        if not InputController.InputControl().validate_cpf(cpf):
            return self.sc("Error: Invalid CPF.", 400)
        try:
            result = self.users.find_one({"cpf": cpf}, {"_id": 0})
            if result:
                sepbirht = result['birth'].split("/")
                current_date = date.today()
                birth_date = date(int(sepbirht[2]), int(sepbirht[1]), int(sepbirht[0]))
                time_difference = current_date - birth_date
                if float(time_difference.days) < 6574.5:
                    return self.sc([], 200)
            return self.sc(result, 200)
        except:
            return self.sc("Error: Cannot get user in database." , 400)
    
    def debts_get(self) -> sc:
        result = self.users.find({}, {"_id": 0, "fullname": 1, "debt": 1, "score": 1, "birth": 1})
        results = []
        for i in result:
            current_date = date.today()
            sepbirht = i['birth'].split("/")
            birth_date = date(int(sepbirht[2]), int(sepbirht[1]), int(sepbirht[0]))
            time_difference = current_date - birth_date
            if float(time_difference.days) >= 6574.5:
                results.append(i)
        return self.sc(results, 200)
    
    def debts_update(self, cpf) -> sc:
        cpf = cpf.replace("-", "")
        cpf = cpf.replace(".", "")
        try:
            result = self.users.find_one({"cpf": cpf})
        except:
            return self.sc("Error: Cannot find user in database", 500)
        if not result:
            return self.sc("Error: No user found with this CPF.", 400)
        self.users.update_one({"cpf": cpf}, {"$set": {"score": 1000, "debt": 0}})
        return self.sc("Success: The debt has payed with success", 200)
            

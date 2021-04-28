class ScoreControl:
    def get_score(self, debt) -> int:
        if debt == 0:
            return 1000
        elif debt > 0 and debt <= 100:
            return 900
        elif debt > 100 and debt <= 500:
            return 800
        elif debt > 500 and debt <= 1000:
            return 700
        elif debt > 1000 and debt <= 10000:
            return 600
        elif debt > 10000 and debt <= 50000:
            return 500
        elif debt > 30000 and debt <= 50000:
            return 400
        elif debt > 50000 and debt <= 80000:
            return 300
        elif debt > 80000 and debt <= 100000:
            return 200
        elif debt > 100000 and debt <= 1000000:
            return 100
        elif debt > 1000000:
            return 0


class MovingAverage:
    """A class for calculating simple moving averages"""
    def __init__(self, history = 5):
        self.values = []
        self.history = history
        self.movingaverage = 0

    def reset(self):
        del self.values[:]
        self.movingaverage = 0

    def movingaveragecalc(self, value):
        self.values.append(value)
        if len(self.values) > self.history:
            del self.values[0]
        self.movingaverage = sum(self.values)/len(self.values)


if __name__ == "__main__":
    test = MovingAverage()
    print(test.movingaverage(10))
    print(test.movingaverage(11))
    print(test.movingaverage(12))
    print(test.movingaverage(13))
    print(test.movingaverage(14))
    print(test.movingaverage(17))
    print(test.movingaverage(18))
    print(test.movingaverage(19))
    print(test.movingaverage(20))
    print(test.movingaverage(21))
    print(test.movingaverage(22))
    print(test.movingaverage(23))
    print(test.movingaverage(24))
    print(test.movingaverage(25))
    

    
    

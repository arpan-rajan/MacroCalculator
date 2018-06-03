class Ingredient:
    def __init__(self, amount, unitOfMeasure, item):
        self.amount = amount
        self.unitOfMeasure = unitOfMeasure
        self.item = item
    def __str__(self):
        return "{0} {1} {2}".format(self.amount, self.unitOfMeasure, self.item)
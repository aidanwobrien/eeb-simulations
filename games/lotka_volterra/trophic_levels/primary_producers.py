class PrimaryProducer:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.energy = 1         # 1 = edible, 0 = eaten
        self.regrow_timer = 0   # turns until it regrows

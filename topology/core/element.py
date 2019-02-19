class Element(object):
    """An element."""
    def __init__(self, name=None, symbol=None, mass=None):
        self.name = name
        self.symbol = symbol
        self.mass = mass

Hydrogen = Element(name='hydrogen', symbol='H', mass=1.007947)
Carbon = Element(name='carbon', symbol='C', mass=12.011)
Oxygen = Element(name='oxygen', symbol='O', mass=15.999)

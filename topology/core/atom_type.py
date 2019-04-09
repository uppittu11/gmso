import warnings
import unyt as u

from topology.utils.testing import allclose
from topology.core.potential import Potential


class AtomType(Potential):
    """An atom type, inheriting from the Potential class.

    AtomType represents an atom type and includes the functional form
    describing its interactions and, optionally, other properties such as mass
    and charge.  This class inhereits from Potential, which stores the
    non-bonded interaction between atoms or sites. The functional form of the
    potential is stored as a `sympy` expression and the parameters, with units,
    are stored explicitly.

    Parameters
    ----------
    name : str, default="AtomType"
        The name of the potential.
    mass : unyt.unyt_quantity, optional, default=0.0 * unyt.g / u.mol
        The mass of the atom type.
    charge : unyt.unyt_quantity, optional, default=0.0 * unyt.elementary_charge
        The charge of the atom type.
    expression : str or sympy.Expr,
                 default='4*epsilon*((sigma/r)**12 - (sigma/r)**6)',
        The mathematical expression describing the functional form of the
        potential describing this atom type, i.e. a Lennard-Jones potential.
        The default value is a 12-6 Lennard-Jones potential.
    parameters : dict of str : unyt.unyt_quantity pairs,
        default={'sigma': 0.3 * u.nm, 'epsilon': 0.3 * u.Unit('kJ')},
        The parameters of the potential describing this atom type and their
        values, as unyt quantities.
    independent_variables : str, sympy.Symbol, or list-like of str, sympy.Symbol
        The independent variables of the functional form previously described.
    atomclass : str, default=''
        The class of the atomtype
    doi : str
        Digital Object Identifier of publication where this atom type was specified
    desc : str
        Simple description of the atom type
    overrides : set of str
        Set of other atom types that this atom type overrides
    definition : str
        SMARTS string defining this atom type

    """

    def __init__(self,
                 name='AtomType',
                 mass=0.0 * u.gram / u.mol,
                 charge=0.0 * u.elementary_charge,
                 expression='4*epsilon*((sigma/r)**12 - (sigma/r)**6)',
                 parameters={
                    'sigma': 0.3 * u.nm,
                    'epsilon': 0.3 * u.Unit('kJ')},
                 independent_variables={'r'},
                 atomclass='', doi='', overrides=set(), definition=''):

        super(AtomType, self).__init__(
            name=name,
            expression=expression,
            parameters=parameters,
            independent_variables=independent_variables)
        self._mass = _validate_mass(mass)
        self._charge = _validate_charge(charge)
        self._atomclass = _validate_str(atomclass)
        self._doi = _validate_str(doi)
        self._overrides = _validate_set(overrides)
        self._definition = _validate_str(definition)

        self._validate_expression_parameters()

    @property
    def charge(self):
        return self._charge

    @charge.setter
    def charge(self, val):
        self._charge = _validate_charge(val)

    @property
    def mass(self):
        return self._mass

    @mass.setter
    def mass(self, val):
        self._mass = _validate_mass(val)

    @property
    def atomclass(self):
        return self._atomclass

    @atomclass.setter
    def atomclass(self, val):
        self._atomclass = val

    def __eq__(self, other):
        name_match = (self.name == other.name)
        charge_match = allclose(
            self.charge,
            other.charge,
            atol=1e-6 * u.elementary_charge,
            rtol=1e-5 * u.elementary_charge)
        mass_match = allclose(
            self.mass,
            other.mass,
            atol=1e-6 * u.gram / u.mol,
            rtol=1e-5 * u.gram / u.mol)
        parameter_match = (self.parameters == other.parameters)
        expression_match = (self.expression == other.expression)
        atomclass_match = (self.atomclass == other.atomclass)

        return all([
            name_match, charge_match, mass_match, parameter_match,
            expression_match, atomclass_match
        ])

    def __repr__(self):
        desc = "<AtomType {}, id {}>".format(self._name, id(self))
        return desc


def _validate_charge(charge):
    if not isinstance(charge, u.unyt_array):
        warnings.warn("Charges are assumed to be elementary charge")
        charge *= u.elementary_charge
    elif charge.units.dimensions != u.elementary_charge.units.dimensions:
        warnings.warn("Charges are assumed to be elementary charge")
        charge = charge.value * u.elementary_charge
    else:
        pass

    return charge


def _validate_mass(mass):
    if not isinstance(mass, u.unyt_array):
        warnings.warn("Masses are assumed to be g/mol")
        mass *= u.gram / u.mol
    elif mass.units.dimensions != (u.gram / u.mol).units.dimensions:
        warnings.warn("Masses are assumed to be g/mol")
        mass = mass.value * u.gram / u.mol
    else:
        pass

    return mass

def _validate_str(val):
    if not isinstance(val, str):
        raise ValueError("Passed value {} is not a string".format(val))
    return val

def _validate_set(val):
    if not isinstance(val, set):
        raise ValueError("Passed value {} is not a set".format(val))
    if not all([isinstance(char, str) for char in val]):
        raise ValueError("Passed overrides of non-string to overrides")
    return val

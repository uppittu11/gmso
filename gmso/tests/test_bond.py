import pytest

from gmso.core.topology import Topology
from gmso.core.bond import Bond
from gmso.core.atom_type import AtomType
from gmso.core.bond_type import BondType
from gmso.core.site import Site
from gmso.tests.base_test import BaseTest
from gmso.exceptions import GMSOError


class TestBond(BaseTest):
    def test_bond_nonparametrized(self):
        site1 = Site(name='site1')
        site2 = Site(name='site2')

        assert site1.n_connections == 0
        assert site2.n_connections == 0

        connect = Bond(connection_members=[site1, site2])

        assert site1.n_connections == 1
        assert site2.n_connections == 1
        assert connect.connection_type is None

    def test_bond_parametrized(self):
        site1 = Site(name='site1')
        site2 = Site(name='site2')

        assert site1.n_connections == 0
        assert site2.n_connections == 0
        bond_type = BondType()

        connect = Bond(connection_members=[site1, site2],
                       connection_type=bond_type,
                       name='bond_name')

        assert site1.n_connections == 1
        assert site2.n_connections == 1
        assert len(connect.connection_members) == 2
        assert connect.connection_type is not None
        assert connect.name == 'bond_name'

    def test_bond_fake(self):
        site1 = Site(name='site1')
        site2 = Site(name='site2')
        with pytest.raises(GMSOError):
            Bond(connection_members=['fakesite1', 'fakesite2'])

    def test_bond_fake_bondtype(self):
        site1 = Site(name='site1')
        site2 = Site(name='site2')
        with pytest.raises(GMSOError):
            Bond(connection_members=[site1, site2],
                 connection_type='Fake bondtype')

    def test_bond_constituent_types(self):
        site1 = Site(name='site1', position=[0,0,0], atom_type=AtomType(name='A'))
        site2 = Site(name='site2', position=[1,0,0], atom_type=AtomType(name='B'))
        bondtype = BondType(member_types=[site1.atom_type.name, site2.atom_type.name])
        bond = Bond(connection_members=[site1, site2], connection_type=bondtype)
        assert 'A' in bond.connection_type.member_types
        assert 'B' in bond.connection_type.member_types

    def test_bond_eq(self):
        site1 = Site(name='site1', position=[0, 0, 0])
        site2 = Site(name='site2', position=[1, 1, 1])

        ref_connection = Bond(
            connection_members=[site1, site2],
        )

        same_connection = Bond(
            connection_members=[site1, site2],
        )

        diff_connection = Bond(
            connection_members=[site1, site2],
        )

        assert ref_connection != same_connection
        assert ref_connection != diff_connection

    def test_add_equivalent_connections(self):
        site1 = Site(name="SiteA")
        site2 = Site(name="SiteB")

        bond = Bond([site1, site2])
        bond_eq = Bond([site2, site1])

        top = Topology()
        top.add_connection(bond)
        top.add_connection(bond_eq)
        assert top.n_bonds == 1

    def test_equivalent_members_set(self):
        site1 = Site(name="SiteA")
        site2 = Site(name="SiteB")

        bond = Bond([site1, site2])
        bond_eq = Bond([site2, site1])

        assert (tuple(bond_eq.connection_members)
                in bond.equivalent_members())
        assert (tuple(bond.connection_members)
                in bond_eq.equivalent_members())


import unyt as u
import numpy as np
import pytest

from gmso.core.box import Box
from gmso.external.convert_openmm import to_openmm
from gmso.tests.base_test import BaseTest
from gmso.utils.io import import_, has_openmm, has_simtk_unit
from unyt.testing import assert_allclose_units

if has_openmm and has_simtk_unit:
    simtk_unit = import_('simtk.unit')

@pytest.mark.skipif(not has_openmm, reason="OpenMM is not installed")
@pytest.mark.skipif(not has_simtk_unit, reason="SimTK is not installed")
class TestOpenMM(BaseTest):
    def test_openmm_modeller(self, typed_ar_system):
        to_openmm(typed_ar_system, openmm_object='modeller')

    def test_openmm_topology(self, typed_ar_system):
        to_openmm(typed_ar_system, openmm_object='topology')

    def test_n_atoms(self, typed_ar_system):
        n_topology_sites = len(typed_ar_system.sites)
        modeller = to_openmm(typed_ar_system, openmm_object='modeller')
        n_modeller_atoms = len([i for i in modeller.topology.atoms()])

        assert n_topology_sites == n_modeller_atoms

    def test_box_dims(self, typed_ar_system):
        n_topology_sites = len(typed_ar_system.sites)
        omm_top = to_openmm(typed_ar_system)
        topology_lengths = typed_ar_system.box.lengths
        omm_lengths = omm_top.getUnitCellDimensions()

        assert_allclose_units(topology_lengths.value, omm_lengths._value, rtol=1e-5, atol=1e-8)

    def test_particle_positions(self, typed_ar_system):
        typed_ar_system.sites[0].position = (1,1,1) * u.nanometer
        omm_top = to_openmm(typed_ar_system, openmm_object='modeller')

        assert_allclose_units(omm_top.positions._value,
                typed_ar_system.positions.value, rtol=1e-5, atol=1e-8)

    def test_position_units(self, typed_ar_system):
        typed_ar_system.box = Box(lengths=[1,1,1])

        n_topology_sites = len(typed_ar_system.sites)
        omm_top = to_openmm(typed_ar_system, openmm_object='modeller')

        assert isinstance(omm_top.positions.unit, type(simtk_unit.nanometer))

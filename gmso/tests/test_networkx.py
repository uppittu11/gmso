import pytest

from gmso.formats.networkx import (highlight_networkx_edges, plot_networkx_atomtypes,
plot_networkx_bonds, select_params_on_networkx, get_networkx_edges, identify_labels,
show_parameter_values, interactive_networkx_atomtypes, interactive_networkx_bonds,
interactive_networkx_angles, interactive_networkx_dihedrals, select_dihedrals_from_sites,
plot_networkx_nodes, plot_networkx_params, select_edges_on_networkx,
report_parameter_expression)
from gmso.formats.networkx import _get_formatted_atom_types_names_for

from gmso.tests.base_test import BaseTest
from gmso.utils.io import import_, has_networkx, has_pyplot
from gmso.external.convert_networkx import to_networkx

if has_networkx:
    networkx = import_('networkx')

if has_pyplot:
    plt = import_('matplotlib.pyplot')

@pytest.mark.skipif(not has_networkx, reason="Networkx is not installed")
@pytest.mark.skipif(not has_pyplot, reason="Matplotlib.pyplot is not installed")
class TestNetworkx(BaseTest):
    def test_highlight_networkx_edges(self, typed_ethane):
        list(typed_ethane.angles)[0].angle_type = None
        list(typed_ethane.dihedrals)[0].dihedral_type = None
        
        graph = to_networkx(typed_ethane)
        list_edges = list(graph.edges)[0:3] 
        test_edge_weights, test_edge_colors = highlight_networkx_edges(graph, list_edges[0:2])
        assert test_edge_weights[list_edges[0]] == 5
        assert test_edge_weights[list_edges[1]] == 5
        assert test_edge_weights[list_edges[2]] == 1
        assert test_edge_colors[list_edges[0]] == 'r'
        assert test_edge_colors[list_edges[1]] == 'r'
        assert test_edge_colors[list_edges[2]] == 'k'
  

    def test_plot_networkx_atomtypes(self,typed_ethane):
        fig, ax = plot_networkx_atomtypes(typed_ethane,atom_name=None)
        test_fig, test_ax = plt.subplots(1)
        
        assert isinstance(fig, test_fig.__class__)
        assert isinstance(ax, test_ax.__class__)

    def test_plot_networkx_bonds(self,typed_ethane):
        graph = to_networkx(typed_ethane)
        fig, ax = plot_networkx_bonds(graph)
        test_fig, test_ax = plt.subplots(1)

        assert isinstance(fig, test_fig.__class__)
        assert isinstance(ax, test_ax.__class__)

    def test_select_params_on_networkx(self,typed_ethane):
        graph = to_networkx(typed_ethane)
        assert len(select_params_on_networkx(graph,[None,None,None,None])) == 0
        assert len(select_params_on_networkx(graph,['C','H','H'])) == 1
        assert len(select_params_on_networkx(graph,['C','C','H','H'])) == 1
        assert len(select_params_on_networkx(graph,[None,None,None])) == 0
        assert len(select_params_on_networkx(graph,['C','H',None])) == 2
        assert len(select_params_on_networkx(graph,['C',None,None])) == 3
        assert len(select_params_on_networkx(graph,['C','C','H', None])) == 1
        assert len(select_params_on_networkx(graph,['C','C', None, None])) == 1

    def test__get_formatted_atom_types_names_for(self,typed_ethane):
        graph = to_networkx(typed_ethane)
        for node, dihedrals in graph.nodes(data='angles'):
            assert isinstance(_get_formatted_atom_types_names_for(dihedrals[0]),str)

    def test_get_networkx_edges(self,typed_ethane,capsys):
        assert len(get_networkx_edges([list(typed_ethane.dihedrals[0].connection_members)])) == 6
        assert len(get_networkx_edges([list(typed_ethane.angles[0].connection_members)])) == 4

    def test_identify_labels(self,typed_ethane):
        graph = to_networkx(typed_ethane)
        assert len(identify_labels(graph,['name'],atom_name = 'C')) == 2

    def test_show_parameter_values(self,typed_ethane):
        parameters = list(typed_ethane.angles[0].connection_members[0:2])
        with pytest.raises(ValueError):
            show_parameter_values(typed_ethane, [parameters], True) 

    def test_interactive_networkx_atomtypes(self,typed_ethane,capsys):
        interactive_networkx_atomtypes(typed_ethane)
        captured, err = capsys.readouterr()
        assert isinstance(err,str)

    def test_interactive_networkx_bonds(self,typed_ethane,capsys):
        interactive_networkx_bonds(typed_ethane)
        captured, err = capsys.readouterr()
        assert isinstance(err,str)

    def test_interactive_networkx_angles(self,typed_ethane,capsys):
        interactive_networkx_angles(typed_ethane)
        captured, err = capsys.readouterr()
        assert isinstance(err,str)

    def test_interactive_networkx_dihedrals(self,typed_ethane,capsys):
        interactive_networkx_dihedrals(typed_ethane)
        captured, err = capsys.readouterr()
        assert isinstance(err,str)

    def test_select_dihedrals_from_sites(self,typed_ethane,capsys):
        graph = to_networkx(typed_ethane)
        select_dihedrals_from_sites(graph,typed_ethane)
        captured,err = capsys.readouterr()
        assert isinstance(err,str)

    def test_select_dihedrals_from_sites(self,typed_ethane,capsys):
        graph = to_networkx(typed_ethane)
        select_dihedrals_from_sites(graph,typed_ethane)
        captured, err = capsys.readouterr()
        assert isinstance(err,str)

    def test_plot_networkx_nodes(self,typed_ethane):
        graph = to_networkx(typed_ethane)
        fig, ax = plt.subplots(1,1)
        plot_networkx_nodes(graph,ax,edge_weights = {1:5}, 
                            edge_colors = {1:'r'})

    def test_plot_networkx_params(self,typed_ethane):
        graph = to_networkx(typed_ethane)
        list_of_edges = get_networkx_edges(list_of_params = [typed_ethane.dihedrals[0].connection_members,
                                           typed_ethane.dihedrals[1].connection_members])
        fig, ax = plot_networkx_params(graph, list_of_edges)
        test_fig, test_ax = plt.subplots(1)

        assert isinstance(fig, test_fig.__class__)
        assert isinstance(ax, test_ax.__class__)

    def test_select_edges_on_networkx(self,typed_ethane,capsys):
        graph = to_networkx(typed_ethane)
        edges = select_params_on_networkx(graph, ['C','C','H'])
        select_edges_on_networkx(graph,typed_ethane, edges[0][1])
        captured, err = capsys.readouterr()
        assert isinstance(err,str)

    def test_report_parameter_expression(self,typed_ethane,capsys):
        report_parameter_expression(typed_ethane,list(typed_ethane.dihedrals[0].connection_members))
        report_parameter_expression(typed_ethane,list(typed_ethane.angles[0].connection_members))
        captured, err = capsys.readouterr()
        assert isinstance(err,str)

import json
from pathlib import Path

from gmso.abc.abstract_potential import AbstractPotential
from gmso.utils.singleton import Singleton
from gmso.exceptions import GMSOError

POTENTIAL_JSONS = list(Path(__file__).parent.glob('jsons/*.json'))
JSON_DIR = Path.joinpath(Path(__file__).parent, 'jsons')


def _verify_potential_template_keys(_dict, name):
    assert 'name' in _dict, f"Key name not found in the potential template {name}.json"
    assert 'expression' in _dict, f"Key expression not found in the potential template {name}.json"
    assert 'independent_variables' in _dict, f"Key independent_variables not found in the potential template {name}.json"
    if str(name) != _dict['name']:
        raise GMSOError(f'Mismatch between Potential name {name} and {_dict["name"]}')


def _load_template_json(item, json_dir=JSON_DIR):
    with json_dir.joinpath(f'{item}.json').open('r') as json_file:
        potential_dict = json.load(json_file)
        _verify_potential_template_keys(potential_dict, item)
        return potential_dict


class PotentialTemplate(AbstractPotential):
    def __init__(self,
                 name='PotentialTemplate',
                 expression='4*epsilon*((sigma/r)**12 - (sigma/r)**6)',
                 independent_variables='r',
                 template=True):
        if not isinstance(independent_variables, set):
            independent_variables = set(independent_variables.split(','))

        super(PotentialTemplate, self).__init__(
            name=name,
            expression=expression,
            independent_variables=independent_variables,
        )

    def set_expression(self, *args, **kwargs):
        raise NotImplementedError

    class Config:
        allow_mutation = False


class PotentialTemplateLibrary(Singleton):
    """A singleton collection of all the potential templates"""

    def __init__(self):
        try:
            self.json_refs
        except AttributeError:
            self.json_refs = POTENTIAL_JSONS
            potential_names = [pot_json.name for pot_json in POTENTIAL_JSONS]
            self._ref_dict = {potential.replace('.json', ''): None for potential in potential_names}
            self._user_ref_dict = {}

    def get_available_template_names(self):
        return tuple(self._ref_dict.keys())

    def __getitem__(self, item):
        if item not in self._ref_dict:
            raise KeyError(f'Potential Template {item} not found.')

        return self._load_from_json(item)

    def _load_from_json(self, item):
        if self._ref_dict[item] is None:
            potential_dict = _load_template_json(item, JSON_DIR)
            self._ref_dict[item] = PotentialTemplate(**potential_dict)
        return self._ref_dict[item]

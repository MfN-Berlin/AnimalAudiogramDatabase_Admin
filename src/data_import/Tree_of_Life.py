"""
API queries.
* Implements the template method pattern
* Connects to the Tree of Life API

Ticket see:
https://code.naturkundemuseum.berlin/Alvaro.Ortiz/Pinguine/issues/79

Created on 06.02.2020
@author: Alvaro.Ortiz for Museum fuer Naturkunde Berlin
"""

import abc
import urllib.parse
import requests
import json
import objectpath
import traceback


class Tree_of_Life(abc.ABC):
    """Base class for Tree of Life queries called during data import."""

    BASE_URL = "https://api.opentreeoflife.org/v3/"

    def run(self, param):
        results = self._run(param)
        return results

    @abc.abstractmethod
    def _run(self, id=None):
        pass

    def send_request(self, url, data):
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json.dumps(data), headers=headers)
        return response.json()


class Obtain_OTT_ID(Tree_of_Life):
    """Get the ott id for a given scientific name."""

    def _run(self, param):
        """
        Calls Tree of Life API taxonomy name resolution (tnrs) service,
        match_names with the species name given in param

        @param param String, scientific name of a species.
        @return int ott id
        """
        response_json = None
        try:
            url = urllib.parse.urljoin(
                Tree_of_Life.BASE_URL, "tnrs/match_names")
            name_array = []
            name_array.append(param)
            data = {'names': name_array, "do_approximate_matching": False}
            response_json = self.send_request(url, data)
            ott_id = response_json['results'][0]['matches'][0]['taxon']['ott_id']
            return ott_id
        except:
            # print(response_json)
            traceback.format_exc()
            return 'NA'


class Obtain_Lineage(Tree_of_Life):
    """Get genus, family order and class by ott_id"""
    tree_obj = None

    def _run(self, param):
        """
        Calls Tree of Life API taxon_info with the ott id species given in param

        @param param String, ott id of a species.
        @return dict{'species':String, 'genus':String, 'family':String, 'order':String, 'class':String}
        """
        url = urllib.parse.urljoin(
            Tree_of_Life.BASE_URL, "taxonomy/taxon_info")
        data = {'ott_id': param, "include_lineage": True}
        response_json = self.send_request(url, data)

        # use objectpath to search the tree for interesting taxa
        self.tree_obj = objectpath.Tree(response_json)
        lineage = dict()
        lineage['unique_name'] = self.tree_obj.execute("$.*['unique_name']")
        lineage['subspecies'] = self._get_taxon_by_rank("subspecies")
        lineage['species'] = self._get_taxon_by_rank("species")
        lineage['genus'] = self._get_taxon_by_rank("genus")
        lineage['family'] = self._get_taxon_by_rank("family")
        lineage['order'] = self._get_taxon_by_rank("order")
        lineage['class'] = self._get_taxon_by_rank("class")
        lineage['phylum'] = self._get_taxon_by_rank("phylum")
        return lineage

    def _get_taxon_by_rank(self, rank):
        """Search the tree for entry with given rank name (e.g. 'genus')"""
        obj_name = tuple(self.tree_obj.execute(
            '$..*[@.rank is "%s"]["name"]' % rank))
        if obj_name:
            name = obj_name[0]
            ott_id = tuple(self.tree_obj.execute(
                '$..*[@.rank is "%s"]["ott_id"]' % rank))[0]
            return {'name': name, 'ott_id': ott_id}
        else:
            return None

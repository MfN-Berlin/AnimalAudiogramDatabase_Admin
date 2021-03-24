"""
API queries.
* Implements the template method pattern
* Connects to the Wikidata API to get vernacular names

Ticket see:
https://code.naturkundemuseum.berlin/Alvaro.Ortiz/Pinguine/issues/79

Created on 06.02.2020
@author: Alvaro.Ortiz for Museum fuer Naturkunde Berlin
"""
import abc
import urllib.parse
import requests
import json
import traceback


class Wikidata(abc.ABC):
    """Base class for Wikidata queries called during data import."""
    WIKIPEDIA_BASE_URL = "https://en.wikipedia.org/w/api.php"
    WIKIDATA_BASE_URL = "https://www.wikidata.org/w/api.php"

    known_taxa = {
        'Lipotes vexillifer': {
            'ott_id': 5269,
            'vernacular_name_english': "Baiji",
            'vernacular_name_german': "Chinesischer Flussdelfin"},
        'Mesoplodon densirostris': {
            'ott_id': 6470,
            'vernacular_name_english': "Blainville's beaked whale",
            'vernacular_name_german': "Blainville-Schnabelwal"},
        'Zalophus californianus': {
            'ott_id': 95364,
            'vernacular_name_english': "California sea lion",
            'vernacular_name_german': "Kalifornischer Seelöwe"},
        'Globicephala melas': {
            'ott_id': 124212,
            'vernacular_name_english': "Long-finned pilot whale",
            'vernacular_name_german': "Grindwal"},
        'Orcinus orca': {
            'ott_id': 124215,
            'vernacular_name_english': "Orca",
            'vernacular_name_german': "Schwertwal"},
        'Stenella coeruleoalba': {
            'ott_id': 124224,
            'vernacular_name_english': "Striped dolphin",
            'vernacular_name_german': "Blau-Weißer Delfin"},
        'Tursiops truncatus': {
            'ott_id': 124230,
            'vernacular_name_english': "Common bottlenose dolphin",
            'vernacular_name_german': "Großer Tümmler"},
        'Grampus griseus': {
            'ott_id': 154711,
            'vernacular_name_english': "Risso's dolphin",
            'vernacular_name_german': "Rundkopfdelfin"},
        'Pusa hispida': {
            'ott_id': 175251,
            'vernacular_name_english': "Ringed seal",
            'vernacular_name_german': "Ringelrobbe"},
        'Mirounga angustirostris': {
            'ott_id': 175268,
            'vernacular_name_english': "Northern elephant seal",
            'vernacular_name_german': "Nördlicher See-Elefant"},
        'Neomonachus schauinslandi': {
            'ott_id': 180367,
            'vernacular_name_english': "Hawaiian monk seal",
            'vernacular_name_german': "Hawaii-Mönchsrobbe"},
        'Sousa chinensis': {
            'ott_id': 187220,
            'vernacular_name_english': "Chinese white dolphin",
            'vernacular_name_german': "Chinesischer Weißer Delfin"},
        'Pseudorca crassidens': {
            'ott_id': 209644,
            'vernacular_name_english': "False killer whale",
            'vernacular_name_german': "Kleiner Schwertwal"},
        'Trichechus manatus': {
            'ott_id': 226178,
            'vernacular_name_english': "West Indian manatee",
            'vernacular_name_german': "Karibik-Manati"},
        'Trichechus inunguis': {
            'ott_id': 226185,
            'vernacular_name_english': "Amazonian manatee",
            'vernacular_name_german': "Amazonas-Manati"},
        'Tursiops aduncus': {
            'ott_id': 257323,
            'vernacular_name_english': "Indo-Pacific bottlenose dolphin",
            'vernacular_name_german': "Indopazifischer Großer Tümmler"},
        'Sotalia fluviatilis': {
            'ott_id': 336231,
            'vernacular_name_english': "Tucuxio",
            'vernacular_name_german': "Amazonas-Sotalia"},
        'Phoca vitulina vitulina': {
            'ott_id': 553449,
            'vernacular_name_english': "Harbour seal (subsp. vitulina)",
            'vernacular_name_german': "Seehund (Unterart vitulina)"},
        'Phoca groenlandica': {
            'ott_id': 664062,
            'vernacular_name_english': "Harp seal",
            'vernacular_name_german': "Sattelrobbe"},
        'Inia geoffrensis': {
            'ott_id': 698411,
            'vernacular_name_english': "Amazon river dolphin",
            'vernacular_name_german': "Amazonasdelfin"},
        'Phoca vitulina': {
            'ott_id': 698422,
            'vernacular_name_english': "Harbour seal",
            'vernacular_name_german': "Seehund"},
        'Odobenus rosmarus': {
            'ott_id': 749644,
            'vernacular_name_english': "Walrus",
            'vernacular_name_german': "Walross"},
        'Trichechus manatus latirostris': {
            'ott_id': 816446,
            'vernacular_name_english': "West Indian manatee, subsp. latirostris",
            'vernacular_name_german': "Karibik-Manati, unterart latirostris"},
        'Phocoena phocoena': {
            'ott_id': 851312,
            'vernacular_name_english': "Harbour porpoise",
            'vernacular_name_german': "Gewöhnlicher Schweinswal"},
        'Delphinapterus leucas': {
            'ott_id': 851318,
            'vernacular_name_english': "Beluga whale",
            'vernacular_name_german': "Weißwal"},
        'Callorhinus ursinus': {
            'ott_id': 949693,
            'vernacular_name_english': "Northern fur seal",
            'vernacular_name_german': "Nördlicher Seebär"},
        'Halichoerus grypus': {
            'ott_id': 1040694,
            'vernacular_name_english': "Grey seal",
            'vernacular_name_german': "Kegelrobbe"},
        'Globicephala macrorhynchus': {
            'ott_id': 535886,
            'vernacular_name_english': "Short-finned pilot whale",
            'vernacular_name_german': "Kurzflossen-Grindwal"},
        'Phalacrocorax carbo': {
            'ott_id': 969841,
            'vernacular_name_english': "Great cormorant",
            'vernacular_name_german': "Kormoran"},
        'Phalacrocorax carbo sinensis': {
            'ott_id': 5859705,
            'vernacular_name_english': "Great cormorant subsp. sinensis",
            'vernacular_name_german': "Kormoran, Unterart sinensis"},
        'Neophocaena asiaeorientalis asiaeorientalis': {
            'ott_id': 5846401,
            'vernacular_name_english': "Narrow-ridged finless porpoise, subsp. asiaeorientalis",
            'vernacular_name_german': "Östlicher Glattschweinswal, Unterart asiaeorientalis"},
        'Eumetopias jubatus': {
            'ott_id': 949686,
            'vernacular_name_english': "Steller's sea lion",
            'vernacular_name_german': "Stellerscher Seelöwe"},
        'Sciaena umbra': {
            'ott_id': 3634399,
            'vernacular_name_english': "Brown meagre",
            'vernacular_name_german': "Meerrabe"},
        'Eretmochelys imbricata': {
            'ott_id': 430337,
            'vernacular_name_english': "Hawksbill sea turtle",
            'vernacular_name_german': "Echte Karettschildkröte"},
        'Caretta caretta': {
            'ott_id': 392505,
            'vernacular_name_english': "Loggerhead sea turtle",
            'vernacular_name_german': "Unechte Karettschildkröte"},
        'Enhydra lutris': {
            'ott_id': 949676,
            'vernacular_name_english': "Sea otter",
            'vernacular_name_german': "Seeotter"}
    }

    def run(self, taxon_name):
        results = self._run(taxon_name)
        return results

    @abc.abstractmethod
    def _run(self, taxon_name=None):
        pass

    def send_request(self, url, data=None):
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json.dumps(data), headers=headers)
        return response.json()


class Obtain_Wikibase_Item_ID(Wikidata):
    """Get the wikibase item id for a given term."""

    def _run(self, taxon_name):
        """
        Calls Wikipedia API service,
        match page title with the species name given in param

        @param taxon_name String, latin name
        @return String wikibase_item id
        """
        try:
            # get the page id, resolving redirects
            url = urllib.parse.urljoin(Wikidata.WIKIPEDIA_BASE_URL,
                                       "?action=query&prop=redirects&titles=%s&format=json&redirects=true" % taxon_name)
            response_json = self.send_request(url)
            page_id = None
            for k in response_json['query']['pages']:
                page_id = str(k)
                break
            if page_id is None:
                raise Exception("no key found for %s" % param)

            # get the wikibase_item id
            url = urllib.parse.urljoin(Wikidata.WIKIPEDIA_BASE_URL,
                                       "?action=query&prop=pageprops&pageids=%s&format=json" % page_id)
            response_json = self.send_request(url)
            wikibase_item = response_json['query']['pages'][page_id]['pageprops']['wikibase_item']
            return wikibase_item

        except Exception:
            print("Could not get wikibase item for %s" % param)


class Obtain_Vernacular_Name(Wikidata):
    """Get the vernacular name for a given wikibase_item id"""

    def _run(self, taxon_name):
        """
        Calls Wikidata API service,
        match page entity labels with the wikibase term id name given in param

        @param taxon_name String, latin name
        @return dict vernacular names in German and English
        """
        labels = dict()
        # get taxon name from known_taxa array
        if taxon_name in Wikidata.known_taxa:
            labels['de'] = Wikidata.known_taxa[taxon_name]['vernacular_name_german']
            labels['en'] = Wikidata.known_taxa[taxon_name]['vernacular_name_english']
            return labels
        # get taxon names from Wikidata
        else:
            wd_id = Obtain_Wikibase_Item_ID().run(taxon_name)
            url = urllib.parse.urljoin(Wikidata.WIKIDATA_BASE_URL,
                                       "?action=wbgetentities&props=labels&ids=%s&languages=de|en&format=json" % wd_id)
            response_json = None
            try:
                response_json = self.send_request(url)
                labels['de'] = response_json['entities'][wd_id]['labels']['de']['value']
                labels['en'] = response_json['entities'][wd_id]['labels']['en']['value']
                return labels
            except:
                print(response_json)
                traceback.format_exc()
                return 'NA'

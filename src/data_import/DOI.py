"""
API queries.
* Implements the template method pattern
* Connects to the DOI API to get bibliographical information

Ticket see:
https://code.naturkundemuseum.berlin/Alvaro.Ortiz/Pinguine/issues/80

Content-negociation
@see: https://citation.crosscite.org/docs.html

BibTeX parser
@see: https://bibtexparser.readthedocs.io/en/master/tutorial.html#parse-a-string

Created on 12.02.2020
@author: Alvaro.Ortiz for Museum fuer Naturkunde Berlin
"""
import abc
import urllib.parse
import requests
import bibtexparser
from bibtexparser.customization import convert_to_unicode


class DOI(abc.ABC):
    """Base class for DOI queries called during data import."""
    BASE_URL = "http://dx.doi.org/"

    def run(self, param):
        results = self._run(param)
        return results

    @abc.abstractmethod
    def _run(self, id=None):
        pass

    def send_request(self, url, headers):
        response = requests.post(url, headers=headers)
        if response.status_code != 200:
            raise Exception("Error %d getting %s" %
                            (response.status_code, url))
        return response.text.strip()


class Obtain_Bibtex(DOI):
    """Get BibTeX data for a given DOI."""

    def _run(self, param):
        """
        Calls DOI.org REST API service,
        gets matching BibTeX information for the DOI given in param

        @param param String, DOI to search
        @return String, bibliographical information in BibTeX format
        """
        url = urllib.parse.urljoin(DOI.BASE_URL, param)
        headers = {'Accept': "text/bibliography;style=bibtex"}
        bibtex = self.send_request(url, headers)

        return bibtex


class Obtain_Citation(DOI):
    """Get APA citation for a given DOI."""

    def _run(self, param):
        """
        Calls DOI.org REST API service,
        gets matching APA citation for the DOI given in param

        @param param String, DOI to search
        @return String, citation in APA format
        """
        url = urllib.parse.urljoin(DOI.BASE_URL, param)
        headers = {'Accept': "text/bibliography;style=apa"}
        citation = self.send_request(url, headers)
        # Name ist falsch eingetragen beim Journal
        citation = citation.replace('Gotz', 'Götz')
        citation = citation.replace('Ã¢Â€Â“', '-')
        return citation


class Obtain_Citation_Short(DOI):
    """Get short citation for a given DOI."""

    def _run(self, param):
        """
        Calls DOI.org REST API service,
        returns matching short citation for the DOI given in param

        @param param String, DOI to search
        @return String, citation in short format
        """
        bibtex = Obtain_Bibtex().run(param)
        bibtexparser.customization = convert_to_unicode

        # Name ist falsch eingetragen beim Journal
        bibtex = bibtex.replace('Gotz', 'Götz')

        bib_dict = bibtexparser.loads(bibtex)
        author_str = bib_dict.entries[0]['author']
        if "and" in author_str:
            authors = author_str.split(' and ')
            for i in range(0, len(authors)):
                authors[i] = authors[i].split(',')[0].strip()
                if len(authors) <= 3:
                    author_str = ', '.join(authors)
                    # replace last comma by &
                    author_str = author_str[::-1].replace(" ,", " & ", 1)[::-1]
                else:
                    author_str = "%s et al." % authors[0]
        else:
            author_str = author_str.split(',')[0].strip()

        year_str = str(bib_dict.entries[0]['year'])
        return "%s, %s" % (author_str, year_str)

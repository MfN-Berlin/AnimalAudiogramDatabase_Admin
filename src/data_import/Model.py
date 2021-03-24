# -*- coding: utf-8 -*-
'''
Created on 28.11.2019
Convert audiogram data from a spreadsheet into SQL
@author: Alvaro Ortiz for Museum fuer Naturkunde Berlin
'''


class Model:

    def __init__(self):
        # Parse this from the file audiogram_data/audiogrambase_import_methods.csv
        self.methods = [
            {'id': 1,
             'category_level': 1, 'denomination': "behavioral"},
            {'id': 2,
             'category_level': 2, 'denomination': "go - no go", 'parent_method_id': 1},
            {'id': 3,
             'category_level': 2, 'denomination': "pressing a paddle", 'parent_method_id': 1},
            {'id': 4,
             'category_level': 2, 'denomination': "pushing something", 'parent_method_id': 1},
            {'id': 5,
             'category_level': 1, 'denomination': "electrophysiological"},
            {'id': 6,
             'category_level': 2, 'denomination': "auditory evoked potentials (AEP)", 'parent_method_id': 5},
            {'id': 7,
             'category_level': 2, 'denomination': "auditory brain stem responses (ABR)", 'parent_method_id': 5},
            {'id': 8,
             'category_level': 1, 'denomination': "cosine-gated tone bursts"},
            {'id': 9,
             'category_level': 1, 'denomination': "sinusoidal amplitude modulated tone (SAM)"},
            {'id': 10,
             'category_level': 2, 'denomination': "modulated narrow band noise", 'parent_method_id': 9},
            {'id': 11,
             'category_level': 2, 'denomination': "modulated rectangular click", 'parent_method_id': 9},
            {'id': 12,
             'category_level': 2, 'denomination': "pure tone", 'parent_method_id': 9},
            {'id': 13,
             'category_level': 1, 'denomination': "sinusoidal frequency modulated tone (FM)"},
            {'id': 14,
             'category_level': 2, 'denomination': "linear upward frequency modulated sweep",
             'parent_method_id': 13},
            {'id': 15,
             'category_level': 2, 'denomination': "linear downward frequency modulated sweep", 'parent_method_id': 13},
            {'id': 16,
             'category_level': 2, 'denomination': "sinusoidal frequency modulation", 'parent_method_id': 13},
            {'id': 17,
             'category_level': 2, 'denomination': "avoidance behavior", 'parent_method_id': 1},
            {'id': 18,
             'category_level': 2, 'denomination': "cortical evoked response", 'parent_method_id': 5},
            {'id': 19,
             'category_level': 2, 'denomination': "go - no go & vocalization", 'parent_method_id': 1},
            {'id': 20,
             'category_level': 2, 'denomination': "envelope-following responses (EFR)", 'parent_method_id': 5},
            {'id': 21,
             'category_level': 2, 'denomination': "go - no go & touching a target", 'parent_method_id': 1},
            {'id': 22,
             'category_level': 1, 'denomination': "linear frequency-modulated (FM)"},
        ]

        # Parse this from the file audiogram_data/audiogrambase_impport_spl.csv
        self.sound_pressure_level_reference = [
            {'id': 1, 'spl_reference_value': 1, 'spl_reference_unit': "μPa",
                'spl_reference_significance': "current SPL reference in water"},
            {'id': 2, 'spl_reference_value': 1, 'spl_reference_unit': "μbar",
             'spl_reference_significance': "deprecated SPL reference in water",
             'conversion_factor_airborne_sound_in_decibel': 'NA',
             'conversion_factor_waterborne_sound_in_decibel': 20},
            {'id': 3, 'spl_reference_value': 1, 'spl_reference_unit': "1mPa",
             'spl_reference_significance': "deprecated SPL reference in water",
             'conversion_factor_airborne_sound_in_decibel': 34,
             'conversion_factor_waterborne_sound_in_decibel': 60},
            {'id': 4, 'spl_reference_value': 20, 'spl_reference_unit': "μPa",
             'spl_reference_significance': "current SPL reference in air",
             'conversion_factor_airborne_sound_in_decibel': 'NA',
             'conversion_factor_waterborne_sound_in_decibel': 26},
            {'id': 5, 'spl_reference_value': 0.0002, 'spl_reference_unit': "dyne cm-2",
             'spl_reference_significance': "deprecated SPL reference in air",
             'conversion_factor_airborne_sound_in_decibel': 74,
             'conversion_factor_waterborne_sound_in_decibel': 'NA'},
            {'id': 6, 'spl_reference_value': 1, 'spl_reference_unit': "dyne cm-2",
             'spl_reference_significance': "deprecated SPL reference in air",
             'conversion_factor_airborne_sound_in_decibel': 74,
             'conversion_factor_waterborne_sound_in_decibel': 100},
            {'id': 7, 'spl_reference_value': 2e-4, 'spl_reference_unit': "μbar", 'spl_reference_significance': "",
             'conversion_factor_airborne_sound_in_decibel': 'NA',
             'conversion_factor_waterborne_sound_in_decibel': 'NA'},
        ]

        # concatenate label from parts
        for i, entry in enumerate(self.sound_pressure_level_reference):
            self.sound_pressure_level_reference[i]['spl_reference_display_label'] = ' '.join(
                ['re', str(entry['spl_reference_value']), entry['spl_reference_unit']])

    """
    ===================================================
    Private variables
    ===================================================
    """

    __facilities = None
    __methods = None
    __audiogram_experiments = None
    __sound_pressure_level_reference = None
    __audiogram_data_point = None
    __taxon = []
    __individual_animal = None
    __test_animal = None
    __publication = None
    __audiogram_publication = None

    """
    ===================================================
    Model properties
    ===================================================
    """

    @property
    def facilities(self):
        """List of dicts"""
        return self.__facilities

    @facilities.setter
    def facilities(self, val):
        """val: list of dicts"""
        self.__facilities = val

    @property
    def methods(self):
        """List of dicts"""
        return self.__methods

    @methods.setter
    def methods(self, val):
        """val: list of dicts"""
        self.__methods = val

    @property
    def audiogram_experiments(self):
        """List of dicts"""
        return self.__audiogram_experiments

    @audiogram_experiments.setter
    def audiogram_experiments(self, val):
        """val: list of dicts"""
        self.__audiogram_experiments = val

    @property
    def sound_pressure_level_reference(self):
        """List of dicts"""
        return self.__sound_pressure_level_reference

    @sound_pressure_level_reference.setter
    def sound_pressure_level_reference(self, val):
        """val: list of dicts"""
        self.__sound_pressure_level_reference = val

    @property
    def audiogram_data_point(self):
        """List of dicts"""
        return self.__audiogram_data_point

    @audiogram_data_point.setter
    def audiogram_data_point(self, val):
        """val: list of dicts"""
        self.__audiogram_data_point = val

    @property
    def taxon(self):
        """List of dicts"""
        return self.__taxon

    @taxon.setter
    def taxon(self, val):
        """val: list of dicts"""
        self.__taxon = val

    @property
    def individual_animal(self):
        """List of dicts"""
        return self.__individual_animal

    @individual_animal.setter
    def individual_animal(self, val):
        """val: list of dicts"""
        self.__individual_animal = val

    @property
    def test_animal(self):
        """List of dicts"""
        return self.__test_animal

    @test_animal.setter
    def test_animal(self, val):
        """val: list of dicts"""
        self.__test_animal = val

    @property
    def publication(self):
        """List of dicts"""
        return self.__publication

    @publication.setter
    def publication(self, val):
        """val: list of dicts"""
        self.__publication = val

    @property
    def audiogram_publication(self):
        """List of dicts"""
        return self.__audiogram_publication

    @audiogram_publication.setter
    def audiogram_publication(self, val):
        """val: list of dicts"""
        self.__audiogram_publication = val

    """
    ===================================================
    Search methods
    ===================================================
    """

    def get_facility_by_name(self, name):
        """Returns the id of a facility."""
        resp = None
        for f in self.facilities:
            if f['name'] == name:
                resp = f['id']
                break
        return resp

    def get_method_by_name(self, name):
        """Returns the id of a method."""
        resp = None
        for f in self.methods:
            if f['denomination'] == name:
                resp = f['id']
                break
        return resp

    def get_spl_reference_by_name(self, name):
        """Returns the id of a spl reference."""
        resp = None
        for f in self.sound_pressure_level_reference:
            if f['spl_reference_display_label'] == name:
                resp = f['id']
                break
        return resp

    def get_taxon_by_name(self, binomial_name):
        """Returns the OTT id of a taxonomic species."""
        resp = None
        for s in self.taxon:
            if s['unique_name'] == binomial_name:
                resp = s
                break
        return resp

    def get_individual_animal(self, name, taxon_id):
        """Returns the id of an animal."""
        resp = None
        for f in self.individual_animal:
            if f['individual_name'] == name and f['taxon_id'] == taxon_id:
                resp = f['id']
                break
        return resp

    def get_publication_by_doi(self, doi):
        """Returns the id of a publication by its doi"""
        resp = None
        for p in self.publication:
            if p['doi'] == doi:
                resp = p['id']
                break
        return resp

    def get_publication_by_citation(self, ct):
        """Returns the id of a publication by its citation_long"""
        resp = None
        for p in self.publication:
            if p['citation_long'] == ct:
                resp = p['id']
                break
        return resp

    def get_publication_by_citation_short(self, ct):
        """Returns the id of a publication by its citation_short"""
        resp = None
        for p in self.publication:
            if p['citation_short'] == ct:
                resp = p['id']
                break
        return resp

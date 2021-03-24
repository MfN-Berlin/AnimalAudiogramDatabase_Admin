# -*- coding: utf-8 -*-
'''
Created on 28.11.2019
Convert a data dictionary into Python objects
@author: Alvaro Ortiz for Museum fuer Naturkunde Berlin
'''
import math
import csv
from data_import.Model import Model
from data_import.Tree_of_Life import Obtain_OTT_ID, Obtain_Lineage
from data_import.Wikidata import Obtain_Wikibase_Item_ID, Obtain_Vernacular_Name
from data_import.DOI import Obtain_Citation, Obtain_Citation_Short
import traceback


class Parser:
    # Name in the spreadsheet : name in the database experiment table
    col_names = {
        'Audiogram ID': 'id',
        'Latitude': 'latitude_in_decimal_degree',
        'Longitude': 'longitude_in_decimal_degree',
        'Position of the animal': 'position_of_animal',
        'Distance to sound source (in m)': 'distance_to_sound_source_in_meter',
        'Test environment': 'test_environment_description',
        'Medium': 'medium',
        'Position of the 1st electrode': 'position_first_electrode',
        'Position of the 2nd electrode': 'position_second_electrode',
        'Position of the 3rd electrode': 'position_third_electrode',
        'Year of experiment start': 'year_of_experiment_start',
        'Year of experiment end': 'year_of_experiment_end',
        'Calibration': 'calibration',
        'Threshold determination info (%)': 'threshold_determination_method',
        'Staircase procedure': 'testtone_presentation_staircase',
        'Method of constants': 'testtone_presentation_method_constants',
        'Form of the sound': 'testtone_presentation_sound_form',
        'Sedated': 'sedated',
        'Sedation details': 'sedation_details',
        'Measurements': 'number_of_measurements',
        'Number of experimental animals': 'number_of_animals'
    }
    # Name in the spreadsheet : name in the database data point table
    data_point_names = {
        'Duration of test tone (ms)': 'testtone_duration_in_millisecond',
        'Frequency (kHz)': 'testtone_frequency_in_khz',
        'SPL (with reference level according to next field)': 'sound_pressure_level_in_decibel',
        'SPL reference value': 'sound_pressure_level_reference_method',
        'Audiogram ID': 'audiogram_experiment_id',
    }
    # Name in the spreadsheet : name in the database publication table
    publication_names = {
        'Source long': 'citation_long', 'Source short': 'citation_short', 'DOI': 'doi'
    }

    def __init__(self):
        """
        Initializes an empty Model object that will be filled when calling parse(filename)
        """
        self.data_dict = []
        self.model = Model()

    def process(self, path):
        """Parses the csv file."""
        self._load(path)
        self._parse()
        return self.model

    def _load(self, path):
        """Load a csv file.

        Load a ',' separated list of entries into an array of dict. CSV column headers are dict keys.

        @param: String $path
        @return: list<dict>
        """
        with open(path) as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                self.data_dict.append(row)

    def _parse(self):
        """
        Convert a data dictionary into Python objects.
        """
        self.model.facilities = self.parse_facilities()
        self.model.audiogram_experiments = self.parse_audiogram_experiments()
        self.model.audiogram_data_point = []  # self.parse_audiogram_data_point()
        self.parse_taxa()
        self.model.individual_animal = self.parse_individual_animal()
        self.model.test_animal = self.parse_test_animal()
        self.model.publication = self.parse_publication()
        self.model.audiogram_publication = self.parse_audiogram_publication()

    def parse_facilities(self):
        resp = []
        facility_names = self.unique_values('Name of the facility')
        for i, name in enumerate(facility_names):
            if not self.isna(name):
                facility = dict()
                facility['id'] = i+1
                facility['name'] = name
                resp.append(facility)
        return resp

    def parse_taxa(self):
        """
        Parses each species binomial name, gets taxonomy from Tree of Life API.
        """
        binomial_names = self.unique_values('Binomial name')

        for i, name in enumerate(binomial_names):
            if not name:
                continue
            ott = Obtain_OTT_ID().run(name)
            lineage = Obtain_Lineage().run(ott)
            t_phylum = self._add_taxon(lineage, 'phylum')
            t_class = self._add_taxon(lineage, 'class')
            if t_class is None:
                continue
                # add Reptilia by hand
                #reptilia = Obtain_Lineage().run(5257442)
                #t_class = self._add_taxon(reptilia, 'class')

            if t_class:
                t_class['parent'] = t_phylum['ott_id']
            t_order = self._add_taxon(lineage, 'order')
            if t_order:
                if t_class:
                    t_order['parent'] = t_class['ott_id']
            t_family = self._add_taxon(lineage, 'family')
            if t_family:
                t_family['parent'] = t_order['ott_id']
            t_genus = self._add_taxon(lineage, 'genus')
            if t_genus:
                t_genus['parent'] = t_family['ott_id']
            t_species = self._add_taxon(lineage, 'species')
            if t_species:
                t_species['parent'] = t_genus['ott_id']
            t_subspecies = self._add_taxon(lineage, 'subspecies')
            if t_subspecies:
                t_subspecies['parent'] = t_species['ott_id']
                # if subspecies doesn't have a name, use the species name
                if 'vernacular_name_english' not in t_subspecies:
                    t_subspecies['vernacular_name_english'] = t_species['vernacular_name_english']
                if 'vernacular_name_german' not in t_subspecies:
                    t_subspecies['vernacular_name_german'] = t_species['vernacular_name_german']
        self._make_nested_set()

    def _add_taxon(self, lineage, rank):
        """Appends a taxon to the model's taxonomy."""
        if lineage[rank] is None:
            return None
        taxon_name = lineage[rank]['name']
        taxon = self.model.get_taxon_by_name(taxon_name)
        if not taxon:
            try:
                taxon = dict()
                taxon['unique_name'] = taxon_name
                taxon['rank'] = rank
                taxon['ott_id'] = lineage[rank]['ott_id']
                if rank == "species":
                    vernacular = Obtain_Vernacular_Name().run(taxon_name)
                    taxon['vernacular_name_english'] = vernacular['en']
                    taxon['vernacular_name_german'] = vernacular['de']
                self.model.taxon.append(taxon)
            except:
                print("Could not add taxon for lineage: ", lineage)
                traceback.format_exc()
        return taxon

    def _make_nested_set(self):
        """Adds left and right indexes to make an nested set out of the taxonomic tree."""
        root = None
        for taxon in self.model.taxon:
            # assuming there is a single root, i.e. one rooted tree
            if taxon['rank'] == 'phylum':
                root = taxon
                break
        index = 1
        root['lft'] = index
        index = self._nested_set_recurse(index, root)
        root['rgt'] = index

    def _nested_set_recurse(self, index, parent_node):
        """Recurse the nodes of the tree, adding left and right indexes."""
        index += 1
        for taxon in self.model.taxon:
            if 'parent' in taxon and taxon['parent'] == parent_node['ott_id']:
                taxon['lft'] = index
                index = self._nested_set_recurse(index, taxon)
                taxon['rgt'] = index
                index += 1
        return index

    def parse_individual_animal(self):
        resp = []
        # agregate rows in spreadsheet by audiogram id
        audiogram_ids = self.unique_values('Audiogram ID')

        i = 0
        for aid in audiogram_ids:
            try:
                first_row = self.get_rows_by_column_value(
                    'Audiogram ID', aid)[0]
                # entries may be of several individuals, sperated by a semicolon
                temp = dict()
                if not self.isna(first_row['Name']):
                    temp['individual_name'] = first_row['Name']
                if not self.isna(first_row['Sex']):
                    temp['sex'] = first_row['Sex']
                # foreign keys
                binomial_name = first_row['Binomial name']
                taxon_id = self.model.get_taxon_by_name(binomial_name)
                temp['taxon_id'] = taxon_id['ott_id']
                individuals_found = self.split_individual_animals(temp)
                for individual in individuals_found:
                    i = i + 1
                    individual['id'] = i
                    resp.append(individual)
            except:
                traceback.format_exc()
                continue
        return resp

    def split_individual_animals(self, temp):
        """Entries may be of several individuals, separated by a semicolon."""
        resp = []
        names = ['NA']
        sexes = None
        if 'individual_name' in temp.keys():
            names = temp['individual_name'].split(';')
        if 'sex' in temp.keys():
            sexes = temp['sex'].lower().split(';')
        for i, name in enumerate(names):
            entry = dict()
            entry['individual_name'] = name.strip()
            if sexes:
                entry['sex'] = sexes[i].strip()
            entry['taxon_id'] = temp['taxon_id']
            resp.append(entry)
        return resp

    def parse_test_animal(self):
        resp = []
        # agregate rows in spreadsheet by audiogram id
        audiogram_ids = self.unique_values('Audiogram ID')

        i = 0
        for aid in audiogram_ids:
            try:
                first_row = self.get_rows_by_column_value(
                    'Audiogram ID', aid)[0]
                # entries may be of several individuals, separated by a semicolon
                temp = dict()
                if not self.isna(first_row['Name']):
                    temp['name'] = first_row['Name']
                if not self.isna(first_row['Audiogram ID']):
                    temp['audiogram_experiment_id'] = math.floor(
                        self.cast(first_row['Audiogram ID']))
                if not self.isna(first_row['Life stage']):
                    temp['life_stage'] = first_row['Life stage']
                if not self.isna(first_row['Age (months)']):
                    temp['age'] = first_row['Age (months)']
                if not self.isna(first_row['Status of liberty']):
                    temp['liberty_status'] = first_row['Status of liberty']
                # if not self.isna(first_row['Duration in captivity (months)']):
                #    temp['captivity_duration_in_month'] = first_row[
                #        'Duration in captivity (months)']
                # foreign keys
                # if not self.isna(first_row['Binomial_name']):
                #    binomial_name = first_row['Binomial name']
                #    taxon_id = self.model.get_taxon_by_name(binomial_name)[
                #        'ott_id']
                #    individuals_found = self.split_individual_test_animals(
                #        temp, taxon_id)
                #    for individual in individuals_found:
                #        i = i + 1
                #        individual['id'] = i
                #        resp.append(individual)
            except Exception as e:
                print(e)
                print(
                    "Could not parse audiogramid %s" % aid)
                traceback.format_exc()
                continue
        return resp

    def split_individual_test_animals(self, temp, taxon_id):
        """Entries may be of several individuals, separated by a semicolon."""
        resp = []
        age_min = []
        age_max = []
        captivity_duration = []
        life_stage = []
        names = ['NA']
        if 'name' in temp:
            names = temp['name'].split(';')
        if 'life_stage' in temp:
            life_stage = temp['life_stage'].split(';')
        if 'age' in temp and temp['age'] != '0':
            age_min = temp['age'].split(';')
            # print(age_min)
            #ages = temp['age'].split(';')
            # print("============================")
            # print(temp['age'])
            # age_min.append(ages)
            # for age in ages:
            #    if 'to' in age:
            #        age_range = age.split('to')
            #        age_min.append(age_range[0].strip())
            #        age_max.append(age_range[1].strip())
        if 'captivity_duration_in_month' in temp.keys():
            captivity_duration = temp['captivity_duration_in_month'].split(';')
        # loop throug animal names
        for i, name in enumerate(names):
            entry = dict()
            entry['individual_animal_id'] = self.model.get_individual_animal(
                name.strip(), taxon_id)
            entry['audiogram_experiment_id'] = temp['audiogram_experiment_id']
            if life_stage:
                entry['life_stage'] = life_stage[i].strip().lower()
            if age_min:
                entry['age_min_in_month'] = self.cast(age_min[i].strip())
            # if age_max:
            #    entry['age_max_in_month'] = self.cast(age_max[i])
            if 'liberty_status' in temp.keys():
                entry['liberty_status'] = temp['liberty_status']
            if captivity_duration:
                entry['captivity_duration_in_month'] = self.cast(
                    captivity_duration[i].strip())
            resp.append(entry)
        return resp

    def parse_audiogram_experiments(self):
        resp = []
        # agregate rows in spreadsheet by audiogram id
        audiogram_ids = self.unique_values('Audiogram ID')

        for i, aid in enumerate(audiogram_ids):
            first_row = self.get_rows_by_column_value('Audiogram ID', aid)[0]
            exp = dict()
            # map spreadsheet column names to database column names
            for key in Parser.col_names:
                val = Parser.col_names[key]
                if key in first_row:
                    if first_row[key] and not self.isna(first_row[key]):
                        exp[val] = first_row[key]
            # set year to int
            if 'year_of_experiment_start' in exp:
                exp['year_of_experiment_start'] = math.floor(
                    self.cast(exp['year_of_experiment_start']))
            if 'year_of_experiment_end' in exp:
                exp['year_of_experiment_end'] = math.floor(
                    self.cast(exp['year_of_experiment_end']))
            # set id to int
            exp['id'] = math.floor(self.cast(exp['id']))
            # add foreign keys
            facility_name = first_row['Name of the facility']
            fid = self.model.get_facility_by_name(facility_name)
            if fid:
                exp['facility_id'] = fid

            method_name = first_row['Method']
            mid = self.model.get_method_by_name(method_name)
            if mid:
                exp['measurement_method_id'] = mid

            form_method_name = first_row['Form of the tone']
            fmid = self.model.get_method_by_name(form_method_name)
            if fmid:
                exp['testtone_form_method_id'] = fmid

            resp.append(exp)

        return resp

    def parse_audiogram_data_point(self):
        """Return a list of data points (dicts), one per row."""
        resp = []
        for i, row in enumerate(self.data_dict):
            point = dict()
            # generate an id, start at 1
            point['id'] = i + 1
            # map spreadsheet column names to database column names
            for key in Parser.data_point_names:
                val = Parser.data_point_names[key]
                if row[key] and not self.isna(row[key]):
                    point[val] = self.cast(row[key])
            # add foreign keys
            spl_reference_name = row['Sound Pressure Level (SPL) reference']
            splr_id = self.model.get_spl_reference_by_name(spl_reference_name)
            if splr_id:
                point['sound_pressure_level_reference_id'] = splr_id
            resp.append(point)
        return resp

    def parse_publication(self):
        """
        Return a list of publications.

        Assuming every publication has a DOI.
        """
        resp = []
        publication_dois = self.unique_values('DOI')
        for i, doi in enumerate(publication_dois):
            if doi == "" or doi == "NA":
                continue
            publication = dict()
            publication['doi'] = doi.strip()
            try:
                # try to get publication data from DOI
                publication['citation_long'] = Obtain_Citation().run(doi)
                publication['citation_short'] = Obtain_Citation_Short().run(doi)
            except Exception:
                # if DOI is wrong, read data from table
                print("Could not import bibliographical data for doi %s" % doi)
                rows = self.get_rows_by_column_value('DOI', doi)
                publication['citation_long'] = rows[0]["Source long"]
                publication['citation_short'] = rows[0]["Source short"]
            # generate an id, start at 1
            publication['id'] = i + 1
            resp.append(publication)
        resp = self.parse_publication_without_DOI(resp)
        return resp

    def parse_publication_without_DOI(self, resp):
        start_id = len(resp)
        publication_cite = self.unique_values('Source long')
        for i, cite in enumerate(publication_cite):
            rows = self.get_rows_by_column_value('Source long', cite)
            if rows[0]['DOI'] != "" and rows[0]['DOI'] != "NA":
                continue
            cite.replace('MÃ¸hl', 'Møhl')
            rows[0]["Source short"] = rows[0]["Source short"].replace(
                'MÃ¸hl', 'Møhl')
            publication = dict()
            publication['citation_long'] = cite
            publication['citation_short'] = rows[0]["Source short"]
            publication['id'] = start_id + i + 1
            resp.append(publication)
        return resp

    def parse_audiogram_publication(self):
        """
        Relate publications to audiograms, many to many
        """
        resp = []
        publications = self.unique_values('Source long')
        for i, cite in enumerate(publications):
            rows = self.get_rows_by_column_value('Source long', cite)
            audiogram_ids = []
            for r in rows:
                if r['Audiogram ID']:
                    audiogram_ids.append(math.floor(
                        self.cast(r['Audiogram ID'])))
            unique_audiogram_ids = set(audiogram_ids)
            for unique_id in unique_audiogram_ids:
                audiogram_publication = dict()
                audiogram_publication['audiogram_experiment_id'] = unique_id
                if 'DOI' in rows[0]:
                    doi = rows[0]['DOI']
                    if doi != "" and doi != "NA":
                        audiogram_publication['publication_id'] = self.model.get_publication_by_doi(
                            doi.strip())
                    else:
                        audiogram_publication['publication_id'] = self.model.get_publication_by_citation(
                            cite.strip())
                else:
                    audiogram_publication['publication_id'] = self.model.get_publication_by_citation(
                        cite.strip())
                resp.append(audiogram_publication)
        return resp

    def cast(self, val):
        """Try to find the right type of a value"""
        try:
            float(val)
            return float(val)
        except ValueError:
            return val

    def get_rows_by_column_value(self, name, val):
        """Returns a list of rows (dicts) where column name has value val."""
        resp = []
        for row in self.data_dict:
            if row[name] == val:
                resp.append(row)
        return resp

    def get_rows_by_2column_value(self, name1, val1, name2, val2):
        """Returns a list of rows (dicts) where column name has value val."""
        resp = []
        for row in self.data_dict:
            if (row[name1] == val1 and row[name2] == val2):
                resp.append(row)
        return resp

    def unique_values(self, name):
        """Returns a set of unique values for column name in data_dict."""
        resp = []
        for row in self.data_dict:
            if not self.isna(row[name]):
                resp.append(row[name])
        resp = set(resp)
        return resp

    def isna(self, val):
        """Checks for NA values"""
        return val == "NA" or not val.strip() or val == "/"

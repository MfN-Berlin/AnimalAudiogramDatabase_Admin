'''
Created on 28.11.2019
Import audiogram data from a spreadsheet into a database
@author: Alvaro Ortiz for Museum fuer Naturkunde Berlin

    Current conversion rules:
    Z:\Projekte\Hoerfaehigkeiten_von_Pinguinen\Informationsplattform\Hörphysiologische_Datenbank\database_requirement_description_working_version.docx

    Example:
    python Converter.py --in spreadsheet.csv --out data.sql

'''
from data_import.SQLSerializer import SQLSerializer
from data_import.Parser import Parser
import logging
import subprocess


class Importer():
    def as_json(self, filepath):
        """Returns a json representation of the csv file."""
        json_data = []
        return json_data

    def convert(self, filepath):
        """Convert a csv fule to SQL statements."""
        # parse the csv file
        model = Parser().process(filepath)

        # convert data to sql statements
        serializer = SQLSerializer()
        sql_string = serializer.process(model)
        return sql_string

    def import_sql(self, sql_string):
        """Import sql dump to database"""
        with open('/tmp/dump.sql', 'w') as file:
            file.write(sql_string)
        command = "mysql -u%s -p%s -hdb audiogrambase < /tmp/dump.sql" % (
            'root', 'qq0uei')
        proc = subprocess.Popen(
            (command).split(),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            shell=False)
        out, err = proc.communicate()
        logging.warning(err)

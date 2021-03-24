'''
Created on 28.11.2019
Import audiogram data from a spreadsheet into a database
@author: Alvaro Ortiz for Museum fuer Naturkunde Berlin

    Current conversion rules: 
    Z:\Projekte\Hoerfaehigkeiten_von_Pinguinen\Informationsplattform\Hörphysiologische_Datenbank\database_requirement_description_working_version.docx

    Example:
    python Converter.py --in spreadsheet.csv --out data.sql

'''
import sys
import os
import configparser
import traceback
import argparse
from data_import.Parser import Parser
from data_import.SQLSerializer import SQLSerializer
from data_import.Timer import Timer

if __name__ == "__main__":
    """
    Parse audiogram data from a spreadsheet into a database dump.

    @arg --in path-to-csv-file as mounted from the hip_data_exchange container (e.g. /data/Audiogramme.csv)
    @arg --out path to generated SQL file (e.g. /data/dump.sql)
    """
    try:
        # Performance
        with Timer() as t:
            # Parse command-line options
            arg_parser = argparse.ArgumentParser()
            csv_path = None
            arg_parser.add_argument(
                "-i", "--in", dest="csv_path", help="Path to csv file as mounted from the hip_data_exchange container (e.g. /data/Audiogramme.csv)")
            sql_path = None
            arg_parser.add_argument(
                "-o", "--out", dest="sql_path", help="Path to output SQl file (e.g. /data/dump.sql)")
            args = arg_parser.parse_args()

            # parse the csv file
            model = Parser().process(args.csv_path)

            # convert data to sql statements
            serializer = SQLSerializer()
            sql_string = serializer.process(model)

            # save to output file
            with open(args.sql_path, 'w') as file:
                file.write(sql_string)

        print("\n= Total time =======================")
        print("Total {:06.4f} s\n".format(t.interval))

    except Exception as e:
        print(e)
        print(traceback.format_exc())
        arg_parser.print_help()
        sys.exit(1)

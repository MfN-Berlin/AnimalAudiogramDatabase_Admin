'''
Created on 02.12.2019
Convert audiogram data from a spreadsheet into SQL
@author: Alvaro Ortiz for Museum fuer Naturkunde Berlin
'''


class SQLSerializer:
    sql_str = None

    def __init__(self):
        self.sql_str = ''

    def process(self, model):
        if model.facilities:
            self.sql_str += self.insert_sql(model.facilities, "facility")
        if model.methods:
            self.sql_str += self.insert_sql(model.methods, "method")
        if model.audiogram_experiments:
            self.sql_str += self.insert_sql(
                model.audiogram_experiments, "audiogram_experiment")
        if model.audiogram_data_point:
            self.sql_str += self.insert_sql(model.audiogram_data_point,
                                            "audiogram_data_point")
        if model.taxon:
            self.sql_str += self.insert_sql(model.taxon, "taxon")
        if model.individual_animal:
            self.sql_str += self.insert_sql(model.individual_animal,
                                            "individual_animal")
        if model.test_animal:
            self.sql_str += self.insert_sql(model.test_animal, "test_animal")
        if model.publication:
            self.sql_str += self.insert_sql(model.publication, "publication")
        if model.audiogram_publication:
            self.sql_str += self.insert_sql(model.audiogram_publication,
                                            "audiogram_publication")
        if model.sound_pressure_level_reference:
            for i, entry in enumerate(model.sound_pressure_level_reference):
                del model.sound_pressure_level_reference[i]['spl_reference_display_label']
            self.sql_str += self.insert_sql(
                model.sound_pressure_level_reference, "sound_pressure_level_reference")

        return self.sql_str

    def insert_sql(self, value_set, table_name):
        """Write a set of values into a SQL statement"""
        resp = ''
        for i, entry in enumerate(value_set):
            keys = []
            vals = []
            for k, v in entry.items():
                if v == 'NA' or v == 'na':
                    vals.append('NULL')
                elif str(v).isdigit():
                    vals.append(str(v))
                else:
                    v = str(v).replace("'", "''")  # escape apostrophes in SQL
                    vals.append("'" + v + "'")
                keys.append(k)
            key_str = ','.join(keys)
            val_str = ','.join(vals)
            resp += "INSERT INTO %s (%s) VALUES (%s);\n" % (table_name,
                                                            key_str, val_str)
        return resp

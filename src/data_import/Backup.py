'''
Created on 09.04.2021
Handle database backups
@author: Alvaro Ortiz for Museum fuer Naturkunde Berlin

'''
import logging
import os


class Backup:
    def __init__(self, config):
        self.host = config.get('DEFAULT', 'DB_HOST')
        self.password = config.get('DEFAULT', 'DB_PASSWORD')
        self.username = config.get('DEFAULT', 'DB_USERNAME')
        self.database = config.get('DEFAULT', 'DB_DATABASE')
        self.backup_file = '/tmp/backup.sql'

    def create(self):
        """Dump database to file"""
        try:
            command = "mysqldump -h %s -u %s -p%s %s > %s" % (
                self.host, self.username, self.password, self.database, self.backup_file)
            os.system(command)
            return self.outfile

        except Exception as e:
            logging.warning(e)
            return False

    def restore(self):
        # drop all tables
        self._drop_all_tables()
        # restore the data from file
        command = "mysql -h %s -u %s -p%s %s < %s" % (
            self.host, self.username, self.password, self.database, self.backup_file)
        os.system(command)

    def _drop_all_tables(self):
        """Drops all audiogram tables in the database"""
        drop_tables_sql = """
        drop table audiogram_data_point,
        audiogram_experiment,
        audiogram_publication,
        facility,
        individual_animal,
        publication,
        taxon,
        test_animal,
        sound_pressure_level_reference,
        method;"""
        try:
            command = "mysql -h %s -u %s -p%s %s -Bse \"%s\"" % (
                self.host, self.username, self.password, self.database,
                drop_tables_sql)
            os.system(command)
            return True
        except Exception as e:
            logging.warning(e)
            return False

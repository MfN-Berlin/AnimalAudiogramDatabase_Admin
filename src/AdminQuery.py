"""
Admin queries.
* Implements the template method pattern
* Connects to the MySQL database using pymysql

API requirements see:
https://code.naturkundemuseum.berlin/Alvaro.Ortiz/Pinguine/wikis/Requirements-Audiogram-Frontend

Created on 28.01.2021
@author: Alvaro.Ortiz for Museum fuer Naturkunde Berlin
"""
import abc
import pymysql
import logging


class AdminQuery(abc.ABC):
    """Base class for database queries called from the Admin service."""

    connection = None
    """Database connection."""

    def __init__(self, config):
        self.host = config.get('DEFAULT', 'DB_HOST')
        self.password = config.get('DEFAULT', 'DB_PASSWORD')
        self.username = config.get('DEFAULT', 'DB_USERNAME')
        self.database = config.get('DEFAULT', 'DB_DATABASE')

    def run(self, param=None):
        """Runs the query implemented in the derived classes."""
        self.connection = self._get_connection()
        results = self._run(param)
        return AdminQuery.jsonize(results)

    @abc.abstractmethod
    def _run(self, param=None):
        pass

    def _get_connection(self):
        """Open a database connection."""
        return pymysql.connect(
            self.host, self.username, self.password, self.database)

    @classmethod
    def jsonize(cls, results):
        """Convert result object to json."""
        json_data = []
        for result in results['results']:
            # combine headers and data (zip is not the compression utility)
            json_data.append(dict(zip(results['headers'], result)))
        return json_data

    @classmethod
    def check_params(cls, param):
        """Check param dictionary for NaN's or undefined's or empty strings, replace by None's"""
        return {key: (val if val not in [
            'NaN', 'undefined', ''] else None) for key, val in param.items()}


class CheckQuery(AdminQuery):
    """Checks whether audiogram exists."""

    def _run(self, param=None):
        with self.connection as cursor:
            cursor.execute(
                """
                select * from audiogram_experiment where id=%(id)s;
                """,
                {'id': param})
            row_headers = [x[0] for x in cursor.description]
            all_results = cursor.fetchall()
        return {'headers': row_headers, 'results': all_results}


class DataPointsQuery(AdminQuery):
    """Get data points for experiment id."""

    def _run(self, param=None):
        with self.connection as cursor:
            cursor.execute(
                """
                select *
                from
                   audiogram_data_point
                where
                   audiogram_experiment_id=%(audiogram_experiment_id)s
                order by
                   testtone_frequency_in_khz desc
                """,  # noqa: E501
                {'audiogram_experiment_id': param})
            row_headers = [x[0] for x in cursor.description]
            all_results = cursor.fetchall()
        return {'headers': row_headers, 'results': all_results}


class CreateDataPointQuery(AdminQuery):
    """Creates a new data point."""

    def _run(self, param=None):
        param = AdminQuery.check_params(param)
        with self.connection as cursor:
            cursor.execute(
                """
                insert into audiogram_data_point(
                    testtone_duration_in_millisecond,
                    testtone_frequency_in_khz,
                    sound_pressure_level_in_decibel,
                    sound_pressure_level_reference_id,
                    sound_pressure_level_reference_method,
                    audiogram_experiment_id
                )
                values (
                    %(testtone_duration_in_millisecond)s,
                    %(testtone_frequency_in_khz)s,
                    %(sound_pressure_level_in_decibel)s,
                    %(sound_pressure_level_reference)s,
                    %(sound_pressure_level_reference_method)s,
                    %(audiogram_experiment_id)s
                )
                """,
                {
                    'testtone_duration_in_millisecond': param['testtone_duration_in_millisecond'],
                    'testtone_frequency_in_khz': param['testtone_frequency_in_khz'],
                    'sound_pressure_level_in_decibel': param['sound_pressure_level_in_decibel'],
                    'sound_pressure_level_reference': param['sound_pressure_level_reference'],
                    'sound_pressure_level_reference_method': param['sound_pressure_level_reference_method'],
                    'audiogram_experiment_id': param['audiogram_experiment_id']
                }
            )
        return {'headers': ['response'], 'results': []}


class SaveAnimalQuery(AdminQuery):
    """Edits the details of an existing animal."""

    def _run(self, param=None):
        param = AdminQuery.check_params(param)

        # taxon
        with self.connection as cursor:
            cursor.execute(
                """
                update
                   individual_animal,test_animal
                set
                   taxon_id=%(ott_id)s,
                   sex=%(sex)s,
                   liberty_status=%(liberty)s,
                   captivity_duration_in_month=%(captivity)s,
                   age_min_in_month=%(age)s,
                   individual_name=%(individual_name)s
                where
                   test_animal.audiogram_experiment_id=%(expId)s
                and
                   individual_animal.id=test_animal.individual_animal_id
                """,
                {
                    'expId': param['expId'],
                    'age': param['age'],
                    'captivity': param['captivity'],
                    'ott_id': param['ott_id'],
                    'sex': param['sex'],
                    'liberty': param['liberty'],
                    'lifestage': param['lifestage'],
                    'individual_name': param['individual_name']
                }
            )

        return {'headers': ['response'], 'results': []}


class SaveDataPointQuery(AdminQuery):
    """Edits the values of an existing data point."""

    def _run(self, param=None):
        param = AdminQuery.check_params(param)
        cols = []
        if param['testtone_duration_in_millisecond']:
            cols.append(
                'testtone_duration_in_millisecond = %(testtone_duration_in_millisecond)s')
        else:
            cols.append(
                'testtone_duration_in_millisecond = NULL')

        if param['testtone_frequency_in_khz']:
            cols.append(
                'testtone_frequency_in_khz = %(testtone_frequency_in_khz)s')
        else:
            cols.append(
                'testtone_frequency_in_khz = NULL')

        if param['sound_pressure_level_in_decibel']:
            cols.append(
                'sound_pressure_level_in_decibel = %(sound_pressure_level_in_decibel)s')
        else:
            cols.append(
                'sound_pressure_level_in_decibel = NULL')

        if param['sound_pressure_level_reference']:
            cols.append(
                'sound_pressure_level_reference_id = %(sound_pressure_level_reference)s')
        else:
            cols.append(
                'sound_pressure_level_reference_id = NULL')

        if param['sound_pressure_level_reference_method']:
            cols.append(
                'sound_pressure_level_reference_method = %(sound_pressure_level_reference_method)s')
        else:
            cols.append(
                'sound_pressure_level_reference_method = NULL')

        cols_string = ','.join(cols)
        query = 'update audiogram_data_point set {} where id = %(id)s'.format(
            cols_string)
        with self.connection as cursor:
            cursor.execute(
                query,
                {
                    'id': param['id'],
                    'testtone_duration_in_millisecond': param['testtone_duration_in_millisecond'],
                    'testtone_frequency_in_khz': param['testtone_frequency_in_khz'],
                    'sound_pressure_level_in_decibel': param['sound_pressure_level_in_decibel'],
                    'sound_pressure_level_reference': param['sound_pressure_level_reference'],
                    'sound_pressure_level_reference_method': param['sound_pressure_level_reference_method']
                }
            )
        return {'headers': ['response'], 'results': []}


class DeleteDataPointQuery(AdminQuery):
    """Deletes a data point."""

    def _run(self, param=None):
        with self.connection as cursor:
            cursor.execute(
                """
                delete from audiogram_data_point where id=%(id)s;
                """,  # noqa: E501
                {'id': param})
        return {'headers': ['response'], 'results': []}


class ListSPLReference(AdminQuery):
    """Lists all entries in sound_pressure_level_reference table."""

    def _run(self, param=None):
        with self.connection as cursor:
            cursor.execute(
                """
                select * from sound_pressure_level_reference
                """,  # noqa: E501
            )
            row_headers = [x[0] for x in cursor.description]
            all_results = cursor.fetchall()
        return {'headers': row_headers, 'results': all_results}


class ExperimentQuery(AdminQuery):
    """Get experiment metadata for experiment id."""

    def _run(self, param=None):
        with self.connection as cursor:
            cursor.execute(
                """
            select
                latitude_in_decimal_degree,
                longitude_in_decimal_degree,
                position_of_animal,
                distance_to_sound_source_in_meter,
                test_environment_description,
                medium,
                position_first_electrode,
                position_second_electrode,
                position_third_electrode,
                year_of_experiment_start,
                year_of_experiment_end,
                background_noise_in_decibel,
                calibration,
                threshold_determination_method,
                testtone_presentation_staircase,
                testtone_presentation_method_constants,
                testtone_presentation_sound_form,
                sedated,
                sedation_details,
                number_of_measurements,
                facility_id,
                measurement_method_id,
                testtone_form_method_id,
                measurement_type
            from
                audiogram_experiment
            where
                id=%(id)s
            """,
                {'id': param})
            row_headers = [x[0] for x in cursor.description]
            all_results = cursor.fetchall()
        return {'headers': row_headers, 'results': all_results}


class InsertExperimentQuery(AdminQuery):
    """Adds a new experiment."""

    def _run(self, param=None):
        param = AdminQuery.check_params(param)
        with self.connection as cursor:
            cursor.execute(
                """
                insert into
                   audiogram_publication(audiogram_experiment_id, publication_id)
                   values(%(id)s, 0)
                """,
                {
                    'id': param['id']
                }
            )
        with self.connection as cursor:
            cursor.execute(
                """
                insert into
                   audiogram_experiment(
                   latitude_in_decimal_degree,
                   longitude_in_decimal_degree,
                   position_of_animal,
                   distance_to_sound_source_in_meter,
                   test_environment_description,
                   medium,
                   position_first_electrode,
                   position_second_electrode,
                   position_third_electrode,
                   year_of_experiment_start,
                   year_of_experiment_end,
                   background_noise_in_decibel,
                   calibration,
                   threshold_determination_method,
                   testtone_presentation_staircase,
                   testtone_presentation_method_constants,
                   testtone_presentation_sound_form,
                   sedated,
                   sedation_details,
                   number_of_measurements,
                   facility_id,
                   measurement_method_id,
                   testtone_form_method_id,
                   measurement_type
                   )
                values (
                   %(latitude_in_decimal_degree)s,
                   %(longitude_in_decimal_degree)s,
                   %(position_of_animal)s,
                   %(distance_to_sound_source_in_meter)s,
                   %(test_environment_description)s,
                   %(medium)s,
                   %(position_first_electrode)s,
                   %(position_second_electrode)s,
                   %(position_third_electrode)s,
                   %(year_of_experiment_start)s,
                   %(year_of_experiment_end)s,
                   %(background_noise_in_decibel)s,
                   %(calibration)s,
                   %(threshold_determination_method)s,
                   %(testtone_presentation_staircase)s,
                   %(testtone_presentation_method_constants)s,
                   %(testtone_presentation_sound_form)s,
                   %(sedated)s,
                   %(sedation_details)s,
                   %(number_of_measurements)s,
                   %(facility_id)s,
                   %(measurement_method_id)s,
                   %(testtone_form_method_id)s,
                   %(measurement_type)s
                )
                """,
                {
                    'latitude_in_decimal_degree': param['latitude_in_decimal_degree'],
                    'longitude_in_decimal_degree': param['longitude_in_decimal_degree'],
                    'position_of_animal': param['position_of_animal'],
                    'distance_to_sound_source_in_meter': param['distance_to_sound_source_in_meter'],
                    'test_environment_description': param['test_environment_description'],
                    'medium': param['medium'],
                    'position_first_electrode': param['position_first_electrode'],
                    'position_second_electrode': param['position_second_electrode'],
                    'position_third_electrode': param['position_third_electrode'],
                    'year_of_experiment_start': param['year_of_experiment_start'],
                    'year_of_experiment_end': param['year_of_experiment_end'],
                    'background_noise_in_decibel': param['background_noise_in_decibel'],
                    'calibration': param['calibration'],
                    'threshold_determination_method': param['threshold_determination_method'],
                    'testtone_presentation_staircase': param['testtone_presentation_staircase'],
                    'testtone_presentation_method_constants': param['testtone_presentation_method_constants'],
                    'testtone_presentation_sound_form': param['testtone_presentation_sound_form'],
                    'sedated': param['sedated'],
                    'sedation_details': param['sedation_details'],
                    'number_of_measurements': param['number_of_measurements'],
                    'facility_id': param['facility_id'],
                    'measurement_method_id': param['measurement_method_id'],
                    'testtone_form_method_id': param['testtone_form_method_id'],
                    'measurement_type': param['measurement_type'],
                }
            )
        with self.connection as cursor:
            cursor.execute(
                """select max(id) from audiogram_experiment"""
            )
            row_headers = [x[0] for x in cursor.description]
            all_results = cursor.fetchall()
        return {'headers': row_headers, 'results': all_results}


class SaveExperimentQuery(AdminQuery):
    """Edits the details of an existing experiment."""

    def _run(self, param=None):
        param = AdminQuery.check_params(param)
        with self.connection as cursor:
            cursor.execute(
                """
                update
                   audiogram_publication
                set
                   publication_id=%(citation_id)s
                where
                   audiogram_experiment_id=%(id)s
                """,
                {
                    'citation_id': param['citation_id'],
                    'id': param['id']
                }
            )

        with self.connection as cursor:
            cursor.execute(
                """
                update
                   audiogram_experiment
                set
                   citation_id=%(citation_id)s,
                   latitude_in_decimal_degree=%(latitude_in_decimal_degree)s,
                   longitude_in_decimal_degree=%(longitude_in_decimal_degree)s,
                   position_of_animal=%(position_of_animal)s,
                   distance_to_sound_source_in_meter=%(distance_to_sound_source_in_meter)s,
                   test_environment_description=%(test_environment_description)s,
                   medium=%(medium)s,
                   position_first_electrode=%(position_first_electrode)s,
                   position_second_electrode=%(position_second_electrode)s,
                   position_third_electrode=%(position_third_electrode)s,
                   year_of_experiment_start=%(year_of_experiment_start)s,
                   year_of_experiment_end=%(year_of_experiment_end)s,
                   background_noise_in_decibel=%(background_noise_in_decibel)s,
                   calibration=%(calibration)s,
                   threshold_determination_method=%(threshold_determination_method)s,
                   testtone_presentation_staircase=%(testtone_presentation_staircase)s,
                   testtone_presentation_method_constants=%(testtone_presentation_method_constants)s,
                   testtone_presentation_sound_form=%(testtone_presentation_sound_form)s,
                   sedated=%(sedated)s,
                   sedation_details=%(sedation_details)s,
                   number_of_measurements=%(number_of_measurements)s,
                   facility_id=%(facility_id)s,
                   measurement_method_id=%(measurement_method_id)s,
                   testtone_form_method_id=%(testtone_form_method_id)s,
                   measurement_type=%(measurement_type)s
                where
                   audiogram_experiment.id=%(id)s
                """,
                {
                    'citation_id': param['citation_id'],
                    'latitude_in_decimal_degree': param['latitude_in_decimal_degree'],
                    'longitude_in_decimal_degree': param['longitude_in_decimal_degree'],
                    'position_of_animal': param['position_of_animal'],
                    'distance_to_sound_source_in_meter': param['distance_to_sound_source_in_meter'],
                    'test_environment_description': param['test_environment_description'],
                    'medium': param['medium'],
                    'position_first_electrode': param['position_first_electrode'],
                    'position_second_electrode': param['position_second_electrode'],
                    'position_third_electrode': param['position_third_electrode'],
                    'year_of_experiment_start': param['year_of_experiment_start'],
                    'year_of_experiment_end': param['year_of_experiment_end'],
                    'background_noise_in_decibel': param['background_noise_in_decibel'],
                    'calibration': param['calibration'],
                    'threshold_determination_method': param['threshold_determination_method'],
                    'testtone_presentation_staircase': param['testtone_presentation_staircase'],
                    'testtone_presentation_method_constants': param['testtone_presentation_method_constants'],
                    'testtone_presentation_sound_form': param['testtone_presentation_sound_form'],
                    'sedated': param['sedated'],
                    'sedation_details': param['sedation_details'],
                    'number_of_measurements': param['number_of_measurements'],
                    'facility_id': param['facility_id'],
                    'measurement_method_id': param['measurement_method_id'],
                    'testtone_form_method_id': param['testtone_form_method_id'],
                    'measurement_type': param['measurement_type'],
                    'id': param['id']
                }
            )

        return {'headers': ['response'], 'results': []}


class DeleteQuery(AdminQuery):  # pylint: disable=too-few-public-methods
    """Deletes an audiogram from the database."""

    def _run(self, param=None):
        with self.connection as cursor:
            # delete experiment
            cursor.execute(
                """
                delete from audiogram_experiment where id = %(id)s;
                """,  # noqa: E501
                {'id': param})
            # delete data points
            cursor.execute(
                """
                delete from audiogram_data_point where audiogram_experiment_id = %(id)s;
                """,  # noqa: E501
                {'id': param})
            # delete linking tables
            cursor.execute(
                """
                delete from audiogram_publication where audiogram_experiment_id = %(id)s;
                """,  # noqa: E501
                {'id': param})
            cursor.execute(
                """
                delete from test_animal where audiogram_experiment_id = %(id)s;
                """,  # noqa: E501
                {'id': param})
            # cleanup publication table
            cursor.execute(
                """
                delete from publication
                where publication.id in (
                   select publication.id
                   from
                      audiogram_publication right join publication
                   on
                      publication.id=audiogram_publication.publication_id
                   where
                      audiogram_publication.publication_id is null
                   )
                """
            )
            # cleanup facility table
            cursor.execute(
                """
                delete from facility
                where facility.id in (
                   select facility.id
                   from
                      audiogram_experiment right join facility
                   on
                      facility.id=audiogram_experiment.facility_id
                   where
                      audiogram_experiment.id is null
                   )
                """
            )
            # cleanup individual_animal table
            cursor.execute(
                """
                delete from
                   individual_animal
                where id in (
                select
                   individual_animal.id
                from
                   taxon,
                   test_animal
                right join
                   individual_animal
                on
                   test_animal.individual_animal_id=individual_animal.id
                where
                   taxon.rank='species'
                and individual_animal.taxon_id=taxon.ott_id
                and test_animal.audiogram_experiment_id is null
                )
                """
            )

        return {'headers': ['response'], 'results': []}


class AnimalQuery(AdminQuery):
    """Get details of animal(s) involved in this experiment."""

    def _run(self, param=None):
        with self.connection as cursor:
            cursor.execute(
                """
            select
                individual_name,
                vernacular_name_english,
                unique_name as species_name,
                sex,
                life_stage,
                floor(age_min_in_month) as age_in_month,
                liberty_status,
                captivity_duration_in_month,
                biological_season,
                ott_id
            from
                test_animal as t,
                individual_animal as i,
                taxon
            where
                audiogram_experiment_id=%(expId)s
                and i.id=t.individual_animal_id
                and taxon.ott_id=i.taxon_id;
                """,
                {'expId': param})
            row_headers = [x[0] for x in cursor.description]
            all_results = cursor.fetchall()
        return {'headers': row_headers, 'results': all_results}


class AllTaxaVernacularQuery(AdminQuery):
    """Get taxon taxon id, English name and animal count for all taxa in the database.

    for the time being: return only species and subspecies
    """

    def _run(self, param=None):
        with self.connection as cursor:
            cursor.execute(
                """
                select
                   taxon.vernacular_name_english as vernacular_name_english,
                   taxon.ott_id,
                   count(individual_animal.id) as total
                from
                   taxon
                left join
                   individual_animal on taxon.ott_id = individual_animal.taxon_id
                where
                   taxon.rank in ('species', 'subspecies')
                group by
                   taxon.ott_id
                order by
                   vernacular_name_english
                """
            )
            row_headers = [x[0] for x in cursor.description]
            all_results = cursor.fetchall()
        return {'headers': row_headers, 'results': all_results}


class AllFacilitiesQuery(AdminQuery):
    """Get all facilities in the database."""

    def _run(self, param=None):
        with self.connection as cursor:
            cursor.execute(
                """
                select
                   id,
                   name
                from
                   facility
                order by
                   name;
                """
            )
            row_headers = [x[0] for x in cursor.description]
            all_results = cursor.fetchall()
        return {'headers': row_headers, 'results': all_results}


class AllMeasurementMethodsQuery(AdminQuery):
    """Get method id and full method name for all measurement methods in the database."""

    def _run(self, param=None):
        with self.connection as cursor:
            cursor.execute(
                """
                select
                   method.id as method_id,
                   concat(m2.denomination, ": ", m1.denomination) as method_name
                from
                   audiogram_experiment exp
                   left join method m1 on m1.id=exp.measurement_method_id
                   left join method m2 on m2.id=m1.parent_method_id,
                   method
                where
                   exp.measurement_method_id=method.id
                   and m2.denomination is not NULL
                group by
                   method_id
                order by
                   method_name
                """
            )
            row_headers = [x[0] for x in cursor.description]
            all_results = cursor.fetchall()
        return {'headers': row_headers, 'results': all_results}


class AllToneMethodsQuery(AdminQuery):
    """Get method id and full method name for all measurement methods in the database."""

    def _run(self, param=None):
        with self.connection as cursor:
            cursor.execute(
                """
                select
                   method.id as method_id,
                   method.denomination as method_name
                from
                   audiogram_experiment exp
                   left join method m1 on m1.id=exp.testtone_form_method_id,
                   method
                where
                   exp.testtone_form_method_id=method.id
                group by
                   method_id
                order by
                   method_name
                """
            )
            row_headers = [x[0] for x in cursor.description]
            all_results = cursor.fetchall()
        return {'headers': row_headers, 'results': all_results}


class All_publications_query(AdminQuery):
    """Get publication id and short citation for all publications in the database."""

    def _run(self, param=None):
        with self.connection as cursor:
            cursor.execute(
                """
                select
                   id,
                   citation_short
                from
                   publication
                order by
                   citation_short;
                """
            )
            row_headers = [x[0] for x in cursor.description]
            all_results = cursor.fetchall()
        return {'headers': row_headers, 'results': all_results}


class Read_publication_query(AdminQuery):
    """Get publication id and short citation for all publications in the database."""

    def _run(self, param=None):
        with self.connection as cursor:
            cursor.execute(
                """
                select
                   id,
                   citation_short,
                   citation_long,
                   doi
                from
                   publication
                where
                   id=%(id)s
                """,
                {
                    'id': param
                }
            )
            row_headers = [x[0] for x in cursor.description]
            all_results = cursor.fetchall()
        return {'headers': row_headers, 'results': all_results}


class Add_publication_query(AdminQuery):
    """Adds a publication to the database."""

    def _run(self, param=None):
        param = AdminQuery.check_params(param)
        try:
            with self.connection as cursor:
                cursor.execute(
                    """
                insert into publication(
                   doi,
                   citation_long,
                   citation_short
                )
                values (
                    %(doi)s,
                    %(citation_long)s,
                    %(citation_short)s
                )
                """,
                    {
                        'doi': param['doi'],
                        'citation_long': param['citation_long'],
                        'citation_short': param['citation_short']
                    }
                )
            # When added, return id of added publication
            with self.connection as cursor:
                cursor.execute(
                    """select max(id) from publication"""
                )
                row_headers = [x[0] for x in cursor.description]
                all_results = cursor.fetchall()
            return {'headers': row_headers, 'results': all_results}
        except Exception as e:
            logging.warning(e)
            # When error, return false
            return {'headers': ['response'], 'results': [[False]]}

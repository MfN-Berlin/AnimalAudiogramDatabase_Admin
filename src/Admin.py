# -*- coding: utf-8 -*-
"""
Audiogrambase http API.

Created on 28.01.2019
@author: Alvaro Ortiz Troncoso, Museum fuer Naturkunde Berlin
"""
from flask import Flask, request, render_template, url_for, jsonify, Response, flash, redirect
from flask_cors import CORS
from functools import wraps
import configparser
import simplejson
import logging
import os
from werkzeug.utils import secure_filename
from AdminQuery import *
from Importer import Importer
from DOI import Obtain_Citation, Obtain_Citation_Short

configPath = "/src/.env"
"""Path to configuration file."""
admin_config = None
"""ConfigParser object will hold the custom API configuration """

fapp = Flask(__name__)
CORS(fapp)
fapp.config["DEBUG"] = True
fapp.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
fapp.config['JSON_AS_ASCII'] = False
fapp.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

##################
# Authentication #
##################


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == admin_config.get('DEFAULT', 'BACKEND_USERNAME') and password == admin_config.get('DEFAULT', 'BACKEND_PASSWORD')


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

##################
# API Start page #
##################


@fapp.route("/admin/v1/start", methods=['GET'])
@requires_auth
def start():
    """Shows the admin API start page"""
    return render_template('start.html')

########################
# Create new audiogram #
########################


@fapp.route("/admin/v1/upload_audiogram", methods=['GET', 'POST'])
@requires_auth
def upload_audiogram():
    """
    Uploads a new audiogram from the UI.

    Example
    ---------
    https://animalaudiograms.museumfuernaturkunde.berlin/admin/v1/create_audiogram
    """
    UPLOAD_FOLDER = '/tmp'

    fapp.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(fapp.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            flash('File uploaded')
            importer = Importer()
            resp = importer.as_json(filepath)
            #sql_string = importer.convert(filepath)
            # importer.import_sql(sql_string)
            return jsonify(resp)
    return render_template('upload_audiogram.html')


def allowed_file(filename):
    """Checks the extension of the file."""
    ALLOWED_EXTENSIONS = {'csv'}

    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


###################
# Animal metadata #
###################


@fapp.route("/admin/v1/edit_animal_metadata", methods=['GET'])
@requires_auth
def edit_animal_metadata():
    """
    Edits an animal's metadata.

    Parameters
    ----------
    expId : int, required
       expId of an audiogram

    Returns
    ----------
    animal details JSON | 'False' string

    Example
    ---------
    https://animalaudiograms.museumfuernaturkunde.berlin/admin/v1/edit_animal_metadata?expId=24
    edits the metadata of the animal that participated in audiogram 24
    """
    if 'expId' not in request.args:
        return render_template('edit_animal_metadata.html')
    expId = int(request.args['expId'])
    check = CheckQuery(admin_config).run(expId)
    if len(check) != 1:
        return 'False'
    return jsonify(AnimalQuery(admin_config).run(expId))


@fapp.route("/admin/v1/save_animal", methods=['GET'])
@requires_auth
def save_animal():
    """
    Saves an animal's details.

    Parameters
    ----------
    expId int ID of an audiogram
    age float
    captivity float
    ott_id int taxon id
    sex string male|female
    liberty string captive|wild|stranded
    lifestage string adult|sub-adult|juvenile
    individual_name string name of the individual animal

    Returns
    ----------
    'True'|'False' string

    Example
    ---------
    /admin/v1/save_animal?expId={this.expId}
        &age=${this.age}
        &captivity=${this.captivity}
        &ott_id=${this.ott_id}
        &sex=${this.sex}
        &liberty=${this.liberty}
        &lifestage=${this.lifestage}
        &individual_name=${individual_name}
    """
    if 'expId' not in request.args:
        return False
    SaveAnimalQuery(admin_config).run(request.args)
    return 'True'

###################
# Data points     #
###################


@fapp.route("/admin/v1/create_data_point", methods=['GET'])
@requires_auth
def create_data_point():
    """
    Creates a new data point.

    Parameters
    ----------
    testtone_frequency_in_khz: float
    sound_pressure_level_in_decibel: float
    testtone_duration_in_millisecond: float
    sound_pressure_level_reference:
        int, references a method in the table sound_pressure_level_reference
    sound_pressure_level_reference_method:
        null or 'root mean squared (RMS)'|'peak to peak (PP)'

    Returns
    ----------
    'True'|'False' string

    Example
    ---------
    https://animalaudiograms.museumfuernaturkunde.berlin/admin/v1/create_data_point?
            testtone_frequency_in_khz=${this.testtone_frequency_in_khz}
            &sound_pressure_level_in_decibel=${this.sound_pressure_level_in_decibel}
            &testtone_duration_in_millisecond=${this.testtone_duration_in_millisecond}
            &sound_pressure_level_reference=${this.sound_pressure_level_reference}
            &sound_pressure_level_reference_method=${this.sound_pressure_level_reference_method}
    """
    CreateDataPointQuery(admin_config).run(request.args)
    return 'True'


@fapp.route("/admin/v1/save_data_point", methods=['GET'])
@requires_auth
def save_data_point():
    """
    Saves a single data point.

    Parameters
    ----------
    id : int, required
       id of a data point

    testtone_frequency_in_khz: float
    sound_pressure_level_in_decibel: float
    testtone_duration_in_millisecond: float
    sound_pressure_level_reference:
        int, references a method in the table sound_pressure_level_reference
    sound_pressure_level_reference_method:
        null or 'root mean squared (RMS)'|'peak to peak (PP)'

    Returns
    ----------
    'True'|'False' string

    Example
    ---------
    https://animalaudiograms.museumfuernaturkunde.berlin/admin/v1/save_data_point?id=${this.id}
            &testtone_frequency_in_khz=${this.testtone_frequency_in_khz}
            &sound_pressure_level_in_decibel=${this.sound_pressure_level_in_decibel}
            &testtone_duration_in_millisecond=${this.testtone_duration_in_millisecond}
            &sound_pressure_level_reference=${this.sound_pressure_level_reference}
            &sound_pressure_level_reference_method=${this.sound_pressure_level_reference_method}
    """
    if 'id' not in request.args:
        return False
    SaveDataPointQuery(admin_config).run(request.args)
    return 'True'


@fapp.route("/admin/v1/delete_data_point", methods=['GET'])
@requires_auth
def delete_data_point():
    """
    Deletes a single data point.

    Parameters
    ----------
    id : int, required
       id of a data point

    Returns
    ----------
    'True'|'False' string

    Example
    ---------
    https://animalaudiograms.museumfuernaturkunde.berlin/admin/v1/save_data_point?id=${this.id}
    """
    if 'id' not in request.args:
        return False
    id = int(request.args['id'])
    DeleteDataPointQuery(admin_config).run(id)
    return 'True'


@fapp.route("/admin/v1/edit_data_points", methods=['GET'])
@requires_auth
def edit_data_points():
    """
    Edits an audiogram's data points.

    Parameters
    ----------
    id : int, required
       id of an audiogram

    Returns
    ----------
    'True'|'False' string

    Example
    ---------
    https://animalaudiograms.museumfuernaturkunde.berlin/admin/v1/edit_data?id=24
    edits the data points of audiogram 24
    """
    if 'id' not in request.args:
        return render_template('edit_data_points.html')
    id = int(request.args['id'])
    check = CheckQuery(admin_config).run(id)
    if len(check) != 1:
        return 'False'
    return jsonify(DataPointsQuery(admin_config).run(id))


##########################
# Audiogram / Experiment #
##########################


@fapp.route("/admin/v1/edit_experiment_metadata", methods=['GET'])
@requires_auth
def edit_experiment_metadata():
    """
    Edits an experiment's metadata.

    Parameters
    ----------
    id : int, required
       id of an audiogram

    Returns
    ----------
    experiment details JSON | 'False' string

    Example
    ---------
    https://animalaudiograms.museumfuernaturkunde.berlin/admin/v1/edit_experiment_metadata?id=24
    edits the metadata of audiogram/experiment with id 24
    """
    if 'id' not in request.args:
        return render_template('edit_experiment_metadata.html')
    id = int(request.args['id'])
    check = CheckQuery(admin_config).run(id)
    if len(check) != 1:
        return 'False'
    return jsonify(ExperimentQuery(admin_config).run(id))


@fapp.route("/admin/v1/save_experiment", methods=['GET'])
@requires_auth
def save_experiment():
    """
    Saves an experiment's details.

    Parameters
    ----------
       id: int, required id of an audiogram or 0 for new audiogram
       citation_id: int
       background_noise_in_decibel: float
       calibration: string
       distance_to_sound_source_in_meter: float
       facility_id: int, id of a faciity in the facility table
       latitude_in_decimal_degree: foat
       longitude_in_decimal_degree: float
       measurement_method_id: int
       measurement_type: string
       medium: string
       number_of_measurements: int
       position_first_electrode: string
       position_second_electrode: string
       position_third_electrode: string
       position_of_animal: string
       sedated: 'yes'|'no'
       sedation_details: string
       test_environment_description: string
       testtone_form_method_id: int, id of a method in the method table
       testtone_presentation_method_constants: 'yes'|'no'
       testtone_presentation_sound_form: string
       testtone_presentation_staircase: 'yes'|'no'
       threshold_determination_method: float
       year_of_experiment_start: int
       year_of_experiment_end: int

    Returns
    ----------
    'True'|'False' string

    Example
    ---------
    /admin/v1/save_experiment?id=197
       &citation_id=
       &background_noise_in_decibel=
       &calibration=
       &distance_to_sound_source_in_meter=
       &facility_id=
       &latitude_in_decimal_degree=
       &longitude_in_decimal_degree=
       &measurement_method_id=
       &measurement_type=
       &medium=water
       &number_of_measurements=
       &position_first_electrode=
       &position_second_electrode=
       &position_third_electrode=
       &position_of_animal=
       &sedated=
       &sedation_details=
       &test_environment_description=
       &testtone_form_method_id=
       &testtone_presentation_method_constants=
       &testtone_presentation_sound_form=
       &testtone_presentation_staircase=
       &threshold_determination_method=
       &year_of_experiment_start=
       &year_of_experiment_end=
    """
    if 'id' not in request.args:
        return False
    try:
        if int(request.args['id']) == 0:
            resp = InsertExperimentQuery(admin_config).run(request.args)
            max_id = resp[0]['max(id)']
            return(jsonify(resp))
        else:
            SaveExperimentQuery(admin_config).run(request.args)
        return 'True'
    except Exception as e:
        logging.warning(e)
        return 'False'


@fapp.route("/admin/v1/delete_experiment", methods=['GET'])
@requires_auth
def delete_experiment():
    """
    Deletes an audiogram in the database,
    along with animal, facility and publication and
    corresponding linking table entries.

    Parameters
    ----------
    id : int, required
       id of an audiogram

    Returns
    ----------
    'True'|'False' string


    Example
    ---------
    https://animalaudiograms.museumfuernaturkunde.berlin/admin/v1/delete?id=24
    deletes audiogram 24
    """
    if 'id' not in request.args:
        return render_template('delete_experiment.html')
    id = int(request.args['id'])
    check = CheckQuery(admin_config).run(id)
    if len(check) != 1:
        return 'False'
    DeleteQuery(admin_config).run(id)
    return 'True'


###################
# util            #
###################


@fapp.route("/admin/v1/list_spl_reference", methods=['GET'])
@requires_auth
def list_spl_reference():
    return jsonify(ListSPLReference(admin_config).run(None))


@fapp.route("/admin/v1/all_species_vernacular", methods=['GET'])
@requires_auth
def get_all_taxa_vernacular():
    """
    Returns all animal species in database (English names), and audiogram counts per species.

    Parameters
    ----------
    none

    Returns
    ----------
    A list in json format containing information on the species recorded in the database:
    # ott_id : int species identifier, references the Open Tree of Life database
    # vernacular_name_english : latin name of a species
    # total : int audiogram count for this species

    Example
    ---------
    http://localhost:9082/api/v1/all_species_vernacular
    Returns a list of species currently recorded in the database.
    """
    species = AllTaxaVernacularQuery(admin_config).run(id)
    return jsonify(species)


@fapp.route("/admin/v1/all_facilities", methods=['GET'])
@requires_auth
def get_all_facilities():
    """
    Returns all research facilities in database.

    Parameters
    ----------
    none

    Returns
    ----------
    A list in json format containing all facilities recorded in the database:
    # id : int internal database identifier of this facility
    # name : name of the facility

    Example
    ---------
    http://localhost:9082/api/v1/all_facilities
    Returns a list of facilities currently recorded in the database.
    """
    facilities = AllFacilitiesQuery(admin_config).run(id)
    return jsonify(facilities)


@fapp.route("/admin/v1/all_measurement_methods", methods=['GET'])
@requires_auth
def get_all_measurement_methods():
    """
    Returns all measurement methods in database.

    Parameters
    ----------
    none

    Returns
    ----------
    A list in json format containing all measurement methods recorded in the database:
    # method_id : int internal database identifier of this method
    # method_name : string name of the method. Method names are composed of:
    a generic method name ("behavioral" or "electrophysiological") and 
    a specific method name (e.g. "behavioral: go - no go")

    Example
    ---------
    http://localhost:9082/api/v1/all_methods
    Returns a list of measurement methods currently recorded in the database.
    """
    methods = AllMeasurementMethodsQuery(admin_config).run(id)
    return jsonify(methods)


@fapp.route("/admin/v1/all_tone_methods", methods=['GET'])
@requires_auth
def get_all_tone_methods():
    """
    Returns all tone methods in database.

    Parameters
    ----------
    none

    Returns
    ----------
    A list in json format cotaining all measurement methods recorded in the database:
    # method_id : int internal database identifier of this method
    # method_name : string name of the method.

    Example
    ---------
    http://localhost:9082/api/v1/all_tone_methods
    Returns a list of tone methods currently recorded in the database.
    """
    methods = AllToneMethodsQuery(admin_config).run(id)
    return jsonify(methods)


@fapp.route("/admin/v1/all_publications", methods=['GET'])
@requires_auth
def all_publications():
    """
    Return all publications in database, in short form.

    Parameters
    ----------
    none

    Returns
    ----------
    A list in json format containing all publications recorded in the database:
    # id : int internal database identifier of this publication
    # citation_short : citation in short form of the original article

    Example
    ---------
    http://localhost:9082/api/v1/all_publications
    Returns a list of publications currently recorded in the database.
    """
    publications = All_publications_query(admin_config).run(id)
    return jsonify(publications)


@fapp.route("/admin/v1/save_publication", methods=['GET'])
@requires_auth
def save_publication():
    """
    Add a publication by DOI

    Parameters
    ----------
    doi: string
    citation_long: string
    citation_short: string

    Returns
    -------
    json with either:
    * doi, citation_long, citation_short: when a doi was passed. The data is retrieved from doi.org
    * id of publication when a publication was added
    * false on error
    """
    if 'doi' not in request.args:
        return render_template('add_publication.html')
    doi = request.args['doi']
    publication = {}
    try:
        # all data is there, save in database
        if (doi
                and request.args['citation_long'] != 'undefined'
                and request.args['citation_short'] != 'undefined'):
            resp = Add_publication_query(admin_config).run(request.args)
            # returns either id of new publication or false
            return jsonify(resp)

        # data is missing, get from DOI
        else:
            publication['doi'] = doi
            publication['citation_long'] = Obtain_Citation().run(doi)
            publication['citation_short'] = Obtain_Citation_Short().run(doi)
            return jsonify(publication)

    except Exception as e:
        fapp.logger.info(e)


@fapp.route("/admin/v1/read_publication", methods=['GET'])
@requires_auth
def read_publication():
    """
    Add a publication by DOI

    Parameters
    ----------
    id: int publication id in the database
    """
    publication = Read_publication_query(admin_config).run(request.args['id'])
    return jsonify(publication)


if __name__ == '__main__':
    try:
        # Read the configuration file
        admin_config = configparser.ConfigParser()
        admin_config.read(configPath)
        fapp.run(host='0.0.0.0')
    except Exception as e:
        fapp.logger.info(e)

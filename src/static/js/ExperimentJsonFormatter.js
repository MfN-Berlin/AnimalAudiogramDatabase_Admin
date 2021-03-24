class ExperimentJsonFormatter extends AbstractJsonFormatter {
    constructor(dao) {
        super(dao);
    }
    
    /**
     * Displays an audiogram's experiment details as a HTML table.
     * @param audiogramId: int id of an audiogram
     * @param jsonObj: dict as returned by Audiogram.readDataPoints()
     */
    format(audiogramId, jsonObj) {
        var resp = `
            ${this.format_pulldown_keyval(
               'Publication', 
               'citation_id', 
               jsonObj.citation_id,
               this._read_publication_options()
            )}
            <div id="filters display_experiment_details">
            ${this.format_pulldown(
               'Measurement type', 
               'measurement_type', 
               jsonObj.measurement_type,
               ['auditory threshold', 'critical ratio', 'critical bandwidth', 'time period of integration', 'TTS - Temporary Threshold Shift', 'PTS - Permanent Threshold Shift', 'signal duration test'] 
            )}
            ${this.format_input('Number of measurements', 'number_of_measurements', jsonObj.number_of_measurements)}
            ${this.format_pulldown_keyval(
               'Facility name', 
               'facility_id', 
               jsonObj.facility_id,
               this._read_facility_name_options()
            )}
            ${this.format_input('Latitude in decimal degree', 'latitude_in_decimal_degree', jsonObj.latitude_in_decimal_degree)}
            ${this.format_input('Longitude in decimal degree', 'longitude_in_decimal_degree', jsonObj.longitude_in_decimal_degree)}
            ${this.format_text('Position of animal', 'position_of_animal', jsonObj.position_of_animal)}
            ${this.format_input('Distance to sound source in meter', 'distance_to_sound_source_in_meter', jsonObj.distance_to_sound_source_in_meter)}
            ${this.format_text('Test environment description', 'test_environment_description', jsonObj.test_environment_description)}
            ${this.format_pulldown(
               'Medium', 
               'medium', 
               jsonObj.medium, 
               ['air', 'water']
            )}
            ${this.format_pulldown_keyval(
               'Measurement method', 
               'measurement_method_id', 
               jsonObj.measurement_method_id,
               this._read_measurement_method_options()
            )}
            ${this.format_text('Position first electrode', 'position_first_electrode', jsonObj.position_first_electrode)}
            ${this.format_text('Position second electrode', 'position_second_electrode', jsonObj.position_second_electrode)}
            ${this.format_text('Position third electrode', 'position_third_electrode', jsonObj.position_third_electrode)}
            ${this.format_input('Year of experiment start', 'year_of_experiment_start', jsonObj.year_of_experiment_start)}​​
            ${this.format_input('Year of experiment end', 'year_of_experiment_end', jsonObj.year_of_experiment_end)}​​
            ${this.format_text('Calibration', 'calibration', jsonObj.calibration)}
            ${this.format_input(
               'Threshold determination info', 
               'threshold_determination_method', 
               jsonObj.threshold_determination_method
            )}
            ${this.format_pulldown_keyval(
               'Testtone form method', 
               'testtone_form_method_id', 
               jsonObj.testtone_form_method_id,
               this._read_testtone_form_method_options()
            )}
            ${this.format_pulldown(
               'Testtone presentation staircase', 
               'testtone_presentation_staircase', 
               jsonObj.testtone_presentation_staircase, 
               ['yes', 'no', 'unknown']
            )}
            ${this.format_pulldown(
               'Testtone presentation method constants', 
               'testtone_presentation_method_constants', 
               jsonObj.testtone_presentation_method_constants, 
               ['yes', 'no', 'unknown']
            )}
            ${this.format_pulldown(
               'Testtone presentation sound form', 
               'testtone_presentation_sound_form', 
               jsonObj.testtone_presentation_sound_form,
               ['click', 'tone-pips', 'pip trains','prolonged','SAM (sinusoidal amplitude modulation)']
            )}
            ${this.format_pulldown(
               'Sedated', 
               'sedated', 
               jsonObj.sedated, 
               ['yes', 'no', 'unknown']
            )}
            ${this.format_text('Sedation details', 'sedation_details', jsonObj.sedation_details)}
            ${this.format_input('Background noise in decibel', 'background_noise_in_decibel', jsonObj.background_noise_in_decibel)}
           </div>`;
        return resp;
    }

    _read_publication_options() {
        var url = '/admin/v1/all_publications';
        var json = this.dao.httpGet(url);
        var obj = JSON.parse(json);
        var dict = {};
        for (var i in obj) {
            var key = obj[i].id;
            var val = obj[i].citation_short;
            dict[key] = val;
        }
        return dict;
    }
    
    _read_facility_name_options() {
        var url = '/admin/v1/all_facilities';
        var json = this.dao.httpGet(url);
        var obj = JSON.parse(json);
        var dict = {};
        for (var i in obj) {
            var key = obj[i].id;
            var val = obj[i].name;
            dict[key] = val;
        }
        return dict;
    }

    _read_measurement_method_options() {
        var url = '/admin/v1/all_measurement_methods';
        var json = this.dao.httpGet(url);
        var obj = JSON.parse(json);
        var dict = {};
        for (var i in obj) {
            var key = obj[i].method_id;
            var val = obj[i].method_name;
            dict[key] = val;
        }
        return dict;
    }

    _read_testtone_form_method_options() {
        var url = '/admin/v1/all_tone_methods';
        var json = this.dao.httpGet(url);
        var obj = JSON.parse(json);
        var dict = {};
        for (var i in obj) {
            var key = obj[i].method_id;
            var val = obj[i].method_name;
            dict[key] = val;
        }
        return dict;        
    }
    
}

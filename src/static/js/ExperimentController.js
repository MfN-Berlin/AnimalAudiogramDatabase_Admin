class ExperimentController extends AbstractController {
    /** 
     * Controller for edit experiment metadata page
     * @param view: object that can format the json returned by the server
     */
    constructor(view, dao) {
        super();
        this.view = view;
        this.dao = dao;
    }

    /**Displays an empty experiment input form*/
    new() {
        var newJson = this.dao.new(); // create a new empty json onbject
        this._showOutput(0, newJson);
    }

    create() {
        try {
            this._toggleSaveThrobber();
            this._readFromForm();
            this.dao.id = 0; // 0 stands for new
            var json = this.dao.save();
            if (json == 'False') throw('Error while saving data');
            var jsonObj = JSON.parse(json)[0];
            var newId = jsonObj['max(id)'];
            alert(`Audiogram id ${newId} has been created`);
            this.dao.id = newId;
            window.location.replace(`/admin/v1/edit_experiment_metadata?newid=${newId}`);
            
        } catch(e) {
            console.log(e);
            alert(e);
        }
        this._toggleSaveThrobber();
    }
    
    /**Reads an experiment's details from the database.*/
    read() {
        try {
            this._toggleEditThrobber();
            var id = parseInt(document.getElementById('edit_id').value);
            var outputEl = this._clearOutput();
            
            // read data from db
            var jsonObj = this.dao.read(id);
            if (!jsonObj) throw `Error reading experiment data for audiogram ${id}`;
            //console.log(jsonObj)
            this._showOutput(id, jsonObj);

        } catch(e) {
            console.log(e);
            alert(e);
        }
        this._toggleEditThrobber();
    }

    
    /**Saves an experiment's details to the database.*/
    save() {
        try {
            this._toggleSaveThrobber();
            this._readFromForm();
            this.dao.save();

            // make sure the edit input is showing the correct id, reload data from server
            document.getElementById('edit_id').value = this.dao.id;
            this.read();
            
        } catch(e) {
            console.log(e);
            alert(e);
        }
        this._toggleSaveThrobber();
    }

    /** Reads data from form and stores it in this.dao */
    _readFromForm() {
        this.dao.citation_id = document.getElementById('citation_id').value;
        this.dao.ott_id = document.getElementById('ott_id').value;
        this.dao.background_noise_in_decibel = document.getElementById('background_noise_in_decibel').value;
        this.dao.calibration = document.getElementById('calibration').value;
        this.dao.distance_to_sound_source_in_meter = document.getElementById('distance_to_sound_source_in_meter').value;
        this.dao.facility_id = document.getElementById('facility_id').value;
        this.dao.latitude_in_decimal_degree = document.getElementById('latitude_in_decimal_degree').value;
        this.dao.longitude_in_decimal_degree = document.getElementById('longitude_in_decimal_degree').value;
        this.dao.measurement_method_id = document.getElementById('measurement_method_id').value;
        this.dao.measurement_type = document.getElementById('measurement_type').value;
        this.dao.medium = document.getElementById('medium').value;
        this.dao.number_of_measurements = document.getElementById('number_of_measurements').value;
        this.dao.position_first_electrode = document.getElementById('position_first_electrode').value;
        this.dao.position_second_electrode = document.getElementById('position_second_electrode').value;
        this.dao.position_third_electrode = document.getElementById('position_third_electrode').value;
        this.dao.position_of_animal = document.getElementById('position_of_animal').value;
        this.dao.sedated = document.getElementById('sedated').value;
        this.dao.sedation_details = document.getElementById('sedation_details').value;
        this.dao.test_environment_description = document.getElementById('test_environment_description').value;
        this.dao.testtone_form_method_id = document.getElementById('testtone_form_method_id').value;
        this.dao.testtone_presentation_method_constants = document.getElementById('testtone_presentation_method_constants').value;
        this.dao.testtone_presentation_sound_form = document.getElementById('testtone_presentation_sound_form').value;
        this.dao.testtone_presentation_staircase = document.getElementById('testtone_presentation_staircase').value;
        this.dao.threshold_determination_method = document.getElementById('threshold_determination_method').value;
        this.dao.year_of_experiment_start = document.getElementById('year_of_experiment_start').value;
        this.dao.year_of_experiment_end = document.getElementById('year_of_experiment_end').value;
    }
    
    _clearOutput() {
        var outputEl = document.getElementById('output');
        outputEl.innerHTML = '';
        document.getElementById('page_actions').style.display='none';
        return outputEl;
    }

    _showOutput(id, jsonObj) {
        var outputEl = document.getElementById('output');
        // display metadata as HTML table
        outputEl.innerHTML = this.view.format(id, jsonObj);
        // show save button
        document.getElementById('page_actions').style.display='block';
    }
}

class ExperimentDAO extends AbstractDAO {
    /** 
     * Object representing an experiment
     * @param id: int id of an audiogram (or experiment)
     */
    constructor() {
        super();
    }
    
    /**Gets experiment details.*/
    read(id) {
        if (!Number.isInteger(id)) {
            throw 'No audiogram id given';
            
        } else {
            this.id = id;
        }
        var edit_url = `/admin/v1/edit_experiment_metadata?id=${this.id}`;
        try {
            var json = this.httpGet(edit_url);
            var jsonObj = JSON.parse(json)[0];
        } catch(e) {
            console.log(e);
            return false;
        }
        return jsonObj;
    }

    /**Saves experiment details*/
    save() {
        var url = `/admin/v1/save_experiment?id=${this.id}`;
        url += `&citation_id=${this.citation_id}`;
        url += `&background_noise_in_decibel=${this.background_noise_in_decibel}`;
        url += `&calibration=${this.calibration}`;
        url += `&distance_to_sound_source_in_meter=${this.distance_to_sound_source_in_meter}`;
        url += `&facility_id=${this.facility_id}`;
        url += `&latitude_in_decimal_degree=${this.latitude_in_decimal_degree}`;
        url += `&longitude_in_decimal_degree=${this.longitude_in_decimal_degree}`;
        url += `&measurement_method_id=${this.measurement_method_id}`;
        url += `&measurement_type=${this.measurement_type}`;
        url += `&medium=${this.medium}`;
        url += `&number_of_measurements=${this.number_of_measurements}`;
        url += `&position_first_electrode=${this.position_first_electrode}`;
        url += `&position_second_electrode=${this.position_second_electrode}`;
        url += `&position_third_electrode=${this.position_third_electrode}`;
        url += `&position_of_animal=${this.position_of_animal}`;
        url += `&sedated=${this.sedated}`;
        url += `&sedation_details=${this.sedation_details}`;
        url += `&test_environment_description=${this.test_environment_description}`;
        url += `&testtone_form_method_id=${this.testtone_form_method_id}`;
        url += `&testtone_presentation_method_constants=${this.testtone_presentation_method_constants}`;
        url += `&testtone_presentation_sound_form=${this.testtone_presentation_sound_form}`;
        url += `&testtone_presentation_staircase=${this.testtone_presentation_staircase}`;
        url += `&threshold_determination_method=${this.threshold_determination_method}`;
        url += `&year_of_experiment_start=${this.year_of_experiment_start}`;
        url += `&year_of_experiment_end=${this.year_of_experiment_end}`;
        
        var resp = this.httpGet(url);
        return resp;
    }
    
    /**
     * Delete an audiogram from the database. 
     * If the deleted audiogram is the only audiogram for the corresponding publication, 
     * facility, experiment or animal, these will be deleted too. 
     * Deletions are permanent, deleted audiograms cannot be undeleted, this action cannot be undone. 
     */
    delete() {
        var delete_url = `/admin/v1/delete_experiment?id=${this.id}`
        var resp = this.httpGet(delete_url);
        if (resp == 'True') {
            return resp;
        } else {
            throw `Error while attempting to delete audiogram ${this.id}`
        }
    }

    new() {
       var jsonObj = JSON.parse(`
[
  {
    "citation_id": null,
    "measurement_type": null, 
    "number_of_measurements": null, 
    "facility_id": null, 
    "latitude_in_decimal_degree": null, 
    "longitude_in_decimal_degree": null, 
    "position_of_animal": null, 
    "distance_to_sound_source_in_meter": null, 
    "test_environment_description": null, 
    "medium": null, 
    "measurement_method_id": null, 
    "position_first_electrode": null, 
    "position_second_electrode": null, 
    "position_third_electrode": null, 
    "year_of_experiment_end": null, 
    "year_of_experiment_start": null,
    "calibration": null, 
    "threshold_determination_method": null, 
    "testtone_form_method_id": null, 
    "testtone_presentation_staircase": null, 
    "testtone_presentation_method_constants": null, 
    "testtone_presentation_sound_form": null, 
    "sedated": null, 
    "sedation_details": null, 
    "background_noise_in_decibel": null
  }
]`);

        return jsonObj;
    }
}

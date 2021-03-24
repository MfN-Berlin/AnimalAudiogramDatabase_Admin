class DataPointDAO extends AbstractDAO {
    /**
     * Object representing a data point
     * @param id: int id of a ata point
     */
    constructor(id) {
        super();
        this.id = id;
    }
    
    /**Gets all data points from an audiogram.*/
    readDataPoints(expId) {
        var edit_url = `/admin/v1/edit_data_points?id=${expId}`
        try {
            var json = this.httpGet(edit_url);
            var jsonObj = JSON.parse(json);
        } catch(e) {
            console.log(e);
            return false;
        }
        return jsonObj;
    }

    /**Creates a new datapoint in the database*/
    create() {
        var url = `/admin/v1/create_data_point?`;
        url += `testtone_frequency_in_khz=${this.testtone_frequency_in_khz}`;
        url += `&sound_pressure_level_in_decibel=${this.sound_pressure_level_in_decibel}`;
        url += `&testtone_duration_in_millisecond=${this.testtone_duration_in_millisecond}`;
        url += `&sound_pressure_level_reference=${this.sound_pressure_level_reference}`;
        url += `&sound_pressure_level_reference_method=${this.sound_pressure_level_reference_method}`;
        url += `&audiogram_experiment_id=${this.audiogram_experiment_id}`;
        var resp = this.httpGet(url);
    }
    
    /**Saves a single data point to the database.*/
    save() {
        var url = `/admin/v1/save_data_point?id=${this.id}`;
        url += `&testtone_frequency_in_khz=${this.testtone_frequency_in_khz}`;
        url += `&sound_pressure_level_in_decibel=${this.sound_pressure_level_in_decibel}`;
        url += `&testtone_duration_in_millisecond=${this.testtone_duration_in_millisecond}`;
        url += `&sound_pressure_level_reference=${this.sound_pressure_level_reference}`;
        url += `&sound_pressure_level_reference_method=${this.sound_pressure_level_reference_method}`;
        var resp = this.httpGet(url);
    }

    /**Deletes a data point from the database*/
    delete() {
        var url = `/admin/v1/delete_data_point?id=${this.id}`;
        var resp = this.httpGet(url);        
    }
}


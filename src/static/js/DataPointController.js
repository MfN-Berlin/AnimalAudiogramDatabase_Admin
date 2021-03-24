class DataPointController extends AbstractController {
    /** 
     * Controller for edit data page
     * @param view: object that can format the json returned by the server
     */
    constructor(view, dao) {
        super();
        this.view = view;
        this.dao = dao;
    }

    /**Reads an audiogram's data points from the database.*/
    read() {
        try {
            this._toggleEditThrobber();
            var id = parseInt(document.getElementById('edit_id').value);
            var outputEl = this._clearOutput();
            
            // read data from db
            var jsonObj = this.dao.readDataPoints(id);
            if (!jsonObj) throw `Error reading audiogram ${id}`; 
            this._showOutput(id, jsonObj)

        } catch(e) {
            alert(e);
        }
        this._toggleEditThrobber();
    }

    /** (un-) mark a data point for deletion*/
    trashToggle(dpId) {
        var trEl = document.querySelector(`tr#datapoint_${dpId}`);
        // mark for deletion
        if ((trEl.className=='datapoint')) {
            trEl.className = 'datapoint_deleted';
            var trInputs = document.querySelectorAll(`tr#datapoint_${dpId} input,tr#datapoint_${dpId} select`);
            for(var i = 0; i < trInputs.length; i++) {
                trInputs[i].disabled = true;
            }
        // unmark
        } else {
            trEl.className = 'datapoint';
            var trInputs = document.querySelectorAll(`tr#datapoint_${dpId} input,tr#datapoint_${dpId} select`);
            for(var i = 0; i < trInputs.length; i++) {
                trInputs[i].disabled = false;
            }
        }
    }
    
    /**Saves an audiogram's data points to the database.*/
    save() {
        try {
            this._toggleSaveThrobber();
            var expId = this._parseAudiogramId();

            // Save existing and new datapoints
            var dpEls = this._allDataPoints();
            if (dpEls.length == 0) throw 'No data points, enter the id of the audiogram to edit and click on edit';
            for (var i = 0; i < dpEls.length; i++) {
                var dpEl = dpEls[i];
                var dataPoint = this._parseDataPoint(expId, dpEl);
                if (!dataPoint) continue; // ignore datapoints without frequency or SPL
                
                if (dataPoint.id == -1) // new data point has id=-1
                    dataPoint.create();
                else
                    dataPoint.save(); // save existing data point
            }
            
            // Deleted data points marked for deletion
            var delEls = this._delDataPoints();
            for (var i = 0; i < delEls.length; i++) {
                var id = parseInt(delEls[i].id.split('_')[1]);
                new DataPointDAO(id).delete()
            }
            
            // make sure the edit input is showing the correct id, reload data from server
            document.getElementById('edit_id').value = expId;
            this.read();
            
        } catch(e) {
            alert(e);
        }
        this._toggleSaveThrobber();
    }

    /**The audiogram's id is stored in the css id of the output table*/
    _parseAudiogramId() {
        return parseInt(document.querySelector('table.audiogram').id.split('_')[1]);
    }

    /**Each row in the output table is a data point, plus one empty row to create a new data point*/
    _allDataPoints() {
        return document.querySelectorAll('.datapoint, .datapoint_new');
    }
    
    /**Datapoints marked for deletion have the css class datapoint_deleted*/
    _delDataPoints() {
        return document.querySelectorAll('.datapoint_deleted');
    }

    /**
     * Parse the data point data from the HTML table row dpEl
     * @param expId: int id of an audiogram
     * @dpEl HTML element, table row with DataPoint
     * @return DataPoint object
     */
    _parseDataPoint(expId, dpEl) {
        var elementId = dpEl.id;
        var id = -1; // new data points have id=-1
        if (elementId != 'datapoint_new')
            var id = parseInt(elementId.split('_')[1]); // existing data points have an id
        
        var dataPoint = new DataPointDAO(id);
        
        // kHz
        var kHz = document.getElementById(`${elementId}_testtone_frequency_in_khz`).value;
        if (kHz == '') return false; // ignore data points without frequency
        dataPoint.testtone_frequency_in_khz = parseFloat(kHz);
        // dB
        var dB = document.getElementById(`${elementId}_sound_pressure_level_in_decibel`).value;
        if (dB == '') return false; // ignore data points without SPL
        dataPoint.sound_pressure_level_in_decibel = parseFloat(dB);
        // millis
        var millis = document.getElementById(`${elementId}_testtone_duration_in_millisecond`).value;
        if (millis)
            dataPoint.testtone_duration_in_millisecond = parseFloat(millis);
        // reference id
        dataPoint.sound_pressure_level_reference =
            parseInt(document.getElementById(`${elementId}_sound_pressure_level_reference`).value);
        // string
        dataPoint.sound_pressure_level_reference_method =
            document.getElementById(`${elementId}_sound_pressure_level_reference_method`).value;
        // experiment id
        dataPoint.audiogram_experiment_id = expId;

        return dataPoint;
    }
    
    _clearOutput() {
        var outputEl = document.getElementById('output');
        outputEl.innerHTML = '';
        document.getElementsByClassName('help2')[0].style.display='none';
        document.getElementById('page_actions').style.display='none';
        return outputEl;
    }

    _showOutput(id, jsonObj) {
        var outputEl = document.getElementById('output');
        // display audiogram as HTML table
        outputEl.innerHTML = this.view.format(id, jsonObj);
        // show help continued and save button
        document.getElementsByClassName('help2')[0].style.display='block';
        document.getElementById('page_actions').style.display='block';
    }
}

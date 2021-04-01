class AnimalController extends AbstractController {
    /** 
     * Controller for edit animal metadata page
     * @param view: object that can format the json returned by the server
     */
    constructor(view, dao) {
        super();
        this.view = view;
        this.dao = dao;
    }

    /**Reads an animal's details from the database.*/
    read() {
        try {
            this._toggleEditThrobber();
            var expId = parseInt(document.getElementById('edit_id').value);
            var outputEl = this._clearOutput();
            
            // read data from db
            var jsonObj = this.dao.read(expId);
            if (!jsonObj) throw `Error reading animal data for audiogram ${expId}`; 
            this._showOutput(expId, jsonObj);

        } catch(e) {
            console.log(e);
            alert(e);
        }
        this._toggleEditThrobber();
    }

    
    /**Saves an animal's details to the database.*/
    save() {
        try {
            this._toggleSaveThrobber();

            this.dao.age = document.getElementById('age').value;
            this.dao.captivity = document.getElementById('captivity').value;
            this.dao.ott_id = document.getElementById('vernacular_selector').value;
            this.dao.sex = document.getElementById('sex_selector').value;
            this.dao.liberty = document.getElementById('liberty_selector').value;
            this.dao.lifestage = document.getElementById('lifestage_selector').value;
            this.dao.individual_name = document.getElementById('individual_name').value;

            this.dao.save();
            
            // make sure the edit input is showing the correct id, reload data from server
            document.getElementById('edit_id').value = this.dao.expId;
            this.read();
            
        } catch(e) {
            console.log(e);
            alert(e);
        }
        this._toggleSaveThrobber();
    }

    /**The audiogram's id is stored in the css id of the output table*/
    _parseAudiogramId() {
        return parseInt(document.querySelector('table.audiogram').id.split('_')[1]);
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

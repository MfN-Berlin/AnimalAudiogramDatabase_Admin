class TaxonomyController extends AbstractController {
    /** 
     * Controller for edit taxonomy page
     * @param view: object that can format the json returned by the server
     */
    constructor(view, dao) {
        super();
        this.view = view;
        this.dao = dao;
    }

    /** Read species from Open Tree of Life */
    create() {
        try {
            this._toggleEditThrobber();
            var latin_name = document.getElementById('latin_name').value;
            var outputEl = this._clearOutput();
            var jsonObj = this.dao.retrieve(latin_name);
            if (!jsonObj || !jsonObj.species) throw `Error reading taxonomic data. Is the latin name spelled correctly?`; 
            this._showOutput(latin_name, jsonObj);
            
        } catch(e) {
            console.log(e);
            alert(e);
        }
        this._toggleEditThrobber();
    }

    /**Saves a taxon's details to the database.*/
    save() {
        this._toggleSaveThrobber();
        try {
            this._readFromForm();
            var resp = this.dao.save();
            if (!resp) {
                alert("Error while saving taxon.")
            } else {
                var jsonObj = JSON.parse(resp);
                if (jsonObj[0].response == false ) {
                    alert(jsonObj[1].response);
                } else {
                    console.log(this.dao)
                    // make sure the latin name input field is showing the correct name, reload data from server
                    document.getElementById('latin_name').value = this.dao.unique_name;
                    alert('Saved');
                }
            }
        } catch(e) {
            alert(e);
            console.log(e);
        }
        this._toggleSaveThrobber();
    }

    
    /* Private methods */
    
    /** Reads data from form and stores it in this.dao */
    _readFromForm() {
        this.dao.phylum = document.getElementById('phylum').value;
        this.dao.phylum_ott_id = document.getElementById('phylum_ott_id').value;
        this.dao.class = document.getElementById('class').value;
        this.dao.class_ott_id = document.getElementById('class_ott_id').value;
        this.dao.order = document.getElementById('order').value;
        this.dao.order_ott_id = document.getElementById('order_ott_id').value;
        this.dao.family = document.getElementById('family').value;
        this.dao.family_ott_id = document.getElementById('family_ott_id').value;
        this.dao.genus = document.getElementById('genus').value;
        this.dao.genus_ott_id = document.getElementById('genus_ott_id').value;
        this.dao.species = document.getElementById('species').value;
        this.dao.species_ott_id = document.getElementById('species_ott_id').value;
        this.dao.unique_name = document.getElementById('unique_name').value;
        this.dao.vernacular_name = document.getElementById('vernacular_name').value;

        if (this.dao.ott_id =='' || this.dao.phylum == '' || this.dao.class == '' || 
            this.dao.order == '' || this.dao.family == '' || this.dao.genus == '' ||
            this.dao.species == '' || this.dao.unique_name == '' ||
            this.dao.vernacular_name == '') throw('Please fill all fields');
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

class PublicationController extends AbstractController {
    /** 
     * Controller for edit experiment metadata page
     * @param view: object that can format the json returned by the server
     */
    constructor(view, dao) {
        super();
        this.view = view;
        this.dao = dao;
    }

    /**Displays an empty publication input form*/
    new() {
        var newJson = this.dao.new(); // create a new empty json onbject
        this._showOutput(0, newJson);
    }

    /** Read publication by DOI */
    create() {
        try {
            this._toggleEditThrobber();
            this.dao = new PublicationDAO();
            this.dao.doi = document.getElementById('doi').value;
            if (!this.dao.doi) throw('No DOI given');
            var json = this.dao.save();
            var jsonObj = JSON.parse(json);
            if (jsonObj.citation_long == undefined) {
                alert('Could not retrieve data from IDF. Is the DOI correct?');
            } else {
                this._showOutput(jsonObj.doi, jsonObj);
            }
        } catch(e) {
            console.log(e);
            alert(e);
        }
        this._toggleEditThrobber();
    }
    
    /**Reads a publication's details from the database.*/
    read(id) {
        try {
            var outputEl = this._clearOutput();
            
            // read data from db
            var json = this.dao.read(id);
            if (!json) throw `Error reading audiogram ${id}`;
            var jsonObj = JSON.parse(json);
            this._showOutput(id, jsonObj[0])

        } catch(e) {
            alert(e);
        }
    }

    
    /**Saves a publication's details to the database.*/
    save() {
        this._toggleSaveThrobber();
        try {
            this._readFromForm();
            var resp = this.dao.save();
            if (!resp) {
                alert("Error while saving publication.")
            } else {
                var jsonObj = JSON.parse(resp);
                // make sure the DOI input is showing the correct DOI, reload data from server
                document.getElementById('doi').value = this.dao.doi;
                this.read(jsonObj[0]['max(id)']);
            }
        } catch(e) {
            alert(e);
        }
        this._toggleSaveThrobber();
    }

    /** Reads data from form and stores it in this.dao */
    _readFromForm() {
        this.dao.doi = document.getElementById('doi').value;
        this.dao.citation_long = document.getElementById('citation_long').value;
        this.dao.citation_short = document.getElementById('citation_short').value;
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

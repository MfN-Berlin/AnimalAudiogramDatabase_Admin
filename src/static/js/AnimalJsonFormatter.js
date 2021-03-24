class AnimalJsonFormatter extends AbstractJsonFormatter {
    constructor(dao) {
        super(dao);
    }
    
    /**
     * Displays an audiogram's animal details as a HTML table.
     * @param audiogramId: int id of an audiogram
     * @param jsonObj: dict as returned by Audiogram.readDataPoints()
     */
    format(audiogramId, jsonObj) {
        var resp = `
            <div id="filters display_animal_details">
               ${this._format_vernacular_selector(jsonObj.ott_id)}
               ${this._format_name_input(jsonObj.individual_name)}
               ${this._format_sex_selector(jsonObj.sex)}
               ${this._format_liberty_selector(jsonObj.liberty_status)}
               ${this._format_lifestage_selector(jsonObj.life_stage)}
               ${this._format_age_input(jsonObj.age_in_month)}
               ${this._format_captivity_input(jsonObj.captivity_duration_in_month)}
           </div>`;
        return resp;
    }

    _format_age_input(age) {
        if (age == null) age = '';
        var resp = `
               <div class="filter_label">Age of the animal (months)</div>
               <input type="text" id="age" size="4" placeholder="" value="${age}">`;
        return resp;
    }
    
    _format_captivity_input(duration) {
        if (duration == null) duration = '';
        var resp = `
               <div class="filter_label">Duration in captivity (months)</div>
               <input type="text" id="captivity" size="4" placeholder="" value="${duration}">`;
        return resp;
    }
    
    _format_name_input(name) {
        if (name == null) name = '';
        var resp = `
               <div class="filter_label">Name of the individual animal</div>
               <input type="text" id="individual_name" size="4" placeholder="" value="${name}">`;
        return resp;
    }
    
    /**
     * Draws a selector for vernacular names.
     * Vernacular names are read from the database.
     * @param selected: int id of the selected vernacular name 
     * @returns: HTML string
     */
    _format_vernacular_selector(selected) {
        var url = '/admin/v1/all_species_vernacular';
        var json = this.dao.httpGet(url);
        console.log(json)
        var obj = JSON.parse(json);
        
        var resp = "";
        for (var i in obj) {
            var option = obj[i];
            if (selected == option.ott_id) {
                resp += `<option value="${option.ott_id}" selected>${option.vernacular_name_english}</option>`
            } else {
                resp += `<option value="${option.ott_id}">${option.vernacular_name_english}</option>`
            }
        }
        return `
           <label class="filter_label" for="vernacular_selector">Species (English name)</label>
           <select id="vernacular_selector">
           ${resp}
           </select>`;
    }

    _format_sex_selector(selected) {
        var obj = ['', 'female', 'male'];
        var resp = "";
        for (var i in obj) {
            var option = obj[i];
            if (selected == option) {
                resp += `<option value="${option}" selected>${option}</option>`
            } else {
                resp += `<option value="${option}">${option}</option>`
            }
        }
        return `
           <label class="filter_label" for="sex_selector">Sex</label>
           <select id="sex_selector">
           ${resp}
           </select>`;
    }

    _format_liberty_selector(selected) {
        var obj = ['', 'captive', 'stranded', 'wild'];
        var resp = "";
        for (var i in obj) {
            var option = obj[i];
            if (selected == option) {
                resp += `<option value="${option}" selected>${option}</option>`
            } else {
                resp += `<option value="${option}">${option}</option>`
            }
        }
        return `
           <label class="filter_label" for="liberty_selector">Liberty status</label>
           <select id="liberty_selector">
           ${resp}
           </select>`;
    }
    
    _format_lifestage_selector(selected) {
        var obj = ['', 'juvenile', 'sub-adult', 'adult'];
        var resp = "";
        for (var i in obj) {
            var option = obj[i];
            if (selected == option) {
                resp += `<option value="${option}" selected>${option}</option>`
            } else {
                resp += `<option value="${option}">${option}</option>`
            }
        }
        return `
           <label class="filter_label" for="lifestage_selector">Life stage</label>
           <select id="lifestage_selector">
           ${resp}
           </select>`;
    }
}

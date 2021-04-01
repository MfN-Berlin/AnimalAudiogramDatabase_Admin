class AnimalDAO extends AbstractDAO {
    /** 
     * Object representing an audiogram
     * @param expId: int id of an audiogram
     */
    constructor(expId) {
        super();
    }

    retrieve(latin_name) {
        if (!latin_name) {
            throw 'No latin name given';
        }
        var retrieve_url = `/admin/v1/retrieve_species_otl?latin_name=${latin_name}`;
        try {
            var json = this.httpGet(retrieve_url);
            var jsonObj = JSON.parse(json);

        } catch(e) {
            console.log(e);
            return false;
        }
        return jsonObj;
    }
    
    /**Gets animal details.*/
    read(expId) {
        if (!Number.isInteger(expId)) {
            throw 'No audiogram id given';
            
        } else {
            this.expId = expId;
        }
        var edit_url = `/admin/v1/edit_animal_metadata?expId=${expId}`;
        try {
            var json = this.httpGet(edit_url);
            var jsonObj = JSON.parse(json)[0];
        } catch(e) {
            console.log(e);
            return false;
        }
        return jsonObj;
    }

    /**Saves animal details*/
    save() {
        var url = `/admin/v1/save_animal?expId=${this.expId}`;
        url += `&age=${this.age}`;
        url += `&captivity=${this.captivity}`;
        url += `&ott_id=${this.ott_id}`;
        url += `&sex=${this.sex}`;
        url += `&liberty=${this.liberty}`;
        url += `&lifestage=${this.lifestage}`;
        url += `&individual_name=${this.individual_name}`;
        var resp = this.httpGet(url);
    }
    
}

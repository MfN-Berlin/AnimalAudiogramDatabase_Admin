class AnimalDAO extends AbstractDAO {
    /** 
     * Object representing an audiogram
     * @param expId: int id of an audiogram
     */
    constructor(expId) {
        super();
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

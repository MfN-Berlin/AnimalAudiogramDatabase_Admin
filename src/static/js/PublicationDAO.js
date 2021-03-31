class PublicationDAO extends AbstractDAO {
    /** 
     * Object representing a publication
     */
    constructor() {
        super();
    }
    
    /**Gets publication by id.*/
    read(id) {
        if (!id) {
            throw 'No id given';
            
        }
        var read_url = `/admin/v1/read_publication?id=${id}`;
        try {
            var json = this.httpGet(read_url);

        } catch(e) {
            console.log(e);
            return false;
        }
        return json;
    }

    /**Saves publication details*/
    save() {
        var citation_long = encodeURIComponent(this.citation_long);
        var citation_short = encodeURIComponent(this.citation_short);
        var url = `/admin/v1/save_publication?doi=${this.doi}`;
        url += `&citation_long=${citation_long}`;
        url += `&citation_short=${citation_short}`;
        return this.httpGet(url);
    }
    
}

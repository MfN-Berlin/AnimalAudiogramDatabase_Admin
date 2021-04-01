class TaxonomyDAO extends AbstractDAO {
    /** 
     * Object representing a taxonomic entry
     */
    constructor() {
        super();
    }

    /** Retrieve taxonomy from Open Tree of Life */
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

    /**Saves taxon details*/
    save() {
        var url = `/admin/v1/add_taxon?`;
        url += `phylum=${this.phylum}`;
        url += `&phylum_ott_id=${this.phylum_ott_id}`;
        url += `&class=${this.class}`;
        url += `&class_ott_id=${this.class_ott_id}`;
        url += `&order=${this.order}`;
        url += `&order_ott_id=${this.order_ott_id}`;
        url += `&family=${this.family}`;
        url += `&family_ott_id=${this.family_ott_id}`;
        url += `&genus=${this.genus}`;
        url += `&genus_ott_id=${this.genus_ott_id}`;
        url += `&species=${this.species}`;
        url += `&species_ott_id=${this.species_ott_id}`;
        url += `&unique_name=${this.unique_name}`;
        url += `&vernacular_name=${this.vernacular_name}`;
        return this.httpGet(url);
    }
}

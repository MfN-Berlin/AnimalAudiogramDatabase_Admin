class TaxonomyJsonFormatter extends AbstractJsonFormatter {
    constructor(dao) {
        super(dao);
    }
    
    /**
     * Displays a taxonomic entry's details as a HTML table.
     * @param latin_name: string
     * @param jsonObj: dict lineage
     */
    format(audiogramId, jsonObj) {
        var resp = `
            <div id="filters display_taxon_details">
               ${this.format_input_long('English name', 'vernacular_name', jsonObj.vernacular_name)}
               ${this.format_input_long_disabled('Phylum', 'phylum', jsonObj.phylum.name)}`
        
        if(jsonObj.class) {
            resp += `
               ${this.format_input_long_disabled('Class', 'class', jsonObj.class.name)}
               ${this.format_hidden('class_ott_id', jsonObj.class.ott_id)}`
        } else {
            resp += `
               ${this.format_input_long('Class', 'class', 'n/a')}
               ${this.format_hidden('class_ott_id', '0')}`
        }

        resp += `${this.format_input_long_disabled('Order', 'order', jsonObj.order.name)}
               ${this.format_input_long_disabled('Family', 'family', jsonObj.family.name)}
               ${this.format_input_long_disabled('Genus', 'genus', jsonObj.genus.name)}
               ${this.format_input_long_disabled('Species', 'species', jsonObj.species.name)}
               ${this.format_input_long_disabled('Unique name', 'unique_name', jsonObj.unique_name)}
               
               ${this.format_hidden('phylum_ott_id', jsonObj.phylum.ott_id)}
               ${this.format_hidden('order_ott_id', jsonObj.order.ott_id)}
               ${this.format_hidden('family_ott_id', jsonObj.family.ott_id)}
               ${this.format_hidden('genus_ott_id', jsonObj.genus.ott_id)}
               ${this.format_hidden('species_ott_id', jsonObj.species.ott_id)}
           </div>`;
        return resp;
    }
}

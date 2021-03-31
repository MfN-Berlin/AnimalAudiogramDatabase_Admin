class PublicationJsonFormatter extends AbstractJsonFormatter {
    constructor(dao) {
        super(dao);
    }
    
    /**
     * Displays a publication's details as a HTML table.
     * @param doi
     * @param jsonObj
     */
    format(doi, jsonObj) {
        var resp = `
            <div id="filters display_publication_details">
            ${this.format_text('Citation long', 'citation_long', this.replace_special_chars(jsonObj.citation_long))}
            ${this.format_text('Citation short', 'citation_short', jsonObj.citation_short)}
            </div>`;
        return resp;
    }
}

class AbstractJsonFormatter {

    constructor(dao) {
        this.dao = dao;
    }

    
    format_input(label, id, val) {
        if (val == null) val = '';
        var resp = `
               <div class="filter_label">${label}</div>
               <input type="text" id="${id}" size="4" placeholder="" value="${val}"/>`;
        return resp;
    }
    
    format_text(label, id, val) {
        if (val == null) val = '';
        var resp = `
               <div class="filter_label">${label}</div>
               <textarea rows="5" cols="120" id="${id}" size="4" placeholder="">${val}</textarea>`;
        return resp;
    }

    format_pulldown(label, id, val, options=[]) {
        var resp = "<option/>";
        for (var i in options) {
            var option = options[i];
            if (val == option) {
                resp += `<option value="${option}" selected>${option}</option>`
            } else {
                resp += `<option value="${option}">${option}</option>`
            }
        }
        return `
           <label class="filter_label">${label}</label>
           <select id="${id}">
           ${resp}
           </select>`;
    }

    format_pulldown_keyval(label, id, val, options=[]) {
        var resp = "<option/>";
        for (var key in options) {
            var option = options[key];
            if (val == key) {
                resp += `<option value="${key}" selected>${option}</option>`
            } else {
                resp += `<option value="${key}">${option}</option>`
            }
        }
        return `
           <label class="filter_label">${label}</label>
           <select id="${id}">
           ${resp}
           </select>`;
    }
}

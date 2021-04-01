class AbstractJsonFormatter {

    constructor(dao) {
        this.dao = dao;
    }

    format_hidden(id, val) {
        var resp = `
               <input type="hidden" id="${id}" value="${val}"/>`;
        return resp;
    }
    
    format_input(label, id, val) {
        if (val == null) val = '';
        var resp = `
               <div class="filter_label">${label}</div>
               <input type="text" id="${id}" size="4" placeholder="" value="${val}"/>`;
        return resp;
    }
    
    format_input_long(label, id, val) {
        if (val == null) val = '';
        var resp = `
               <div class="filter_label">${label}</div>
               <input type="text" id="${id}" size="64" placeholder="" value="${val}"/>`;
        return resp;
    }
    
    format_input_long_disabled(label, id, val) {
        if (val == null) val = '';
        var resp = `
               <div class="filter_label disabled">${label}</div>
               <input type="text" id="${id}" size="64" placeholder="" value="${val}" disabled/>`;
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

    replace_special_chars(str) {
        str = str.replace('â', '-');
        str = str.replace('Ã¢Â€Â¦', '-');
        str = str.replace('Ã¢Â€Â“', '-');
        str = str.replace('Ã¢Â€Â', '-');
        str = str.replace('â€“', '-');
        str = str.replace('Ã¶', 'ö');
        str = str.replace('Ã¸', 'ø');
        str = str.replace('â€™', '\'');
        str = str.replace('Ã¼', 'ü');
        str = str.replace('â€˜', '\'');
        str = str.replace('â€', '');
        str = str.replace('â€˜', '');
        //    str = str.replace("Î¼ ", "\u03BC");
        //    str = str.replace(" Î¼", "\u03BC");
        str = str.replace("Î¼", "\u03BC");
        str = str.replace('“', '-');
        str = str.replace('Â±', '+-');
        str = str.replace('Â°', '°');
        str = str.replace('Â', ' ');
        str = str.replace('-™', "'");    
        return str;
    }
}

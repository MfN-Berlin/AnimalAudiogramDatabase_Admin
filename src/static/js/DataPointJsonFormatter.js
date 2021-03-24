class DataPointJsonFormatter extends AbstractJsonFormatter {
    constructor(dao) {
        super(dao);
    }
    
    /**
     * Displays an audiogram as a HTML table.
     * @param audiogramId: int id of an audiogram
     * @param jsonObj: dict as returned by Audiogram.readDataPoints()
     */
    format(audiogramId, jsonObj) {
        var dataResp = "";
        for (var i in jsonObj) {
            var val = jsonObj[i];
            dataResp += `
               <tr id="datapoint_${val.id}" class="datapoint">
                  <td><input type="text" value="${val.testtone_frequency_in_khz}" id="datapoint_${val.id}_testtone_frequency_in_khz" class="freq_input"/></td>
                  <td><input type="text" value="${val.sound_pressure_level_in_decibel}" id="datapoint_${val.id}_sound_pressure_level_in_decibel" class="spl_input"/></td>
                  <td><input type="text" value="${val.testtone_duration_in_millisecond}" id="datapoint_${val.id}_testtone_duration_in_millisecond" class="ms_input"/></td>
                  <td>${this._format_sound_pressure_level_reference_pulldown(val.id, val.sound_pressure_level_reference_id)}</td>
                  <td>${this._format_spl_reference_method_pulldown(val.id, val.sound_pressure_level_reference_method)}</td>
                  <td><img src="/static/images/trashcan.png" class="delete_icon" onclick="controller.trashToggle(${val.id})"/></td>
               </tr>`;
        }
        var emptyLine = `
               <tr class="datapoint_new" id="datapoint_new">
                  <td><input type="text" id="datapoint_new_testtone_frequency_in_khz" class="freq_input"/></td>
                  <td><input type="text" id="datapoint_new_sound_pressure_level_in_decibel" class="spl_input"/></td>
                  <td><input type="text" id="datapoint_new_testtone_duration_in_millisecond" class="ms_input"/></td>
                  <td>${this._format_sound_pressure_level_reference_pulldown('new', null)}</td>
                  <td>${this._format_spl_reference_method_pulldown('new', null)}</td>
               </tr>`;

        var resp = `
            <table id="experiment_${audiogramId}" class="audiogram">
            <tr>
                <th>Frequency (kHz)</th>
                <th>SPL (dB)</th>
                <th>Duration (ms)</th>
                <th>SPL reference</th>
                <th>Reference method</th>
                <th></th>
            </tr>
            ${dataResp}
            </table>
            Add a new data point
            <table>
            ${emptyLine}
            </table>`;
        return resp;
    }
    
    /**
     * Draws a pulldown for SPL reference.
     * SPL reference values are read from the database.
     * @param id: int id of a data point, or null to create a new data point
     * @param selected: int id of the selected SPL reference 
     * @returns: HTML string
     */
    _format_sound_pressure_level_reference_pulldown(id, selected) {
        var url = `/admin/v1/list_spl_reference`
        var json = this.dao.httpGet(url);
        var obj = JSON.parse(json);
        
        var resp = "<option/>";
        for (var i in obj) {
            var option = obj[i];
            var label = option.spl_reference_display_label.replace("Î¼", "\u03BC");
            if (selected == option.id) {
                resp += `<option value="${option.id}" selected>${label}</option>`
            } else {
                resp += `<option value="${option.id}">${label}</option>`
            }
        }
        return `<select id="datapoint_${id}_sound_pressure_level_reference">${resp}</select>`;
    }

    /**
     * Draws a pulldown for reference methods
     * @param id: int id of a data point, or null to create a new data point
     * @param selected: string selected name of a reference method 
     * @returns: HTML string
     */
    _format_spl_reference_method_pulldown(id, selected) {
        var options = ['', 'root mean squared (RMS)', 'peak to peak (PP)'];
        var resp = "";
        for (var i in options) {
            var option = options[i];
            if (option == selected) {
                resp += `<option selected>${option}</option>`
            } else {
                resp += `<option>${option}</option>`
            }
        }
        return `<select id="datapoint_${id}_sound_pressure_level_reference_method">${resp}</select>`;    
    }
}

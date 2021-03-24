class AbstractController {
    read() {
        raise ("Unimplemented");
    }
    
    save() {
        raise ("Unimplemented");
    }
    
    /**Indicates that the page is loading, next to the edit button*/
    _toggleEditThrobber() {
        var throbber = document.getElementById('edit_throbber')
        throbber.style.display = (throbber.style.display=='')? 'inline': '';
    }
    
    /**Indicates that the page is loading, next to the save button*/
    _toggleSaveThrobber() {
        var throbber = document.getElementById('save_throbber')
        throbber.style.display = (throbber.style.display=='')? 'block': '';
    }
}

class AbstractDAO {
    /**
       Sends a HTTP request, returns response text.
    */
    httpGet(theUrl){
        var xmlHttp = new XMLHttpRequest();
        xmlHttp.open( "GET", theUrl, false );
        xmlHttp.setRequestHeader('Content-Type', 'text/html');
        xmlHttp.setRequestHeader('charset', 'utf-8');
        xmlHttp.send( null );
        return xmlHttp.responseText;
    }
}


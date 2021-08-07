var EventSource = require("eventsource");

var source = new EventSource("/send");
source.addEventListener('greeting', function(event) {
    var data = JSON.parse(event.data);
    // do what you want with this data
}, false);
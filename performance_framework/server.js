var util = require('util'),
    twitter = require('twitter');
    
var twit = new twitter({
    consumer_key: 'pQSAr0PjP7uCpiyMNXKFQ',
    consumer_secret: 'otnGPLDMvE96v3LDEUjR0VA62zoMI8QPDkh6ljGUCM',
    access_token_key: '226118989-WDff2219bGcoqWdiq8oAlF2KhGiqEG28xCzPVMlD',
    access_token_secret: 'i1BIqxrFdSDQx9dTx7QSTDoI8AOJgvfis6nlnF5lw'
});
    
sys = require('sys');

twit.stream('statuses/sample', function(stream) {
    count = 0;
    stream.on('data', function(data) {
      curTime = Date.now();
      tweet = util.inspect(data);
      count += 1;
      console.log(count)      
      // save it to database
    });
});
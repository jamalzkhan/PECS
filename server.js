var express = require('express');
var app = express();
app.use(express.bodyParser());

app.get('/', function(req, res){
  var body = 'Hello World!';
  console.log('get acquired')
  res.setHeader('Content-Type', 'text/plain');
  res.setHeader('Content-Length', body.length);
  res.end(body);
});

app.post('/posturl', function(req, res){
  var body = "Post request recieved!"
  console.log("post aqcuired")
  
  user = req.param('user',null);
  /*
   * Do more stuff with the post request params
   */
  res.setHeader('Content-Type', 'text/plain');
  res.setHeader('Content-Length', body.length);
  res.end(body)
  
});

app.listen(3000)
console.log("Listening on port 3000")
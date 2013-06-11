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
  var data_limit = 10
  var body = "Post request recieved!"
  console.log("post aqcuired")
  
  user = req.param('user',null);
  console.log(user)
  data = []
  for (var i=0; i<data_limit; i++){
    data[i] = req.param('data'+i,null);
  }
  /*
   * Do more stuff with the post request params
   */
  res.setHeader('Content-Type', 'text/plain');
  res.setHeader('Content-Length', body.length);
  res.end(body)
  
});

app.listen(3000)
console.log("Listening on port 3000")
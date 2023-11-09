var express = require('express');
var fs = require('fs');
var bodyParser = require('body-parser');

var app = express();
app.use(bodyParser.json({limit: '500mb', extended: true}));
app.use(bodyParser.urlencoded({limit: '500mb', extended: true}));
var endpoint = '/writePDF';

app.post(endpoint, function(req, res) {

    try{
        console.log(req.body)
        console.log(req.headers.Name)
        var dir = './DocsExtracted/';
        var namePDF = req.headers.Name;
    
        fs.writeFileSync(dir + namePDF, JSON.stringify(req.body));
        res.status(201).send('Saved to ' + dir + namePDF);
    }catch(error){
        console.log(error)
        res.status(500).send('Failed to store file' + namePDF);
    }

});

var port = 3000;
app.listen(port);
console.log("\nReady to write files on https://localhost:" + port + endpoint);
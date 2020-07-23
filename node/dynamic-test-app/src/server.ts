import * as express from 'express';
import * as bodyParser from 'body-parser';
import * as path from 'path';
import * as fs from 'fs';

const app = express.default();
app.use(bodyParser.json());
const port = 7272;

app.head('/api/get/json', (req, res) => {
    res.header('Content-Type', 'application/json');
    res.send();
});

app.get('/api/get/json', (req, res) => {
    res.header('Content-Type', 'application/json');
    res.send(JSON.stringify({ greeting: 'HELLO' }));
});

app.get('/api/get/text', (req, res) => {
    res.send('HELLO');
});

app.post('/api/post', (req, res) => {
    res.header('Content-Type', 'application/json');
    res.send(JSON.stringify({ name: req.body.name, id: 1 }));
});

app.put('/api/put', (req, res) => {
    res.header('Content-Type', 'application/json');
    res.send(JSON.stringify({ name: req.body.name, id: 3 }));
});

app.patch('/api/patch', (req, res) => {
    res.header('Content-Type', 'application/json');
    res.send(JSON.stringify({ name: req.body.name, id: 3 }));
});

app.delete('/api/delete', (req, res) => {
    res.send();
});

app.use(express.static(path.join(__dirname, '..')));
app.use(express.static(path.join(__dirname, '..', 'static')));

// Path debugging helper
app.get('*', (req, res) => {
    const fullPath = path.join(__dirname, req.path);
    const dir = fs.opendirSync(fullPath);
    let entity;
    const listing = [];
    while ((entity = dir.readSync()) !== null) {
        if (entity.isFile()) {
            listing.push({ type: 'f', name: entity.name });
        } else if (entity.isDirectory()) {
            listing.push({ type: 'd', name: entity.name });
        }
    }
    dir.closeSync();
    res.send(listing);
});

app.listen(port, () => console.log('Succesfully started server on http://localhost:7272'));

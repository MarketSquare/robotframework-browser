import * as express from 'express';
import * as path from 'path';

const app = express.default();
// eslint-disable-next-line
app.use(express.json());
const port = parseInt(process.argv[2]) || 7272;

app.set('etag', false);

// @ts-expect-error
app.get('/favicon.ico', (req, res) => res.status(204).send());
// @ts-expect-error
app.get('/dist/favicon.ico', (req, res) => res.status(204).send());

app.head('/api/get/json', (req, res) => {
    res.header('Content-Type', 'application/json');
    res.send();
});

app.get('/api/get/json', (req, res) => {
    res.header('Content-Type', 'application/json');
    res.send(JSON.stringify({ greeting: 'HELLO' }));
});

app.get('/api/get/json/big', (req, res) => {
    res.header('Content-Type', 'application/json');
    res.send(
        JSON.stringify({
            long1: '1 Mauris vitae orci magna. Pellentesque eu volutpat elit. '.repeat(10000),
            long2: '2 Mauris vitae orci magna. Pellentesque eu volutpat elit. '.repeat(10000),
            long3: '3 Mauris vitae orci magna. Pellentesque eu volutpat elit. '.repeat(10000),
            long4: '4 Mauris vitae orci magna. Pellentesque eu volutpat elit. '.repeat(10000),
            long5: '5 Mauris vitae orci magna. Pellentesque eu volutpat elit. '.repeat(10000),
            long6: '6 Mauris vitae orci magna. Pellentesque eu volutpat elit. '.repeat(10000),
            long7: '7 Mauris vitae orci magna. Pellentesque eu volutpat elit. '.repeat(10000),
            long8: '8 Mauris vitae orci magna. Pellentesque eu volutpat elit. '.repeat(10000),
            long9: '9 Mauris vitae orci magna. Pellentesque eu volutpat elit. '.repeat(10000),
            long10: '10 Mauris vitae orci magna. Pellentesque eu volutpat elit. '.repeat(10000),
            long11: '11 Mauris vitae orci magna. Pellentesque eu volutpat elit. '.repeat(10000),
            long12: '12 Mauris vitae orci magna. Pellentesque eu volutpat elit. '.repeat(10000),
            long13: '13 Mauris vitae orci magna. Pellentesque eu volutpat elit. '.repeat(10000),
            long14: '14 Mauris vitae orci magna. Pellentesque eu volutpat elit. '.repeat(10000),
            long15: '15 Mauris vitae orci magna. Pellentesque eu volutpat elit. '.repeat(10000),
            long16: '16 Mauris vitae orci magna. Pellentesque eu volutpat elit. '.repeat(10000),
            long17: '17 Mauris vitae orci magna. Pellentesque eu volutpat elit. '.repeat(10000),
            long18: '18 Mauris vitae orci magna. Pellentesque eu volutpat elit. '.repeat(10000),
            long19: '19 Mauris vitae orci magna. Pellentesque eu volutpat elit. '.repeat(10000),
            long20: '20 Mauris vitae orci magna. Pellentesque eu volutpat elit. '.repeat(10000),
        }),
    );
});

app.options('/api/options', (req, res) => {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.status(204);
    res.send();
});

app.get('/api/get/text', (req, res) => {
    res.send('HELLO');
});

app.get('/api/get/delay', (req, res) => {
    setTimeout(() => {
        res.header('Content-Type', 'application/json');
        res.send(JSON.stringify({ greeting: 'after some time I respond' }));
    }, 400);
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

app.get('/slowpage.html', (req, res) => {
    setTimeout(() => {
        res.send('<html lang="en"><head><title>Slow page</title></head><body>HELLO</body></html>');
    }, 11000);
});

app.get('/redirector.html', (req, res) => {
    setTimeout(() => {
        res.redirect('/redirector2.html');
    }, 700);
});

app.get('/redirector2.html', (req, res) => {
    setTimeout(() => {
        res.redirect('/postredirect.html');
    }, 700);
});

app.post('/posted.html', (req, res) => {
    setTimeout(() => {
        res.send('<html lang="en"><head><title>Posted</title></head><body>Posted HELLO!!</body></html>');
    }, 500);
});

app.get('/api/get/bad_binary', (req, res) => {
    const data = Buffer.from([123120349139516]);
    // res.contentType('image/jpeg');
    res.end(data, 'binary');
});

app.use(express.static(path.join(__dirname, '..')));
app.use(express.static(path.join(__dirname, '..', 'static')));

// Path debugging helper
/* app.get('*', (req, res) => {
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
*/

app.listen(port, () => console.log(`Successfully started server on http://localhost:${port}`));

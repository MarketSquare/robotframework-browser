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

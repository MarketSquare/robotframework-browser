import { Command } from 'commander';
import * as express from 'express';
import * as fs from 'fs';
import * as https from 'https';
import morgan from 'morgan';
import * as path from 'path';

const app = express.default();

app.use(
    morgan((tokens, req, res) =>
        JSON.stringify({
            ts: tokens.date(req, res, 'iso'),
            type: 'http',
            method: tokens.method(req, res),
            url: tokens.url(req, res),
            status: parseInt(tokens.status(req, res) ?? '0'),
            ms: parseFloat(tokens['response-time'](req, res) ?? '0'),
        }),
    ),
);
app.use(express.json());

// Inject telemetry.js into all HTML responses. Registered before any route
// handlers so it applies to inline HTML routes (e.g. /slowpage.html, /posted.html)
// that never call next() and would otherwise bypass a later-registered middleware.
app.use((req, res, next) => {
    const originalEnd = (res.end as any).bind(res);
    (res as any).end = function (...args: any[]) {
        // Normalise Node's overloaded res.end signatures:
        //   end(cb?)
        //   end(chunk, cb?)
        //   end(chunk, encoding, cb?)
        let chunk: any = undefined;
        let encoding: BufferEncoding | undefined = undefined;
        let callback: (() => void) | undefined = undefined;

        if (args.length >= 1 && typeof args[0] !== 'function') {
            chunk = args[0];
        } else if (args.length >= 1 && typeof args[0] === 'function') {
            callback = args[0];
        }
        if (args.length >= 2) {
            if (typeof args[1] === 'function') {
                callback = args[1];
            } else {
                encoding = args[1];
            }
        }
        if (args.length >= 3 && typeof args[2] === 'function') {
            callback = args[2];
        }

        const ct = (res.getHeader('Content-Type') as string) ?? '';
        if (ct.includes('text/html') && chunk) {
            const body = Buffer.isBuffer(chunk) ? chunk.toString('utf8') : String(chunk);
            if (body.includes('</body>') && !body.includes('/telemetry.js')) {
                const injected = body.replace('</body>', '<script src="/telemetry.js"></script></body>');
                return originalEnd(injected, encoding, callback);
            }
        }
        return originalEnd(chunk, encoding, callback);
    };
    next();
});

let rfContext: { suite_id: string; test_id: string; kw_name: string; ts: string } = {
    suite_id: '',
    test_id: '',
    kw_name: '',
    ts: '',
};

app.post('/rf-context', (req, res) => {
    rfContext = { ...req.body, ts: new Date().toISOString() };
    res.sendStatus(204);
});

app.get('/rf-context', (req, res) => res.json(rfContext));

app.post('/browser-events', (req, res) => {
    process.stdout.write(JSON.stringify({ type: 'browser', ...req.body }) + '\n');
    res.sendStatus(204);
});

const program = new Command();
program
    .option('-p, --port <number>', 'port number', '7272')
    .option('-T, --tls', 'enables TLS (HTTPS)', false)
    .option('-c, --certificate <path>', 'path to server certificate in PEM format')
    .option('-k, --private-key <path>', 'path to private key in PEM format')
    .option('-P, --passphrase <passphrase>', 'passphrase for the private key')
    .option('-C, --certificate-authority <path>', 'path to CA certificate in PEM format')
    .option('-M, --mutual-tls', 'mutual TLS authentication with a client certificate (implies TLS)', false);

program.parse(process.argv);
const options = program.opts();

const port = parseInt(options.port);
const tls: boolean = options.tls;
const certificate = options.certificate;
const privateKey = options.privateKey;
const passphrase = options.passphrase;
const certificateAuthority = options.certificateAuthority;
const mutualTls: boolean = options.mutualTls;

app.set('etag', false);

app.get('/favicon.ico', (req, res) => res.status(204).send());
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

// Prefer self-contained dist roots when present, but keep source tree fallbacks
// for local development where server.ts is executed before bundling.
const staticRoots = [
    path.join(__dirname, 'static'),
    __dirname,
    path.join(__dirname, '..', 'static'),
    path.join(__dirname, '..'),
];

// Serve static HTML files with telemetry injection. express.static streams files,
// so res.end interception does not always have the full HTML body to patch.
app.use((req, res, next) => {
    if (req.method !== 'GET' && req.method !== 'HEAD') {
        return next();
    }
    if (req.path.startsWith('/api/') || req.path === '/rf-context' || req.path === '/browser-events') {
        return next();
    }
    if (req.path === '/telemetry.js') {
        return next();
    }

    const relPath = req.path === '/' ? 'index.html' : req.path.replace(/^\//, '');
    const candidatePaths = [relPath];
    if (relPath.endsWith('/')) {
        candidatePaths.push(relPath + 'index.html');
    } else if (!path.extname(relPath)) {
        candidatePaths.push(path.join(relPath, 'index.html'));
    }

    for (const root of staticRoots) {
        const resolvedRoot = path.resolve(root);
        for (const relCandidate of candidatePaths) {
            const candidate = path.resolve(root, relCandidate);
            if (!candidate.startsWith(resolvedRoot + path.sep) && candidate !== resolvedRoot) {
                continue;
            }
            try {
                const stat = fs.statSync(candidate);
                if (!stat.isFile()) {
                    continue;
                }
                if (path.extname(candidate).toLowerCase() !== '.html') {
                    continue;
                }
                let html = fs.readFileSync(candidate, 'utf8');
                if (!html.includes('/telemetry.js')) {
                    if (html.includes('</body>')) {
                        html = html.replace('</body>', '<script src="/telemetry.js"></script></body>');
                    } else {
                        html += '\n<script src="/telemetry.js"></script>\n';
                    }
                }
                res.type('html');
                return res.send(html);
            } catch {
                continue;
            }
        }
    }

    return next();
});

for (const root of staticRoots) {
    app.use(express.static(root));
}

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

if (tls || mutualTls) {
    const serverOptions = {
        cert: certificate ? fs.readFileSync(path.join(__dirname, certificate)) : undefined,
        key: privateKey ? fs.readFileSync(path.join(__dirname, privateKey)) : undefined,
        passphrase: passphrase ?? undefined,
        ca: certificateAuthority ? fs.readFileSync(path.join(__dirname, certificateAuthority)) : undefined,
        requestCert: mutualTls,
        rejectUnauthorized: mutualTls,
    };

    https.createServer(serverOptions, app).listen(port, () =>
        console.log(
            JSON.stringify({
                ts: new Date().toISOString(),
                type: 'server',
                event: 'start',
                url: `https://localhost:${port}`,
            }),
        ),
    );
} else {
    app.listen(port, () =>
        console.log(
            JSON.stringify({
                ts: new Date().toISOString(),
                type: 'server',
                event: 'start',
                url: `http://localhost:${port}`,
            }),
        ),
    );
}

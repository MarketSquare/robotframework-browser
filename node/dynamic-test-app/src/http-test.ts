import busboy from 'busboy';
import { createHash } from 'crypto';
import type { Express, NextFunction, Request, Response } from 'express';
import * as fs from 'fs';
import type { IncomingHttpHeaders } from 'http';
import * as path from 'path';
import * as zlib from 'zlib';

type LogJson = (entry: Record<string, unknown>) => void;

const MAX_BODY_BYTES = 50 * 1024 * 1024;
const FIXTURE_NAME = /^[A-Za-z0-9][A-Za-z0-9._-]*$/;

interface BodyView {
    size: number;
    sha256: string;
    contentType: string | null;
    text: string;
    json: unknown;
    base64: string;
}

interface Part {
    name: string;
    filename: string | null;
    mimeType: string;
    size: number;
    sha256: string;
    text: string | null;
    truncated: boolean;
}

interface Echo {
    method: string;
    url: string;
    path: string;
    query: Record<string, string | string[]>;
    headers: IncomingHttpHeaders;
    origin: string | null;
    body: BodyView;
    parts: Part[] | null;
    partsError?: string;
}

const sha256 = (data: Buffer) => createHash('sha256').update(data).digest('hex');

function readRawBody(req: Request): Promise<Buffer> {
    return new Promise((resolve, reject) => {
        const chunks: Buffer[] = [];
        let size = 0;
        req.on('data', (chunk: Buffer) => {
            size += chunk.length;
            if (size > MAX_BODY_BYTES) {
                reject(new Error(`Request body larger than ${MAX_BODY_BYTES} bytes`));
                req.destroy();
                return;
            }
            chunks.push(chunk);
        });
        req.on('end', () => resolve(Buffer.concat(chunks)));
        req.on('error', reject);
    });
}

function parseJson(text: string): unknown {
    if (text.trim() === '') {
        return null;
    }
    try {
        return JSON.parse(text);
    } catch {
        return null;
    }
}

function bodyView(raw: Buffer, contentType: string | undefined): BodyView {
    const text = raw.toString('utf8');
    return {
        size: raw.length,
        sha256: sha256(raw),
        contentType: contentType ?? null,
        text,
        json: parseJson(text),
        base64: raw.toString('base64'),
    };
}

function parseMultipart(raw: Buffer, headers: IncomingHttpHeaders): Promise<Part[]> {
    return new Promise((resolve, reject) => {
        // A slot per part in arrival order; a file's slot is filled when its stream ends.
        const parts: Part[] = [];
        const parser = busboy({
            headers,
            defParamCharset: 'utf8',
            limits: { fileSize: MAX_BODY_BYTES, fieldSize: MAX_BODY_BYTES },
        });
        parser.on('field', (name, value, info) => {
            const data = Buffer.from(value, 'utf8');
            parts.push({
                name,
                filename: null,
                mimeType: info.mimeType,
                size: data.length,
                sha256: sha256(data),
                text: value,
                truncated: info.valueTruncated,
            });
        });
        parser.on('file', (name, stream, info) => {
            const index = parts.length;
            parts.push({
                name,
                filename: info.filename ?? null,
                mimeType: info.mimeType,
                size: 0,
                sha256: '',
                text: null,
                truncated: false,
            });
            const chunks: Buffer[] = [];
            // Busboy reports a cut-off file part on the file stream, not on the parser.
            stream.on('error', reject);
            stream.on('data', (chunk: Buffer) => chunks.push(chunk));
            stream.on('end', () => {
                const data = Buffer.concat(chunks);
                parts[index] = {
                    ...parts[index],
                    size: data.length,
                    sha256: sha256(data),
                    truncated: stream.truncated === true,
                };
            });
        });
        parser.on('close', () => resolve(parts));
        parser.on('error', reject);
        parser.end(raw);
    });
}

function queryObject(req: Request): Record<string, string | string[]> {
    const params = new URL(req.originalUrl, 'http://test-app').searchParams;
    // Object.fromEntries defines own properties, so a key such as `__proto__` is kept.
    return Object.fromEntries(
        [...new Set(params.keys())].map((key) => {
            const values = params.getAll(key);
            return [key, values.length === 1 ? values[0] : values];
        }),
    );
}

function queryValues(req: Request, name: string): string[] {
    return new URL(req.originalUrl, 'http://test-app').searchParams.getAll(name);
}

function queryValue(req: Request, name: string): string | undefined {
    return queryValues(req, name)[0];
}

async function buildEcho(req: Request): Promise<Echo> {
    const raw = await readRawBody(req);
    const contentType = req.get('content-type');
    const isMultipart = (contentType ?? '').toLowerCase().startsWith('multipart/form-data');
    const echo: Echo = {
        method: req.method,
        url: req.originalUrl,
        path: new URL(req.originalUrl, 'http://test-app').pathname,
        query: queryObject(req),
        headers: req.headers,
        origin: req.get('origin') ?? null,
        body: bodyView(raw, contentType),
        parts: null,
    };
    if (isMultipart) {
        try {
            echo.parts = await parseMultipart(raw, req.headers);
        } catch (error) {
            echo.partsError = error instanceof Error ? error.message : String(error);
        }
    }
    return echo;
}

const escapeHtml = (text: string) => text.replace(/[&<>"']/g, (c) => `&#${c.charCodeAt(0)};`);

function echoContent(req: Request, res: Response, payload: Record<string, unknown>, contentType = 'json') {
    const json = JSON.stringify({ ...payload, served: res.locals.served }, null, 2);
    if (queryValue(req, 'format') === 'html') {
        return {
            type: 'html',
            data:
                '<html lang="en"><head><title>Echo</title></head>' +
                `<body><pre id="echo">${escapeHtml(json)}</pre></body></html>`,
        };
    }
    return { type: contentType, data: json };
}

function sendEcho(req: Request, res: Response, payload: Record<string, unknown>, contentType = 'json') {
    const { type, data } = echoContent(req, res, payload, contentType);
    res.type(type).send(data);
}

const ENCODERS: Record<string, (data: string | Buffer) => Buffer> = {
    gzip: zlib.gzipSync,
    br: zlib.brotliCompressSync,
};

type CorsOutcome = 'off' | 'none' | 'allowed' | 'preflight';

const SERVED_HEADER = 'X-Test-App-Served';

interface JournalEntry {
    id: number;
    method: string;
    path: string;
    url: string;
    status: number;
    headers: IncomingHttpHeaders;
}

function applyCors(req: Request, res: Response, exposeHeaders: string[]): CorsOutcome {
    if (queryValue(req, 'cors') === 'off') {
        return 'off';
    }
    const origin = req.get('origin');
    if (!origin) {
        return 'none';
    }
    res.set('Access-Control-Allow-Origin', origin);
    res.set('Access-Control-Allow-Credentials', 'true');
    res.append('Vary', 'Origin');
    // With credentials, `*` is not a wildcard, so the custom names are listed as well.
    res.set('Access-Control-Expose-Headers', ['*', SERVED_HEADER, ...exposeHeaders].join(', '));
    return 'allowed';
}

function isPreflight(req: Request): boolean {
    return req.method === 'OPTIONS' && req.get('access-control-request-method') !== undefined;
}

function answerPreflight(req: Request, res: Response, log: LogJson, endpoint: string) {
    const cors = applyCors(req, res, []);
    if (cors === 'allowed') {
        res.set('Access-Control-Allow-Methods', req.get('access-control-request-method') ?? '');
        const requested = req.get('access-control-request-headers');
        if (requested) {
            res.set('Access-Control-Allow-Headers', requested);
        }
        res.set('Access-Control-Max-Age', '0');
    }
    log({
        event: 'http_echo',
        endpoint,
        method: req.method,
        url: req.originalUrl,
        cors: cors === 'allowed' ? 'preflight' : cors,
    });
    res.status(204).send();
}

function logExchange(log: LogJson, endpoint: string, echo: Echo, status: number, cors: CorsOutcome, extra = {}) {
    log({
        event: 'http_echo',
        endpoint,
        method: echo.method,
        url: echo.url,
        status,
        bodySize: echo.body.size,
        bodySha256: echo.body.sha256,
        parts: echo.parts?.map((part) => part.name) ?? null,
        cors,
        ...extra,
    });
}

const wait = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

const HEADER_NAME = /^[!#$%&'*+.^_`|~0-9A-Za-z-]+$/;
const HEADER_TEXT = /^[\t\x20-\x7e\x80-\xff]*$/;

interface RespondSpec {
    status: number;
    statusText: string | undefined;
    contentType: string | undefined;
    headers: [string, string][];
    body: string | undefined;
    file: string | undefined;
    delay: number;
    encoding: string | undefined;
}

function parseInteger(value: string | undefined, fallback: number): number {
    if (value === undefined) {
        return fallback;
    }
    return /^\d+$/.test(value) ? Number(value) : NaN;
}

/** Reads the `/api/respond` query; returns an error message naming the first bad parameter. */
function parseRespondSpec(req: Request): RespondSpec | string {
    const status = parseInteger(queryValue(req, 'status'), 200);
    if (!(status >= 200 && status <= 599)) {
        return `Invalid status: ${queryValue(req, 'status')} (an integer from 200 to 599)`;
    }
    const delay = parseInteger(queryValue(req, 'delay'), 0);
    if (Number.isNaN(delay)) {
        return `Invalid delay: ${queryValue(req, 'delay')} (milliseconds as a non-negative integer)`;
    }
    const statusText = queryValue(req, 'statusText');
    if (statusText !== undefined && !HEADER_TEXT.test(statusText)) {
        return `Invalid statusText: ${statusText} (Latin-1 text without line breaks)`;
    }
    const encoding = queryValue(req, 'encoding');
    if (encoding !== undefined && !(encoding in ENCODERS)) {
        return `Invalid encoding: ${encoding} (gzip or br)`;
    }
    const headers: [string, string][] = [];
    for (const header of queryValues(req, 'header')) {
        const colon = header.indexOf(':');
        const name = header.slice(0, colon).trim();
        const value = header.slice(colon + 1).trim();
        if (colon <= 0 || !HEADER_NAME.test(name) || !HEADER_TEXT.test(value)) {
            return `Invalid header: ${header} (Name:Value with a valid header name and Latin-1 value)`;
        }
        headers.push([name, value]);
    }
    return {
        status,
        statusText,
        contentType: queryValue(req, 'contentType'),
        headers,
        body: queryValue(req, 'body'),
        file: queryValue(req, 'file'),
        delay,
        encoding,
    };
}

function decodeBasicAuth(header: string | undefined): { user: string; password: string } | null {
    const match = /^Basic\s+(.+)$/i.exec(header ?? '');
    if (!match) {
        return null;
    }
    const decoded = Buffer.from(match[1], 'base64').toString('utf8');
    const colon = decoded.indexOf(':');
    if (colon < 0) {
        return null;
    }
    return { user: decoded.slice(0, colon), password: decoded.slice(colon + 1) };
}

const asyncRoute =
    (handler: (req: Request, res: Response) => Promise<void>) => (req: Request, res: Response, next: NextFunction) => {
        handler(req, res).catch(next);
    };

/**
 * Generic endpoints for the HTTP test page (static/http.html).
 * Registered before any body parser, because they read every request body raw.
 */
export function registerHttpTestRoutes(app: Express, log: LogJson, fixturesDir: string) {
    let servedCount = 0;
    const journal: JournalEntry[] = [];

    app.get('/api/journal', (req, res) => {
        const prefix = queryValue(req, 'path') ?? '';
        res.set('Access-Control-Allow-Origin', '*');
        res.json(journal.filter((entry) => entry.path.startsWith(prefix)));
    });

    app.use(['/api/echo', '/api/respond', '/api/basic-auth'], (req, res, next) => {
        const id = ++servedCount;
        res.locals.served = id;
        res.set(SERVED_HEADER, String(id));
        res.on('finish', () =>
            journal.push({
                id,
                method: req.method,
                path: new URL(req.originalUrl, 'http://test-app').pathname,
                url: req.originalUrl,
                status: res.statusCode,
                headers: req.headers,
            }),
        );
        next();
    });

    app.use(
        '/api/echo',
        asyncRoute(async (req, res) => {
            if (isPreflight(req)) {
                return answerPreflight(req, res, log, 'echo');
            }
            const echo = await buildEcho(req);
            const cors = applyCors(req, res, []);
            logExchange(log, 'echo', echo, 200, cors);
            sendEcho(req, res, { ...echo });
        }),
    );

    app.use(
        '/api/respond',
        asyncRoute(async (req, res) => {
            if (isPreflight(req)) {
                return answerPreflight(req, res, log, 'respond');
            }
            const echo = await buildEcho(req);
            const spec = parseRespondSpec(req);
            if (typeof spec === 'string') {
                const cors = applyCors(req, res, []);
                logExchange(log, 'respond', echo, 400, cors, { error: spec });
                res.status(400)
                    .type('json')
                    .send(JSON.stringify({ error: spec }));
                return;
            }
            const { status, statusText, contentType, headers, body, file, delay, encoding } = spec;
            const cors = applyCors(
                req,
                res,
                headers.map(([name]) => name),
            );

            let fileData: Buffer | null = null;
            if (file !== undefined) {
                const filePath = path.join(fixturesDir, file);
                if (!FIXTURE_NAME.test(file) || !fs.existsSync(filePath)) {
                    logExchange(log, 'respond', echo, 404, cors, { file });
                    res.status(404)
                        .type('json')
                        .send(JSON.stringify({ error: `Unknown fixture: ${file}` }));
                    return;
                }
                fileData = fs.readFileSync(filePath);
            }

            if (delay > 0) {
                await wait(delay);
            }
            res.status(status);
            if (statusText) {
                res.statusMessage = statusText;
            }
            for (const [name, value] of headers) {
                res.append(name, value);
            }
            logExchange(log, 'respond', echo, status, cors, { file: file ?? null });
            let content: { type: string; data: string | Buffer };
            if (fileData !== null) {
                content = { type: contentType ?? path.extname(file ?? ''), data: fileData };
            } else if (body !== undefined) {
                content = { type: contentType ?? 'text/plain', data: body };
            } else {
                content = echoContent(req, res, { ...echo }, contentType);
            }
            res.type(content.type);
            if (encoding !== undefined) {
                res.set('Content-Encoding', encoding);
                res.send(ENCODERS[encoding](content.data));
            } else {
                res.send(content.data);
            }
        }),
    );

    app.all(
        '/api/basic-auth/:user/:password',
        asyncRoute(async (req, res) => {
            if (isPreflight(req)) {
                return answerPreflight(req, res, log, 'basic-auth');
            }
            const echo = await buildEcho(req);
            const cors = applyCors(req, res, ['WWW-Authenticate']);
            const credentials = decodeBasicAuth(req.get('authorization'));
            const user = String(req.params.user);
            if (credentials?.user !== user || credentials.password !== String(req.params.password)) {
                logExchange(log, 'basic-auth', echo, 401, cors, { auth: credentials ? 'wrong' : 'missing' });
                res.status(401).set('WWW-Authenticate', 'Basic realm="test-app"');
                sendEcho(req, res, { authenticated: false });
                return;
            }
            logExchange(log, 'basic-auth', echo, 200, cors, { auth: 'ok' });
            sendEcho(req, res, { ...echo, authenticatedUser: user });
        }),
    );
}

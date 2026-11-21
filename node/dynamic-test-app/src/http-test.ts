import busboy from 'busboy';
import { createHash } from 'crypto';
import type { Express, NextFunction, Request, Response } from 'express';
import * as fs from 'fs';
import type { IncomingHttpHeaders } from 'http';
import * as path from 'path';

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
        const parts: Part[] = [];
        const parser = busboy({ headers, limits: { fileSize: MAX_BODY_BYTES } });
        parser.on('field', (name, value, info) => {
            const data = Buffer.from(value, 'utf8');
            parts.push({
                name,
                filename: null,
                mimeType: info.mimeType,
                size: data.length,
                sha256: sha256(data),
                text: value,
            });
        });
        parser.on('file', (name, stream, info) => {
            const chunks: Buffer[] = [];
            stream.on('data', (chunk: Buffer) => chunks.push(chunk));
            stream.on('end', () => {
                const data = Buffer.concat(chunks);
                parts.push({
                    name,
                    filename: info.filename ?? null,
                    mimeType: info.mimeType,
                    size: data.length,
                    sha256: sha256(data),
                    text: null,
                });
            });
        });
        parser.on('close', () => resolve(parts));
        parser.on('error', reject);
        parser.end(raw);
    });
}

function queryObject(req: Request): Record<string, string | string[]> {
    const params = new URL(req.originalUrl, 'http://test-app').searchParams;
    const query: Record<string, string | string[]> = {};
    for (const key of new Set(params.keys())) {
        const values = params.getAll(key);
        query[key] = values.length === 1 ? values[0] : values;
    }
    return query;
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
    return {
        method: req.method,
        url: req.originalUrl,
        path: new URL(req.originalUrl, 'http://test-app').pathname,
        query: queryObject(req),
        headers: req.headers,
        origin: req.get('origin') ?? null,
        body: bodyView(raw, contentType),
        parts: isMultipart ? await parseMultipart(raw, req.headers) : null,
    };
}

const escapeHtml = (text: string) => text.replace(/[&<>"']/g, (c) => `&#${c.charCodeAt(0)};`);

function sendEcho(req: Request, res: Response, payload: Record<string, unknown>, contentType = 'json') {
    const json = JSON.stringify(payload, null, 2);
    if (queryValue(req, 'format') === 'html') {
        res.type('html').send(
            '<html lang="en"><head><title>Echo</title></head>' +
                `<body><pre id="echo">${escapeHtml(json)}</pre></body></html>`,
        );
    } else {
        res.type(contentType).send(json);
    }
}

type CorsOutcome = 'off' | 'none' | 'allowed' | 'preflight';

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
    res.set('Access-Control-Expose-Headers', ['*', ...exposeHeaders].join(', '));
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

function parseHeaderParams(req: Request): [string, string][] {
    return queryValues(req, 'header').flatMap((value): [string, string][] => {
        const colon = value.indexOf(':');
        if (colon <= 0) {
            return [];
        }
        return [[value.slice(0, colon).trim(), value.slice(colon + 1).trim()]];
    });
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
            const headers = parseHeaderParams(req);
            const cors = applyCors(
                req,
                res,
                headers.map(([name]) => name),
            );
            const status = parseInt(queryValue(req, 'status') ?? '200', 10);
            const statusText = queryValue(req, 'statusText');
            const contentType = queryValue(req, 'contentType');
            const body = queryValue(req, 'body');
            const file = queryValue(req, 'file');
            const delay = parseInt(queryValue(req, 'delay') ?? '0', 10);

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
            if (fileData !== null) {
                res.type(contentType ?? path.extname(file ?? '')).send(fileData);
            } else if (body !== undefined) {
                res.type(contentType ?? 'text/plain').send(body);
            } else {
                sendEcho(req, res, { ...echo }, contentType);
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
            const cors = applyCors(req, res, []);
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

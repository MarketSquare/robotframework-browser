// Generic HTTP test page: builds a request, sends it from the frontend and shows
// what the frontend received. Plain script, no build step (ADR 0002).
(function () {
    'use strict';

    const $ = (id) => document.getElementById(id);
    let requestCount = 0;

    // ---------- SHA-256 (crypto.subtle is missing on plain-http non-localhost hosts) ----------
    const K = new Uint32Array([
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5, 0xd807aa98,
        0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174, 0xe49b69c1, 0xefbe4786,
        0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da, 0x983e5152, 0xa831c66d, 0xb00327c8,
        0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967, 0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
        0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85, 0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819,
        0xd6990624, 0xf40e3585, 0x106aa070, 0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a,
        0x5b9cca4f, 0x682e6ff3, 0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7,
        0xc67178f2,
    ]);

    function sha256Hex(bytes) {
        const bitLength = bytes.length * 8;
        const paddedLength = Math.ceil((bytes.length + 9) / 64) * 64;
        const data = new Uint8Array(paddedLength);
        data.set(bytes);
        data[bytes.length] = 0x80;
        const view = new DataView(data.buffer);
        view.setUint32(paddedLength - 8, Math.floor(bitLength / 0x100000000));
        view.setUint32(paddedLength - 4, bitLength >>> 0);
        const h = new Uint32Array([
            0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19,
        ]);
        const w = new Uint32Array(64);
        const rotr = (x, n) => (x >>> n) | (x << (32 - n));
        for (let offset = 0; offset < paddedLength; offset += 64) {
            for (let i = 0; i < 16; i++) w[i] = view.getUint32(offset + i * 4);
            for (let i = 16; i < 64; i++) {
                const s0 = rotr(w[i - 15], 7) ^ rotr(w[i - 15], 18) ^ (w[i - 15] >>> 3);
                const s1 = rotr(w[i - 2], 17) ^ rotr(w[i - 2], 19) ^ (w[i - 2] >>> 10);
                w[i] = (w[i - 16] + s0 + w[i - 7] + s1) >>> 0;
            }
            let [a, b, c, d, e, f, g, hh] = h;
            for (let i = 0; i < 64; i++) {
                const t1 = (hh + (rotr(e, 6) ^ rotr(e, 11) ^ rotr(e, 25)) + ((e & f) ^ (~e & g)) + K[i] + w[i]) >>> 0;
                const t2 = ((rotr(a, 2) ^ rotr(a, 13) ^ rotr(a, 22)) + ((a & b) ^ (a & c) ^ (b & c))) >>> 0;
                hh = g;
                g = f;
                f = e;
                e = (d + t1) >>> 0;
                d = c;
                c = b;
                b = a;
                a = (t1 + t2) >>> 0;
            }
            h[0] += a;
            h[1] += b;
            h[2] += c;
            h[3] += d;
            h[4] += e;
            h[5] += f;
            h[6] += g;
            h[7] += hh;
        }
        return Array.from(h, (x) => x.toString(16).padStart(8, '0')).join('');
    }

    // ---------- builder ----------
    function readBuilder() {
        return {
            kind: $('kind').value,
            method: $('method').value,
            url: $('url').value,
            headers: $('headers').value.trim() === '' ? {} : JSON.parse($('headers').value),
            bodyMode: $('body-mode').value,
            body: $('body').value,
            fixture: $('fixture').value,
            fileField: $('file-field').value || 'file',
            credentials: $('credentials').value,
            target: $('target').value,
        };
    }

    async function selectedFiles(config) {
        const files = Array.from($('file').files);
        if (config.fixture) {
            const response = await fetch('/http-fixtures/' + config.fixture);
            if (!response.ok) throw new Error('fixture ' + config.fixture + ' answered ' + response.status);
            const blob = await response.blob();
            files.push(new File([blob], config.fixture, { type: blob.type }));
        }
        return files;
    }

    function bodyFields(config) {
        if (config.body.trim() === '') return {};
        return JSON.parse(config.body);
    }

    function hasHeader(headers, name) {
        return Object.keys(headers).some((key) => key.toLowerCase() === name.toLowerCase());
    }

    async function requestBody(config) {
        const headers = { ...config.headers };
        switch (config.bodyMode) {
            case 'text':
                return { headers, body: config.body };
            case 'json':
                if (!hasHeader(headers, 'content-type')) headers['Content-Type'] = 'application/json';
                return { headers, body: config.body };
            case 'form-urlencoded':
                return { headers, body: new URLSearchParams(bodyFields(config)) };
            case 'multipart': {
                const form = new FormData();
                for (const [name, value] of Object.entries(bodyFields(config))) form.append(name, String(value));
                for (const file of await selectedFiles(config)) form.append(config.fileField, file, file.name);
                return { headers, body: form };
            }
            case 'raw-file': {
                const [file] = await selectedFiles(config);
                if (file && file.type && !hasHeader(headers, 'content-type')) headers['Content-Type'] = file.type;
                return { headers, body: file };
            }
            default:
                return { headers, body: undefined };
        }
    }

    // ---------- response panel ----------
    // Every send() gets a run number; only the latest run writes the panel, older ones only the history.
    let imageUrl = null;
    const isCurrent = (config) => config.run === requestCount;

    function resetPanel() {
        for (const id of ['status', 'status-text', 'response-url', 'response-size', 'response-sha256', 'error']) {
            $(id).textContent = '';
        }
        $('response-headers').textContent = '';
        $('response-body').textContent = '';
        $('response-image').hidden = true;
        $('response-image').removeAttribute('src');
        if (imageUrl) URL.revokeObjectURL(imageUrl);
        imageUrl = null;
    }

    function setState(state) {
        $('state').textContent = state;
    }

    function describeBody(bytes) {
        try {
            return new TextDecoder('utf-8', { fatal: true }).decode(bytes);
        } catch {
            return '[binary: ' + bytes.length + ' bytes]';
        }
    }

    function addHistory(config, outcome) {
        const item = document.createElement('li');
        item.dataset.run = String(config.run ?? '');
        item.dataset.kind = config.kind;
        item.dataset.method = config.method;
        item.dataset.url = config.url;
        item.dataset.status = outcome.status ?? '';
        item.dataset.sha256 = outcome.sha256 ?? '';
        item.textContent =
            config.kind + ' ' + config.method + ' ' + config.url + ' -> ' + (outcome.status ?? outcome.summary ?? '');
        $('history').appendChild(item);
    }

    function showResponse(config, response) {
        const sha256 = sha256Hex(response.bytes);
        addHistory(config, { status: response.status, sha256 });
        if (!isCurrent(config)) return;
        $('status').textContent = String(response.status);
        $('status-text').textContent = response.statusText;
        $('response-url').textContent = response.url;
        $('response-size').textContent = String(response.bytes.length);
        $('response-sha256').textContent = sha256;
        $('response-headers').textContent = JSON.stringify(response.headers, null, 2);
        $('response-body').textContent = describeBody(response.bytes);
        const contentType = response.headers['content-type'] || '';
        if (contentType.startsWith('image/')) {
            imageUrl = URL.createObjectURL(new Blob([response.bytes], { type: contentType }));
            $('response-image').src = imageUrl;
            $('response-image').hidden = false;
        }
        setState('done');
    }

    // For an <img> load or a form submit: no status, size or headers, only a body summary.
    function showResult(config, url, body, summary) {
        addHistory(config, { summary });
        if (!isCurrent(config)) return;
        $('response-url').textContent = url;
        $('response-body').textContent = body;
        setState('done');
    }

    function showError(config, message) {
        addHistory(config, { summary: 'error: ' + message });
        if (!isCurrent(config)) return;
        $('error').textContent = message;
        setState('error');
    }

    // ---------- senders ----------
    async function sendFetch(config) {
        const { headers, body } = await requestBody(config);
        const options = { method: config.method, headers, credentials: config.credentials };
        if (body !== undefined && config.method !== 'GET' && config.method !== 'HEAD') options.body = body;
        const response = await fetch(config.url, options);
        const responseHeaders = {};
        response.headers.forEach((value, name) => (responseHeaders[name] = value));
        showResponse(config, {
            status: response.status,
            statusText: response.statusText,
            url: response.url,
            headers: responseHeaders,
            bytes: new Uint8Array(await response.arrayBuffer()),
        });
    }

    function parseXhrHeaders(raw) {
        const headers = {};
        for (const line of raw.trim().split(/[\r\n]+/)) {
            const colon = line.indexOf(':');
            if (colon > 0) headers[line.slice(0, colon).trim().toLowerCase()] = line.slice(colon + 1).trim();
        }
        return headers;
    }

    async function sendXhr(config) {
        const { headers, body } = await requestBody(config);
        await new Promise((resolve, reject) => {
            const xhr = new XMLHttpRequest();
            xhr.open(config.method, config.url);
            xhr.responseType = 'arraybuffer';
            xhr.withCredentials = config.credentials === 'include';
            for (const [name, value] of Object.entries(headers)) xhr.setRequestHeader(name, value);
            xhr.onload = () => {
                showResponse(config, {
                    status: xhr.status,
                    statusText: xhr.statusText,
                    url: xhr.responseURL,
                    headers: parseXhrHeaders(xhr.getAllResponseHeaders()),
                    bytes: new Uint8Array(xhr.response || new ArrayBuffer(0)),
                });
                resolve();
            };
            xhr.onerror = () => reject(new Error('XMLHttpRequest network error'));
            xhr.onabort = () => reject(new Error('XMLHttpRequest aborted'));
            xhr.ontimeout = () => reject(new Error('XMLHttpRequest timed out'));
            xhr.send(config.method === 'GET' || config.method === 'HEAD' ? null : body);
        });
    }

    function sendImg(config) {
        return new Promise((resolve, reject) => {
            // Each load has its own element, so a later request cannot cancel this one.
            const image = new Image();
            image.alt = 'response image';
            image.onload = () => {
                if (isCurrent(config)) {
                    image.id = 'response-image';
                    $('response-image').replaceWith(image);
                }
                const size = image.naturalWidth + 'x' + image.naturalHeight;
                showResult(config, image.currentSrc, 'image ' + size, 'loaded ' + size);
                resolve();
            };
            image.onerror = () => reject(new Error('image failed to load'));
            image.src = config.url;
        });
    }

    // Navigations that never load leave no event behind; after this long the form submit counts as failed.
    const FORM_TIMEOUT_MS = 15000;

    // A form control named like a form property (submit, action, appendChild...) masks that property,
    // so the form is only touched through attributes and the prototypes' methods.
    function appendToForm(form, node) {
        Node.prototype.appendChild.call(form, node);
    }

    function addHiddenInput(form, name, value) {
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = name;
        input.value = String(value);
        appendToForm(form, input);
    }

    function submitForm(form) {
        HTMLFormElement.prototype.submit.call(form);
    }

    function removeForm(form) {
        Element.prototype.remove.call(form);
    }

    function readFormResult(frame, action) {
        let doc = null;
        try {
            doc = frame.contentDocument;
        } catch {
            doc = null;
        }
        if (doc && doc.location.origin === action.origin) {
            const echo = doc.getElementById('echo');
            return { text: echo ? echo.textContent : doc.body.textContent };
        }
        // A same-origin action whose result is unreadable or on another origin got the browser's error page.
        if (action.origin === location.origin) return { error: 'form submit failed' };
        return { text: '[cross-origin result]' };
    }

    async function sendForm(config) {
        const action = new URL(config.url, location.href);
        if (!action.searchParams.has('format')) action.searchParams.set('format', 'html');
        const form = document.createElement('form');
        const method = config.method === 'GET' ? 'GET' : 'POST';
        // A GET form replaces the action's query with its fields, so the query travels as fields.
        const formAction = method === 'GET' ? action.origin + action.pathname : action.href;
        form.setAttribute('method', method);
        form.setAttribute('target', config.target);
        form.setAttribute('action', formAction);
        form.setAttribute('hidden', '');
        if (method === 'GET') {
            for (const [name, value] of action.searchParams) addHiddenInput(form, name, value);
        }
        const fields = ['form-urlencoded', 'multipart', 'json'].includes(config.bodyMode) ? bodyFields(config) : {};
        for (const [name, value] of Object.entries(fields)) addHiddenInput(form, name, value);
        if (config.bodyMode === 'multipart') {
            form.setAttribute('enctype', 'multipart/form-data');
            const transfer = new DataTransfer();
            for (const file of await selectedFiles(config)) transfer.items.add(file);
            const input = document.createElement('input');
            input.type = 'file';
            input.name = config.fileField;
            input.multiple = true;
            input.files = transfer.files;
            appendToForm(form, input);
        }
        document.body.appendChild(form);
        if (config.target !== 'form-result') {
            submitForm(form);
            removeForm(form);
            return;
        }
        const frame = document.querySelector('iframe[name="form-result"]');
        try {
            await new Promise((resolve, reject) => {
                const onLoad = () => {
                    frame.onload = null;
                    clearTimeout(timer);
                    const result = readFormResult(frame, action);
                    if (result.error) {
                        reject(new Error(result.error));
                        return;
                    }
                    showResult(config, formAction, result.text, 'submitted');
                    resolve();
                };
                const timer = setTimeout(() => {
                    // A later submit into the same frame owns the handler by now.
                    if (frame.onload === onLoad) frame.onload = null;
                    reject(new Error('form submit got no response within ' + FORM_TIMEOUT_MS + ' ms'));
                }, FORM_TIMEOUT_MS);
                frame.onload = onLoad;
                submitForm(form);
            });
        } finally {
            removeForm(form);
        }
    }

    const SENDERS = { fetch: sendFetch, xhr: sendXhr, img: sendImg, form: sendForm };

    async function send() {
        requestCount += 1;
        $('request-count').textContent = String(requestCount);
        resetPanel();
        setState('pending');
        let config;
        try {
            config = readBuilder();
        } catch (error) {
            showError({ run: requestCount, kind: '', method: '', url: '' }, 'invalid builder input: ' + error.message);
            return;
        }
        config.run = requestCount;
        try {
            await SENDERS[config.kind](config);
        } catch (error) {
            showError(config, String(error && error.message ? error.message : error));
        }
    }

    // ---------- prefill from the page URL ----------
    const PREFILL = {
        kind: 'kind',
        method: 'method',
        url: 'url',
        headers: 'headers',
        bodyMode: 'body-mode',
        body: 'body',
        fixture: 'fixture',
        fileField: 'file-field',
        credentials: 'credentials',
        target: 'target',
    };

    // Returns an error message for a value a select does not offer, so a typo never sends silently.
    function prefill() {
        const params = new URLSearchParams(location.search);
        for (const [param, id] of Object.entries(PREFILL)) {
            if (!params.has(param)) continue;
            const value = params.get(param);
            $(id).value = value;
            if ($(id).value !== value) return 'unknown ' + param + ': ' + value;
        }
        return params.get('send') === '1' ? null : undefined;
    }

    $('send').addEventListener('click', () => void send());
    const prefillResult = prefill();
    if (typeof prefillResult === 'string') {
        $('error').textContent = prefillResult;
        setState('error');
    } else if (prefillResult === null) {
        void send();
    }
})();

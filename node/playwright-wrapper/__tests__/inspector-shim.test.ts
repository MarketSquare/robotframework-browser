/// <reference types="jest" />

import { describe, expect, it, jest } from '@jest/globals';

import { FORK_TARGET_ENV, inspectorStub, wrapFork, wrapModuleLoad } from '../inspector-shim';

const OOP_DOWNLOAD = '/snapshot/app/node_modules/playwright-core/lib/entry/oopBrowserDownload.js';

function inspectorNotAvailable(): NodeJS.ErrnoException {
    const error: NodeJS.ErrnoException = new Error('Inspector is not available');
    error.code = 'ERR_INSPECTOR_NOT_AVAILABLE';
    return error;
}

// Stands in for the NodeJS builds that @yao-pkg/pkg bundles into the
// BrowserBatteries grpc_server, which are compiled without inspector support.
function loadWithoutInspector(request: string): unknown {
    if (request.includes('inspector')) {
        throw inspectorNotAvailable();
    }
    return { module: request };
}

describe('inspector shim', () => {
    it('passes unrelated modules straight through', () => {
        const originalLoad = jest.fn(() => 'real module');
        const load = wrapModuleLoad(originalLoad);

        expect(load('fs', null, false)).toBe('real module');
        expect(originalLoad).toHaveBeenCalledTimes(1);
    });

    it('returns the real inspector when NodeJS provides one', () => {
        const realInspector = { url: () => 'ws://127.0.0.1:9229/abc' };
        const load = wrapModuleLoad(() => realInspector);

        expect(load('inspector', null, false)).toBe(realInspector);
    });

    it.each(['inspector', 'node:inspector', 'inspector/promises', 'node:inspector/promises'])(
        'substitutes the stub for %s when the builtin is unavailable',
        (request) => {
            const load = wrapModuleLoad(loadWithoutInspector);

            expect(load(request, null, false)).toBe(inspectorStub);
        },
    );

    it('leaves non-inspector modules working when the builtin is unavailable', () => {
        const load = wrapModuleLoad(loadWithoutInspector);

        expect(load('fs', null, false)).toEqual({ module: 'fs' });
    });

    it('propagates load errors that are not ERR_INSPECTOR_NOT_AVAILABLE', () => {
        const load = wrapModuleLoad(() => {
            throw new Error('boom');
        });

        expect(() => load('inspector', null, false)).toThrow('boom');
    });

    it('reports no attached debugger, which is what Playwright asks the stub', () => {
        expect(inspectorStub.url()).toBeUndefined();
    });

    it('fails loudly for inspector features that cannot be emulated', () => {
        expect(() => inspectorStub.open()).toThrow(/inspector is not available in this build/);
        expect(() => new inspectorStub.Session()).toThrow(/inspector is not available in this build/);
    });
});

describe('fork redirection', () => {
    const bootstrap = () => '/snapshot/app/Browser/wrapper/fork-bootstrap.js';

    it("runs the bootstrap instead, handing over Playwright's script", () => {
        const originalFork = jest.fn();
        wrapFork(originalFork, bootstrap)(OOP_DOWNLOAD);

        expect(originalFork).toHaveBeenCalledTimes(1);
        const [modulePath, args, options] = originalFork.mock.calls[0] as [
            string,
            string[],
            { env: NodeJS.ProcessEnv },
        ];
        expect(modulePath).toBe(bootstrap());
        expect(args).toEqual([]);
        expect(options.env[FORK_TARGET_ENV]).toBe(OOP_DOWNLOAD);
    });

    it('keeps the caller args and other options', () => {
        const originalFork = jest.fn();
        wrapFork(originalFork, bootstrap)(OOP_DOWNLOAD, ['run-driver'], { stdio: 'pipe', env: { FOO: 'bar' } });

        const [, args, options] = originalFork.mock.calls[0] as [string, string[], Record<string, unknown>];
        expect(args).toEqual(['run-driver']);
        expect(options.stdio).toBe('pipe');
        expect(options.env).toEqual({ FOO: 'bar', [FORK_TARGET_ENV]: OOP_DOWNLOAD });
    });

    it('supports fork(modulePath, options) without args', () => {
        const originalFork = jest.fn();
        wrapFork(originalFork, bootstrap)(OOP_DOWNLOAD, { stdio: 'inherit' });

        const [, args, options] = originalFork.mock.calls[0] as [string, string[], Record<string, unknown>];
        expect(args).toEqual([]);
        expect(options.stdio).toBe('inherit');
    });

    it('leaves forks of anything outside Playwright alone', () => {
        const originalFork = jest.fn();
        wrapFork(originalFork, bootstrap)('/snapshot/app/node_modules/some-dep/worker.js', ['a']);

        expect(originalFork).toHaveBeenCalledWith('/snapshot/app/node_modules/some-dep/worker.js', ['a']);
    });

    it('leaves forks alone when there is no bootstrap to run', () => {
        const originalFork = jest.fn();
        wrapFork(originalFork, () => undefined)(OOP_DOWNLOAD, ['a']);

        expect(originalFork).toHaveBeenCalledWith(OOP_DOWNLOAD, ['a']);
    });
});

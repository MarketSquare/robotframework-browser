// Copyright 2020-     Robot Framework Foundation
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

// The NodeJS binaries that @yao-pkg/pkg bundles into the BrowserBatteries
// grpc_server are built without inspector support, so `require('inspector')`
// throws ERR_INSPECTOR_NOT_AVAILABLE instead of returning a module. Playwright
// requires it unconditionally when its client `page` module is initialised
// (playwright-core/lib/coreBundle.js, from src/client/page.ts) and the whole
// process dies before the gRPC server is up.
//
// Playwright only calls `inspector.url()` from there, to detect whether a JS
// debugger is attached. Inside a pkg binary one never is, so answering
// `undefined` is the truthful answer rather than a workaround.
//
// This module is injected as the first thing in the bundle by
// node/build.wrapper.js so that the patch is in place before any `require` of
// Playwright. On a normal NodeJS installation the real module loads and the
// stub is never used.
//
// Patching require() only covers this process. Playwright downloads browser
// binaries out of process: it forks playwright-core/lib/entry/*.js, which pkg
// runs by re-executing grpc_server with that script as the entry, so none of
// our bundle is loaded there and the child dies the same way. Those forks are
// therefore redirected through fork-bootstrap.js, which installs the shim
// before requiring the script Playwright asked for.

// eslint-disable-next-line @typescript-eslint/no-require-imports
import childProcess = require('child_process');
// eslint-disable-next-line @typescript-eslint/no-require-imports
import fs = require('fs');
// eslint-disable-next-line @typescript-eslint/no-require-imports
import Module = require('module');
// eslint-disable-next-line @typescript-eslint/no-require-imports
import path = require('path');

export const FORK_TARGET_ENV = 'ROBOT_FRAMEWORK_BROWSER_FORK_TARGET';

// Only Playwright's own entry scripts need the shim; anything else a
// dependency forks is left alone.
const PLAYWRIGHT_ENTRY = /[\\/]playwright(-core)?[\\/]lib[\\/]/;

const INSPECTOR_MODULES = new Set(['inspector', 'node:inspector', 'inspector/promises', 'node:inspector/promises']);

function unavailable(method: string): () => never {
    return () => {
        throw new Error(
            `NodeJS inspector is not available in this build, cannot call inspector.${method}(). ` +
                'Use the Browser library without BrowserBatteries if you need the NodeJS inspector.',
        );
    };
}

export const inspectorStub = {
    // No debugger can be attached to an inspector-less binary.
    url: () => undefined,
    open: unavailable('open'),
    close: () => undefined,
    waitForDebugger: unavailable('waitForDebugger'),
    Session: class Session {
        constructor() {
            unavailable('Session')();
        }
    },
    console: {},
};

type ModuleLoad = (request: string, parent: unknown, isMain: boolean) => unknown;
interface ModuleWithLoad {
    _load: ModuleLoad;
}

/**
 * Wraps Module._load so that only a failing load of the inspector builtin is
 * answered with the stub. Everything else, including other load errors, is
 * passed through untouched.
 */
export function wrapModuleLoad(originalLoad: ModuleLoad): ModuleLoad {
    return function (this: unknown, request: string, ...rest: [unknown, boolean]): unknown {
        if (!INSPECTOR_MODULES.has(request)) {
            return originalLoad.call(this, request, ...rest);
        }
        try {
            return originalLoad.call(this, request, ...rest);
        } catch (error) {
            if ((error as NodeJS.ErrnoException)?.code !== 'ERR_INSPECTOR_NOT_AVAILABLE') {
                throw error;
            }
            return inspectorStub;
        }
    };
}

type Fork = (modulePath: string, ...rest: unknown[]) => unknown;
interface ForkOptions {
    env?: NodeJS.ProcessEnv;
}

/**
 * Wraps child_process.fork so that forks of a Playwright entry script run
 * fork-bootstrap.js instead, with the original target handed over in the
 * environment. `bootstrap` returns undefined when there is nothing to
 * bootstrap with, in which case the fork is left untouched.
 */
export function wrapFork(originalFork: Fork, bootstrap: () => string | undefined): Fork {
    return function (this: unknown, modulePath: string, ...rest: unknown[]): unknown {
        const bootstrapPath =
            typeof modulePath === 'string' && PLAYWRIGHT_ENTRY.test(modulePath) ? bootstrap() : undefined;
        if (!bootstrapPath) {
            return originalFork.call(this, modulePath, ...rest);
        }
        // fork(modulePath[, args][, options]) - args is optional.
        const args = Array.isArray(rest[0]) ? (rest[0] as string[]) : [];
        const options = (Array.isArray(rest[0]) ? rest[1] : rest[0]) as ForkOptions | undefined;
        return originalFork.call(this, bootstrapPath, args, {
            ...options,
            env: { ...(options?.env ?? process.env), [FORK_TARGET_ENV]: modulePath },
        });
    };
}

// Only redirect once the inspector is known to be missing, and only when the
// bootstrap was actually packaged next to us.
function forkBootstrap(): string | undefined {
    if (!inspectorIsStubbed()) {
        return undefined;
    }
    const bootstrapPath = path.join(__dirname, 'fork-bootstrap.js');
    return fs.existsSync(bootstrapPath) ? bootstrapPath : undefined;
}

let stubbed: boolean | undefined;
function inspectorIsStubbed(): boolean {
    if (stubbed === undefined) {
        try {
            // eslint-disable-next-line @typescript-eslint/no-require-imports
            stubbed = require('inspector') === inspectorStub;
        } catch {
            stubbed = true;
        }
    }
    return stubbed;
}

export function installInspectorShim(): void {
    const moduleWithLoad = Module as unknown as ModuleWithLoad;
    moduleWithLoad._load = wrapModuleLoad(moduleWithLoad._load);
    childProcess.fork = wrapFork(childProcess.fork as unknown as Fork, forkBootstrap) as typeof childProcess.fork;
}

installInspectorShim();

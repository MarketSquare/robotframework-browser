import * as path from 'path';
import type { Tracing } from 'playwright';
import { v4 as uuidv4 } from 'uuid';

export type TraceStartOptions = NonNullable<Parameters<Tracing['start']>[0]>;
export type TraceGroupLocation = NonNullable<NonNullable<Parameters<Tracing['group']>[1]>['location']>;

export const CONTEXT_TRACE_OPTIONS: TraceStartOptions = { screenshots: true, snapshots: true };

// A trace file is a zip path, or a directory that gets fileName; '{contextid}' becomes the context id.
function traceFilePath(traceFile: string, contextId: string, fileName: string): string {
    const file = traceFile.toLowerCase().endsWith('.zip') ? traceFile : path.join(traceFile, fileName);
    return file.replace('{contextid}', contextId);
}

export function contextTraceFile(traceFile: string, contextId: string): string {
    return traceFilePath(traceFile, contextId, `trace_${contextId}.zip`);
}

export function adHocTraceFile(traceFile: string, contextId: string): string {
    return traceFilePath(traceFile, contextId, `trace_${contextId}-${uuidv4()}.zip`);
}

export function isTargetClosed(error: unknown): boolean {
    return error instanceof Error && error.name === 'TargetClosedError';
}

type RunningTrace = { file: string; options: TraceStartOptions };

export type TraceGroup = { name: string; location: TraceGroupLocation };

export class ContextTracer {
    private trace: RunningTrace | undefined;
    private openGroups = 0;

    constructor(
        private readonly contextId: string,
        private readonly tracing: Tracing,
    ) {}

    get running(): boolean {
        return this.trace !== undefined;
    }

    get file(): string {
        return this.trace?.file ?? '';
    }

    get options(): TraceStartOptions | undefined {
        return this.trace?.options;
    }

    async start(options: TraceStartOptions, file: string): Promise<void> {
        if (this.running) {
            throw new Error(`Tracing is already running on context ${this.contextId}, stop it before starting again`);
        }
        await this.tracing.start(options);
        this.trace = { file, options };
    }

    async stop(saveTo?: string): Promise<string> {
        const { file } = this.takeRunningTrace();
        const savedTo = saveTo || file;
        await this.tracing.stop({ path: savedTo });
        return savedTo;
    }

    async discard(): Promise<void> {
        this.takeRunningTrace();
        await this.tracing.stop();
    }

    async endWithContext(save: boolean): Promise<void> {
        if (!this.running) return;
        if (save) {
            await this.stop();
            return;
        }
        try {
            await this.discard();
        } catch (error) {
            if (!isTargetClosed(error)) throw error;
        }
    }

    // The groups open in the running trace are always the bottom of the stack it was given.
    async catchUp(stack: readonly TraceGroup[]): Promise<void> {
        while (this.running && this.openGroups < stack.length) {
            const { name, location } = stack[this.openGroups];
            await this.tracing.group(name, { location });
            this.openGroups++;
        }
    }

    async closeGroupsTo(depth: number): Promise<void> {
        while (this.running && this.openGroups > depth) {
            this.openGroups--;
            await this.tracing.groupEnd();
        }
    }

    private takeRunningTrace(): RunningTrace {
        if (!this.trace) throw new Error(`No trace is running on context ${this.contextId}`);
        const trace = this.trace;
        this.trace = undefined;
        this.openGroups = 0;
        return trace;
    }
}

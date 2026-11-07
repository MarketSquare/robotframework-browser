import { logger } from './browser_logger';
import type { ContextTracer, TraceGroup } from './context-tracer';

type OpenGroup = TraceGroup & { reached: boolean };

export class TraceGroups {
    private stack: OpenGroup[] = [];

    constructor(
        private readonly tracers: () => ContextTracer[],
        private readonly activeTracer: () => ContextTracer | undefined,
    ) {}

    async open(group: TraceGroup, depth: number): Promise<void> {
        await this.closeTo(depth);
        this.stack.push({ ...group, reached: false });
    }

    async closeTo(depth: number): Promise<void> {
        while (this.stack.length > depth) {
            const top = this.stack[this.stack.length - 1];
            const active = this.activeTracer();
            if (!top.reached && active) await this.target(active);
            this.stack.pop();
            for (const tracer of this.tracers()) {
                try {
                    await tracer.closeGroupsTo(this.stack.length);
                } catch (error) {
                    logger.info(`Could not close trace groups: ${String(error)}`);
                }
            }
        }
    }

    // While no trace runs, Python sends no groups, so what is left here is stale; Python sends
    // its open groups again after the first trace starts.
    async started(tracer: ContextTracer): Promise<void> {
        if (!tracer.running) return;
        const othersRunning = this.tracers().some((other) => other !== tracer && other.running);
        if (!othersRunning) this.stack = [];
        await this.target(tracer);
    }

    async target(tracer: ContextTracer): Promise<void> {
        if (!tracer.running) return;
        try {
            await tracer.catchUp(this.stack);
        } catch (error) {
            logger.info(`Could not send trace groups: ${String(error)}`);
            return;
        }
        for (const group of this.stack) group.reached = true;
    }
}

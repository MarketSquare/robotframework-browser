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

import * as pino from 'pino';

const logger = pino.default(pino.destination('./execution-times.log'));
logger.level = 'trace';

// Idea and async_timer method from https://github.com/norbornen/execution-time-decorator/
// eslint-disable-next-line @typescript-eslint/ban-types
export function class_async_timer(target: Function) {
    for (const propertyName of Object.keys(target.prototype)) {
        const descriptor = Object.getOwnPropertyDescriptor(target.prototype, propertyName);
        const isMethod = descriptor?.value instanceof Function;
        if (!isMethod || !descriptor) continue;

        const timered_method = async_timer(descriptor.value, propertyName, descriptor);
        Object.defineProperty(target.prototype, propertyName, timered_method);
    }
}

function toLogObject(
    functionName: string,
    t0: number,
    finished: number,
): { function: string; started: number; finished: number; executionTime: number } {
    return {
        function: functionName,
        started: t0,
        finished: finished,
        executionTime: (finished - t0) * 0.001,
    };
}

export function async_timer(
    target: any,
    propertyKey: string,
    propertyDescriptor: PropertyDescriptor,
): PropertyDescriptor {
    if (propertyDescriptor === undefined) {
        propertyDescriptor = Object.getOwnPropertyDescriptor(target, propertyKey)!;
    }
    const timername =
        (target instanceof Function ? `static ${target.name}` : target.constructor.name) + `::${propertyKey}`;
    const originalMethod = propertyDescriptor.value;
    propertyDescriptor.value = async function (...args: any[]) {
        const t0 = new Date().valueOf();
        try {
            const result = await originalMethod.apply(this, args);
            const finished = new Date().valueOf();
            logger.debug(toLogObject(timername, t0, finished));
            return result;
        } catch (err) {
            const finished = new Date().valueOf();
            logger.debug(toLogObject(timername, t0, finished));
            throw err;
        }
    };
    return propertyDescriptor;
}

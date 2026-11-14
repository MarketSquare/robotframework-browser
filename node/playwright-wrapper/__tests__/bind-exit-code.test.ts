/// <reference types="jest" />

import { describe, expect, it } from '@jest/globals';

import { bindErrorExitCode, PORT_TAKEN_EXIT_CODE } from '../bind-exit-code';

describe('bindErrorExitCode', () => {
    it('reports a taken port with its own exit code', () => {
        const error = new Error(
            'No address added out of total 1 resolved errors: [listen EADDRINUSE: address already in use 127.0.0.1:65048]',
        );
        expect(bindErrorExitCode(error)).toBe(PORT_TAKEN_EXIT_CODE);
    });

    it('reports any other bind failure with 1', () => {
        const error = new Error('No address added out of total 1 resolved errors: [listen EACCES: permission denied]');
        expect(bindErrorExitCode(error)).toBe(1);
    });
});

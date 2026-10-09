/// <reference types="jest" />

import { beforeEach, describe, expect, it } from '@jest/globals';
import { EventEmitter } from 'events';

jest.mock('../browser_logger', () => ({
    logger: { info: jest.fn(), error: jest.fn() },
}));

import { logger } from '../browser_logger';
import { handleAlert } from '../interaction';

const mockLogger = jest.mocked(logger);

function makeMockPage() {
    return new EventEmitter() as any;
}

function makeMockDialog(overrides: Record<string, any> = {}) {
    return {
        message: () => 'Are you sure?',
        accept: jest.fn().mockResolvedValue(undefined),
        dismiss: jest.fn().mockResolvedValue(undefined),
        ...overrides,
    } as any;
}

function makeRequest(alertAction: 'accept' | 'dismiss', promptInput = '') {
    return { alertAction, promptInput } as any;
}

async function fireDialog(page: any, dialog: any) {
    const handlers = page.listeners('dialog');
    for (const handler of handlers) {
        await handler(dialog);
    }
}

describe('handleAlert', () => {
    beforeEach(() => {
        jest.clearAllMocks();
    });

    it('accepts a dialog when called once', async () => {
        const page = makeMockPage();
        const dialog = makeMockDialog();

        await handleAlert(makeRequest('accept'), page);
        await fireDialog(page, dialog);

        expect(page.listenerCount('dialog')).toBe(1);
        expect(dialog.accept).toHaveBeenCalledTimes(1);
        expect(dialog.dismiss).not.toHaveBeenCalled();
    });

    it('passes the prompt input to accept', async () => {
        const page = makeMockPage();
        const dialog = makeMockDialog();

        await handleAlert(makeRequest('accept', 'Kalle'), page);
        await fireDialog(page, dialog);

        expect(dialog.accept).toHaveBeenCalledWith('Kalle');
    });

    it('keeps a single handler when called repeatedly on the same page', async () => {
        const page = makeMockPage();
        const dialog = makeMockDialog();

        await handleAlert(makeRequest('accept'), page);
        await handleAlert(makeRequest('accept'), page);
        await handleAlert(makeRequest('accept'), page);
        await fireDialog(page, dialog);

        expect(page.listenerCount('dialog')).toBe(1);
        expect(dialog.accept).toHaveBeenCalledTimes(1);
    });

    it('lets the latest call decide the action', async () => {
        const page = makeMockPage();
        const dialog = makeMockDialog();

        await handleAlert(makeRequest('accept'), page);
        await handleAlert(makeRequest('dismiss'), page);
        await fireDialog(page, dialog);

        expect(dialog.accept).not.toHaveBeenCalled();
        expect(dialog.dismiss).toHaveBeenCalledTimes(1);
    });

    it('handles every following dialog on the page', async () => {
        const page = makeMockPage();

        await handleAlert(makeRequest('accept'), page);
        const first = makeMockDialog();
        await fireDialog(page, first);
        const second = makeMockDialog();
        await fireDialog(page, second);

        expect(first.accept).toHaveBeenCalledTimes(1);
        expect(second.accept).toHaveBeenCalledTimes(1);
    });

    it('replaces the handler only on the page it was set for', async () => {
        const pageOne = makeMockPage();
        const pageTwo = makeMockPage();
        const dialogOne = makeMockDialog();
        const dialogTwo = makeMockDialog();

        await handleAlert(makeRequest('accept'), pageOne);
        await handleAlert(makeRequest('dismiss'), pageTwo);
        await fireDialog(pageOne, dialogOne);
        await fireDialog(pageTwo, dialogTwo);

        expect(pageOne.listenerCount('dialog')).toBe(1);
        expect(pageTwo.listenerCount('dialog')).toBe(1);
        expect(dialogOne.accept).toHaveBeenCalledTimes(1);
        expect(dialogTwo.dismiss).toHaveBeenCalledTimes(1);
    });

    it('does not report an error when the dialog was already handled', async () => {
        const page = makeMockPage();
        const dialog = makeMockDialog({
            accept: jest.fn().mockRejectedValue(new Error('Cannot accept dialog which is already handled!')),
        });

        await handleAlert(makeRequest('accept'), page);
        await expect(fireDialog(page, dialog)).resolves.toBeUndefined();

        expect(mockLogger.error).not.toHaveBeenCalled();
        expect(mockLogger.info).toHaveBeenCalledWith(expect.stringContaining('was handled by someone else already'));
    });

    it('reports an unexpected dialog failure instead of rejecting', async () => {
        const page = makeMockPage();
        const dialog = makeMockDialog({
            accept: jest.fn().mockRejectedValue(new Error('Target page has been closed')),
        });

        await handleAlert(makeRequest('accept'), page);
        await expect(fireDialog(page, dialog)).resolves.toBeUndefined();

        expect(mockLogger.error).toHaveBeenCalledWith(
            expect.objectContaining({ event_kind: 'internal_error', status: 'failed' }),
            expect.stringContaining('Failed to accept dialog "Are you sure?": Target page has been closed'),
        );
    });
});

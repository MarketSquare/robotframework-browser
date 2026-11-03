import { beforeEach, describe, expect, it } from '@jest/globals';

import { addCookie, deleteAllCookies, deleteCookies, getCookies, getCookiesForUrls } from '../cookie';
import { PlaywrightState } from '../playwright-state';

const contextMock = {
    addCookies: jest.fn<Promise<void>, [unknown[]]>(),
    clearCookies: jest.fn<Promise<void>, [unknown?]>(),
    cookies: jest.fn<Promise<{ name: string }[]>, [unknown]>(),
};

const stateWith = (context: unknown) => ({ getActiveContext: () => context }) as unknown as PlaywrightState;
const jsonRequest = (body: unknown) => ({ body: JSON.stringify(body) });

describe('cookie', () => {
    beforeEach(() => {
        jest.clearAllMocks();
        contextMock.cookies.mockResolvedValue([{ name: 'first' }, { name: 'second' }]);
    });

    it('reads all cookies of the active context', async () => {
        const response = await getCookies({}, stateWith(contextMock));

        expect(contextMock.cookies).toHaveBeenCalledWith(undefined);
        expect(response.log).toBe('first,second');
        expect(JSON.parse(response.json)).toEqual([{ name: 'first' }, { name: 'second' }]);
    });

    it('reads cookies for the requested urls', async () => {
        const urls = ['https://a.example', 'https://b.example'];

        const response = await getCookiesForUrls(jsonRequest(urls), stateWith(contextMock));

        expect(contextMock.cookies).toHaveBeenCalledWith(urls);
        expect(response.log).toBe('first,second');
        expect(JSON.parse(response.json)).toEqual([{ name: 'first' }, { name: 'second' }]);
    });

    it('clears every cookie of the active context', async () => {
        const response = await deleteAllCookies({}, stateWith(contextMock));

        expect(contextMock.clearCookies).toHaveBeenCalledWith();
        expect(response.log).toBe('All cookies deleted.');
    });

    it('clears only the cookies matching the filter', async () => {
        await deleteCookies(jsonRequest({ name: 'session', path: '/app' }), stateWith(contextMock));

        expect(contextMock.clearCookies).toHaveBeenCalledWith({ name: 'session', path: '/app' });
    });

    it('passes the partition key to Playwright', async () => {
        const cookie = { name: 'n', value: 'v', url: 'https://a.example', partitionKey: 'https://site.example' };

        await addCookie(jsonRequest(cookie), stateWith(contextMock));

        expect(contextMock.addCookies).toHaveBeenCalledWith([cookie]);
    });

    it.each([
        ['getCookies', () => getCookies({}, stateWith(undefined))],
        ['addCookie', () => addCookie(jsonRequest({ name: 'n', value: 'v' }), stateWith(undefined))],
        ['deleteAllCookies', () => deleteAllCookies({}, stateWith(undefined))],
        ['getCookiesForUrls', () => getCookiesForUrls(jsonRequest('https://a.example'), stateWith(undefined))],
        ['deleteCookies', () => deleteCookies(jsonRequest({ name: 'n' }), stateWith(undefined))],
    ])('%s fails without an open context', async (_name, call) => {
        expect.assertions(1);
        await expect(call()).rejects.toThrow('no open context.');
    });
});

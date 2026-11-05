import { beforeEach, describe, expect, it } from '@jest/globals';

import { addCookie, deleteAllCookies, getCookies } from '../cookie';
import { Request_Cookie, Request_CookieFilter } from '../generated/playwright';
import { PlaywrightState } from '../playwright-state';

const contextMock = {
    addCookies: jest.fn<Promise<void>, [unknown[]]>(),
    clearCookies: jest.fn<Promise<void>, [unknown?]>(),
    cookies: jest.fn<Promise<{ name: string }[]>, [unknown]>(),
};

const stateWith = (context: unknown) => ({ getActiveContext: () => context }) as unknown as PlaywrightState;

describe('cookie', () => {
    beforeEach(() => {
        jest.clearAllMocks();
        contextMock.cookies.mockResolvedValue([{ name: 'first' }, { name: 'second' }]);
    });

    it('reads all cookies of the active context when no urls are given', async () => {
        const response = await getCookies({ urls: [] }, stateWith(contextMock));

        expect(contextMock.cookies).toHaveBeenCalledWith([]);
        expect(response.log).toBe('first,second');
        expect(JSON.parse(response.json)).toEqual([{ name: 'first' }, { name: 'second' }]);
    });

    it('reads cookies for the requested urls', async () => {
        const urls = ['https://a.example', 'https://b.example'];

        await getCookies({ urls }, stateWith(contextMock));

        expect(contextMock.cookies).toHaveBeenCalledWith(urls);
    });

    it.each([
        ['every cookie when no field is set', {}, 'All cookies deleted.'],
        [
            'cookies matching the given fields',
            { name: 'session', path: '/app' },
            'Cookies matching {"name":"session","path":"/app"} deleted.',
        ],
        ['only nameless cookies for an empty name', { name: '' }, 'Cookies matching {"name":""} deleted.'],
    ])('clears %s', async (_case, filter, log) => {
        const request = Request_CookieFilter.fromPartial(filter);

        const response = await deleteAllCookies(request, stateWith(contextMock));

        expect(contextMock.clearCookies).toHaveBeenCalledWith(request);
        expect(response.log).toBe(log);
    });

    it('passes every given field to Playwright', async () => {
        const request = Request_Cookie.fromPartial({
            name: 'n',
            value: 'v',
            url: 'https://a.example',
            expires: 1822137695.5,
            httpOnly: true,
            secure: true,
            sameSite: 'Strict',
            partitionKey: 'https://site.example',
        });

        const response = await addCookie(request, stateWith(contextMock));

        expect(contextMock.addCookies).toHaveBeenCalledWith([
            {
                name: 'n',
                value: 'v',
                url: 'https://a.example',
                expires: 1822137695.5,
                httpOnly: true,
                secure: true,
                sameSite: 'Strict',
                partitionKey: 'https://site.example',
            },
        ]);
        expect(response.log).toBe('Cookie "n" added.');
    });

    it('passes an empty name and value through', async () => {
        await addCookie(
            Request_Cookie.fromPartial({ name: '', value: '', domain: 'a.example', path: '/' }),
            stateWith(contextMock),
        );

        expect(contextMock.addCookies).toHaveBeenCalledWith([{ name: '', value: '', domain: 'a.example', path: '/' }]);
    });

    it('rejects an unknown sameSite value', async () => {
        expect.assertions(2);
        const request = Request_Cookie.fromPartial({
            name: 'n',
            value: 'v',
            url: 'https://a.example',
            sameSite: 'Loose',
        });

        await expect(addCookie(request, stateWith(contextMock))).rejects.toThrow('Loose');
        expect(contextMock.addCookies).not.toHaveBeenCalled();
    });

    it.each([
        ['getCookies', () => getCookies({ urls: [] }, stateWith(undefined))],
        ['addCookie', () => addCookie(Request_Cookie.fromPartial({ name: 'n', value: 'v' }), stateWith(undefined))],
        ['deleteAllCookies', () => deleteAllCookies({}, stateWith(undefined))],
    ])('%s fails without an open context', async (_name, call) => {
        expect.assertions(1);
        await expect(call()).rejects.toThrow('no open context.');
    });
});

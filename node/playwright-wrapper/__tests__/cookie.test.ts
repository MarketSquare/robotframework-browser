import { addCookie, deleteCookies, getCookiesForUrls } from '../cookie';
import { PlaywrightState } from '../playwright-state';

const contextMock = {
    addCookies: jest.fn(),
    clearCookies: jest.fn(),
    cookies: jest.fn(),
};

const stateWith = (context: unknown) => ({ getActiveContext: () => context }) as unknown as PlaywrightState;
const jsonRequest = (body: unknown) => ({ body: JSON.stringify(body) });

describe('cookie', () => {
    beforeEach(() => jest.resetAllMocks());

    it('reads cookies for the requested urls', async () => {
        const urls = ['https://a.example', 'https://b.example'];
        contextMock.cookies.mockResolvedValue([{ name: 'first' }, { name: 'second' }]);

        const response = await getCookiesForUrls(jsonRequest(urls), stateWith(contextMock));

        expect(contextMock.cookies).toHaveBeenCalledWith(urls);
        expect(response.log).toBe('first,second');
        expect(JSON.parse(response.json)).toEqual([{ name: 'first' }, { name: 'second' }]);
    });

    it('clears only the cookies matching the filter', async () => {
        await deleteCookies(jsonRequest({ name: 'session', path: '/app' }), stateWith(contextMock));

        expect(contextMock.clearCookies).toHaveBeenCalledWith({ name: 'session', path: '/app' });
    });

    it('passes the partition key to Playwright', async () => {
        const cookie = { name: 'n', value: 'v', url: 'https://a.example', partitionKey: 'https://site.example' };

        await addCookie(jsonRequest(cookie), contextMock as never);

        expect(contextMock.addCookies).toHaveBeenCalledWith([cookie]);
    });

    it.each([
        ['getCookiesForUrls', () => getCookiesForUrls(jsonRequest('https://a.example'), stateWith(undefined))],
        ['deleteCookies', () => deleteCookies(jsonRequest({ name: 'n' }), stateWith(undefined))],
    ])('%s fails without an open context', async (_name, call) => {
        await expect(call()).rejects.toThrow('no open context.');
    });
});

export function crash(page: { on: jest.Mock }): void {
    const call = page.on.mock.calls.find(([event]) => event === 'crash');
    if (!call) throw new Error('The page has no crash listener.');
    (call[1] as () => void)();
}

import { describe, expect, it } from '@jest/globals';

import { splitSelector, toPlaywrightSelector } from '../selector-syntax';

const ENTER = 'internal:control=enter-frame';
const ANY = 'internal:control=any-frame';

describe('splitSelector', () => {
    it.each([
        ['css=a', ['css=a'], []],
        ['a >> b', ['a ', ' b'], ['>>']],
        ['a >>> b', ['a ', ' b'], ['>>>']],
        ['a>>b>>>c', ['a', 'b', '>c'], ['>>', '>>']],
        ['a >> b\n>>>\nc', ['a ', ' b\n', '\nc'], ['>>', '>>>']],
        ['>>> b', ['', ' b'], ['>>>']],
        ['text="a >>> b"', ['text="a >>> b"'], []],
        ["text='a >> b' >> c", ["text='a >> b' ", ' c'], ['>>']],
        ['text=`a >>> b` >>> c', ['text=`a >>> b` ', ' c'], ['>>>']],
        ['css=[title="x >> y"] >> z', ['css=[title="x >> y"] ', ' z'], ['>>']],
        ['text="say \\"a >> b\\"" >> c', ['text="say \\"a >> b\\"" ', ' c'], ['>>']],
        ["text=it's >> c", ["text=it's ", ' c'], ['>>']],
        ['"quoted >>> text" >> c', ['"quoted >>> text" ', ' c'], ['>>']],
        ['id=a >>> id=b >>> id=c', ['id=a ', ' id=b ', ' id=c'], ['>>>', '>>>']],
    ])('splits %s outside quotes', (selector, clauses, separators) => {
        expect(splitSelector(selector)).toEqual({ clauses, separators });
    });
});

describe('toPlaywrightSelector', () => {
    describe('frames', () => {
        it('enters the frame a clause selects', () => {
            expect(toPlaywrightSelector('id=f >>> id=b', true)).toBe(`id=f >> ${ENTER} >> id=b`);
        });

        it('enters the first matching frame without strict mode', () => {
            expect(toPlaywrightSelector('id=f >>> id=b', false)).toBe(`id=f >> nth=0 >> ${ENTER} >> id=b`);
        });

        it('enters nested frames', () => {
            expect(toPlaywrightSelector('id=a >>> id=b >>> id=c', true)).toBe(
                `id=a >> ${ENTER} >> id=b >> ${ENTER} >> id=c`,
            );
        });

        it('keeps chains inside and around frames', () => {
            expect(toPlaywrightSelector('body >> id=f >>> div >> span', true)).toBe(
                `body >> id=f >> ${ENTER} >> div >> span`,
            );
        });

        it('reads >>> without whitespace around it as before: a chain, then a child combinator', () => {
            expect(toPlaywrightSelector('div>>>span', true)).toBe('div >> >span');
            expect(toPlaywrightSelector('div >>>span', true)).toBe('div >> >span');
            expect(toPlaywrightSelector('div>>> span', true)).toBe('div >> > span');
        });

        it.each(['id=f >>>', '>>>', '>>>   ', '>>> id=f >>> >>> span', 'id=f >>> >>> id=b'])(
            'names the selector when a part next to >>> is empty: %s',
            (selector) => {
                expect(() => toPlaywrightSelector(selector, true)).toThrow(
                    `Selector "${selector}" has an empty part next to ">>>".`,
                );
            },
        );

        it('searches every frame after a leading separator, in either mode', () => {
            expect(toPlaywrightSelector('>>> id=b', true)).toBe(`${ANY} >> id=b`);
            expect(toPlaywrightSelector('>>> id=b', false)).toBe(`${ANY} >> id=b`);
            expect(toPlaywrightSelector('  >>> id=b', true)).toBe(`${ANY} >> id=b`);
        });

        it('enters frames after a leading separator', () => {
            expect(toPlaywrightSelector('>>> id=f >>> id=b', true)).toBe(`${ANY} >> id=f >> ${ENTER} >> id=b`);
        });
    });

    describe('quotes', () => {
        it.each([
            'text="a >>> b"',
            "text='a >>> b'",
            'text=`a >>> b`',
            '"a >>> b"',
            'css=[title="x >>> y"]',
            'css=[title="label=x"]',
            'text="label=x"',
        ])('leaves %s as it is', (selector) => {
            expect(toPlaywrightSelector(selector, true)).toBe(selector);
        });

        it('translates only the separators outside quotes', () => {
            expect(toPlaywrightSelector('text="a >>> b" >>> id=c', true)).toBe(`text="a >>> b" >> ${ENTER} >> id=c`);
        });

        it('skips escaped quotes', () => {
            expect(toPlaywrightSelector('text="say \\" >>> no" >>> id=c', true)).toBe(
                `text="say \\" >>> no" >> ${ENTER} >> id=c`,
            );
        });

        it('reads an apostrophe in an unquoted text as text, as Playwright does', () => {
            expect(toPlaywrightSelector("text=it's here >>> id=c", true)).toBe(`text=it's here >> ${ENTER} >> id=c`);
        });
    });

    describe('label', () => {
        it.each([
            ['label=Email', 'internal:label="Email"i'],
            ['label=Email address', 'internal:label="Email address"i'],
            ['label="Email"i', 'internal:label="Email"i'],
            ['label="Email"s', 'internal:label="Email"s'],
            ["label='Email'", "internal:label='Email'"],
            ['label=/e-?mail/i', 'internal:label=/e-?mail/i'],
            ['label = Email', 'internal:label="Email"i'],
            ['*label=Email >> css=input', '*internal:label="Email"i >> css=input'],
            ['css=form >> label=Email', 'css=form >> internal:label="Email"i'],
            ["label=Customer's name >> nth=0", 'internal:label="Customer\'s name"i >> nth=0'],
            ['label=say "hi" >> nth=0', 'internal:label="say \\"hi\\""i >> nth=0'],
        ])('translates %s', (selector, expected) => {
            expect(toPlaywrightSelector(selector, true)).toBe(expected);
        });

        it('translates a label inside frames', () => {
            expect(toPlaywrightSelector('>>> id=f >>> label=Email', true)).toBe(
                `${ANY} >> id=f >> ${ENTER} >> internal:label="Email"i`,
            );
        });

        it.each(['labels=Email', 'xlabel=Email', 'css=label', 'label', 'text=label=x', 'internal:label=Email'])(
            'leaves %s alone',
            (selector) => {
                expect(toPlaywrightSelector(selector, true)).toBe(selector);
            },
        );
    });

    it('leaves selectors without Browser syntax unchanged', () => {
        expect(toPlaywrightSelector('css=div.a > span', true)).toBe('css=div.a > span');
        expect(toPlaywrightSelector('//div[@id="a"]', false)).toBe('//div[@id="a"]');
    });
});

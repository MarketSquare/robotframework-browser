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

// Playwright's selector generator drops a number at the start or the end of a
// text, taking it for a count that changes (`suitableTextAlternatives` in
// Playwright 1.65): a radio labelled "46 km/h bis 60 km/h" is recorded as
// `internal:text="km/h bis 60 km/h"i`. A person reads that as a mistake, so the
// recorder and the picker give the number back when the whole text still finds
// the same element and only it. The page under test supplies the texts (ADR
// 0010); Playwright checks every candidate before it is used.

import { Page } from 'playwright';

// Playwright keeps at most 80 characters of a text; a longer source was cut, not stripped.
const MAX_SOURCE_LENGTH = 200;
const TIMEOUT_MS = 500;
// The number Playwright strips, as its own patterns find it.
const LEADING_NUMBER = /^([\d.,]+)[^.,\w]/;
const TRAILING_NUMBER = /[^.,\w]([\d.,]+)$/;
const QUOTED = '"(?:[^"\\\\]|\\\\.)*"';
const TEXT_BODY = new RegExp(`^(internal:(?:text|label)=)(${QUOTED})([is]?)$`);
const ROLE_NAME = new RegExp(`^(internal:role=[a-z]+(?:\\[[^\\]]*\\])*?\\[name=)(${QUOTED})([is]?\\].*)$`);

interface NamedPart {
    // Rebuilds the part with another name.
    rebuild: (name: string) => string;
    name: string;
}

// Splits on Playwright's ` >> ` chain separator, never inside a quoted string.
export function splitChain(selector: string): string[] {
    const parts: string[] = [];
    let start = 0;
    let quoted = false;
    for (let i = 0; i < selector.length; i++) {
        const c = selector[i];
        if (quoted && c === '\\') i++;
        else if (c === '"') quoted = !quoted;
        else if (!quoted && selector.startsWith(' >> ', i)) {
            parts.push(selector.slice(start, i));
            start = i + 4;
            i += 3;
        }
    }
    parts.push(selector.slice(start));
    return parts;
}

function decodeAttribute(quoted: string): string {
    return quoted.slice(1, -1).replace(/\\(.)/g, '$1');
}

function encodeAttribute(value: string): string {
    return `"${value.replace(/\\/g, '\\\\').replace(/"/g, '\\"')}"`;
}

// The text or accessible name a part matches by, if it matches by one.
export function namedPart(part: string): NamedPart | undefined {
    const text = TEXT_BODY.exec(part);
    if (text) {
        const [, engine, quoted, flag] = text;
        return { name: JSON.parse(quoted) as string, rebuild: (name) => `${engine}${JSON.stringify(name)}${flag}` };
    }
    const role = ROLE_NAME.exec(part);
    if (role) {
        const [, head, quoted, tail] = role;
        return { name: decodeAttribute(quoted), rebuild: (name) => `${head}${encodeAttribute(name)}${tail}` };
    }
    return undefined;
}

const normalize = (text: string) => text.replace(/\s+/g, ' ').trim();

// `name` with the number Playwright dropped from `source`, in every spelling of
// the space between them that a match may need; none if it dropped none.
export function withNumber(name: string, source: string): string[] {
    const full = normalize(source);
    const wanted = normalize(name);
    if (!wanted || full === wanted) return [];
    // A space between number and text may be a no-break space, which an
    // accessible name keeps and a role name must then repeat.
    const joined = (rest: string, join: (separator: string) => string) =>
        /^\s|\s$/.test(rest) ? [join(' '), join(' ')] : [join('')];
    const leading = LEADING_NUMBER.exec(full);
    if (leading) {
        const rest = full.slice(leading[1].length);
        if (normalize(rest) === wanted) return joined(rest, (s) => `${leading[1]}${s}${name}`);
    }
    const trailing = TRAILING_NUMBER.exec(full);
    if (trailing) {
        const rest = full.slice(0, full.length - trailing[1].length);
        if (normalize(rest) === wanted) return joined(rest, (s) => `${name}${s}${trailing[1]}`);
    }
    return [];
}

// The texts an element may be found by: its content, labels and naming attributes.
function textsOf(element: Element): string[] {
    const texts: (string | null | undefined)[] = [element.textContent];
    const labels = (element as HTMLInputElement).labels;
    if (labels) labels.forEach((label) => texts.push(label.textContent));
    for (const attribute of ['aria-label', 'title', 'alt', 'placeholder']) texts.push(element.getAttribute(attribute));
    const labelledBy = (element.getAttribute('aria-labelledby') ?? '')
        .split(/\s+/)
        .map((id) => (id ? element.ownerDocument.getElementById(id)?.textContent : undefined));
    texts.push(...labelledBy, labelledBy.join(' '));
    return texts.filter((text): text is string => typeof text === 'string' && text.trim() !== '');
}

async function sourcesOf(page: Page, selector: string): Promise<string[]> {
    const locator = page.locator(selector);
    if ((await locator.count()) !== 1) return [];
    const texts: unknown = await locator.evaluate(textsOf, undefined, { timeout: TIMEOUT_MS });
    if (!Array.isArray(texts)) return [];
    return texts.filter((text): text is string => typeof text === 'string' && text.length <= MAX_SOURCE_LENGTH);
}

async function findsOnly(page: Page, candidate: string, original: string): Promise<boolean> {
    const locator = page.locator(candidate);
    return (await locator.count()) === 1 && (await locator.and(page.locator(original)).count()) === 1;
}

// `selector` with the numbers Playwright dropped given back, where the result
// finds the same element and only it; otherwise `selector` as it is. Never
// throws: a page that navigated or closed leaves the selector as Playwright made it.
export async function widenSelector(page: Page, selector: string): Promise<string> {
    const parts = splitChain(selector);
    if (!parts.some(namedPart) || typeof page?.locator !== 'function') return selector;
    let result = selector;
    try {
        for (let i = 0; i < parts.length; i++) {
            const part = namedPart(parts[i]);
            if (!part) continue;
            const sources = await sourcesOf(page, parts.slice(0, i + 1).join(' >> '));
            const candidates = [...new Set(sources.flatMap((source) => withNumber(part.name, source)))];
            for (const name of candidates) {
                const widened = [...parts.slice(0, i), part.rebuild(name), ...parts.slice(i + 1)];
                const candidate = widened.join(' >> ');
                if (await findsOnly(page, candidate, result)) {
                    parts[i] = widened[i];
                    result = candidate;
                    break;
                }
            }
        }
    } catch {
        // The page navigated, closed or rejected a selector: keep what is found so far.
    }
    return result;
}

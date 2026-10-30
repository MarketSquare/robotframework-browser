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

// Browser's selector syntax on top of Playwright's:
//  - `a >>> b` enters the frame `a` selects and searches `b` inside it;
//  - a leading `>>>` searches in every frame of the page (`page.frameLocator()`);
//  - `label=` finds an element by its label, as Playwright's `getByLabel`.
// Each becomes Playwright's internal form. A `>>>` or `label=` inside a quoted
// string is text, so the selector is split exactly where Playwright splits it
// (`parseSelectorString` in Playwright 1.64): at `>>` outside quotes.

const ENTER_FRAME = 'internal:control=enter-frame';
const ANY_FRAME = 'internal:control=any-frame';
const QUOTES = new Set(['"', "'", '`']);
// Playwright reads the quotes of an unquoted `text=` body as text.
const UNQUOTED_TEXT = /^\s*text\s*=(.+)$/;
const LABEL = /^(\s*\*?)label(\s*=)/;

export interface SplitSelector {
    // The clauses between the separators, as written.
    clauses: string[];
    // `separators[i]` follows `clauses[i]`: `>>` chains, `>>>` enters a frame.
    separators: ('>>' | '>>>')[];
}

export function splitSelector(selector: string): SplitSelector {
    const clauses: string[] = [];
    const separators: ('>>' | '>>>')[] = [];
    let index = 0;
    let start = 0;
    let quote: string | undefined;
    while (index < selector.length) {
        const c = selector[index];
        if (c === '\\' && index + 1 < selector.length) {
            index += 2;
        } else if (c === quote) {
            quote = undefined;
            index++;
        } else if (!quote && QUOTES.has(c) && !UNQUOTED_TEXT.test(selector.substring(start, index))) {
            quote = c;
            index++;
        } else if (!quote && c === '>' && selector[index + 1] === '>') {
            const frame = selector[index + 2] === '>';
            clauses.push(selector.substring(start, index));
            separators.push(frame ? '>>>' : '>>');
            index += frame ? 3 : 2;
            start = index;
        } else {
            index++;
        }
    }
    clauses.push(selector.substring(start));
    return { clauses, separators };
}

function translateClause(clause: string): string {
    return clause.replace(LABEL, '$1internal:label$2');
}

// The selector as Playwright reads it. Without strict mode, a frame selector
// that matches several frames enters the first one.
export function toPlaywrightSelector(selector: string, strictMode: boolean): string {
    if (!selector.includes('>>') && !LABEL.test(selector)) return selector;
    const { clauses, separators } = splitSelector(selector);
    const enterFrame = strictMode ? ` >> ${ENTER_FRAME} >> ` : ` >> nth=0 >> ${ENTER_FRAME} >> `;
    let result = '';
    clauses.forEach((clause, i) => {
        const separator = separators[i];
        if (i === 0 && separator === '>>>' && clause.trim() === '') {
            result = `${ANY_FRAME} >> `;
            return;
        }
        result += translateClause(clause).trim();
        if (separator === '>>>') result += enterFrame;
        else if (separator === '>>') result += ' >> ';
    });
    return result;
}

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

export const MAX_RESPONSE_CHUNK_BYTES = 1000000;

export function splitUtf8ByMaxBytes(text: string, maxBytes: number): string[] {
    if (!text) {
        return [];
    }
    const chunks: string[] = [];
    let current = '';
    let currentBytes = 0;
    for (const char of text) {
        const charBytes = Buffer.byteLength(char, 'utf8');
        if (currentBytes + charBytes > maxBytes && current.length > 0) {
            chunks.push(current);
            current = char;
            currentBytes = charBytes;
        } else {
            current += char;
            currentBytes += charBytes;
        }
    }
    if (current.length > 0) {
        chunks.push(current);
    }
    return chunks;
}

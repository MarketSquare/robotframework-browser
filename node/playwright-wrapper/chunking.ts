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
    if (Buffer.byteLength(text, 'utf8') <= maxBytes) {
        return [text];
    }
    const bytes = Buffer.from(text, 'utf8');
    const chunks: string[] = [];
    let start = 0;
    while (start < bytes.length) {
        let end = Math.min(start + maxBytes, bytes.length);
        while (end > start && end < bytes.length && isContinuationByte(bytes[end])) {
            end--;
        }
        if (end === start) {
            end = start + 1;
            while (end < bytes.length && isContinuationByte(bytes[end])) {
                end++;
            }
        }
        chunks.push(bytes.toString('utf8', start, end));
        start = end;
    }
    return chunks;
}

function isContinuationByte(byte: number): boolean {
    return (byte & 0xc0) === 0x80;
}

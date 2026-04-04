/// <reference types="jest" />

import { describe, expect, it } from '@jest/globals';

import { splitUtf8ByMaxBytes } from '../chunking';

describe('splitUtf8ByMaxBytes', () => {
    it('returns empty array for empty string', () => {
        expect(splitUtf8ByMaxBytes('', 100)).toEqual([]);
    });

    it('returns single-element array when text is shorter than maxBytes', () => {
        const text = 'hello';
        const result = splitUtf8ByMaxBytes(text, 100);
        expect(result).toEqual(['hello']);
    });

    it('returns single-element array when text byte length equals maxBytes exactly', () => {
        const text = 'abc'; // 3 bytes
        const result = splitUtf8ByMaxBytes(text, 3);
        expect(result).toEqual(['abc']);
    });

    it('splits long ASCII text into chunks all within maxBytes', () => {
        const text = 'abcdefghij'; // 10 bytes ASCII
        const result = splitUtf8ByMaxBytes(text, 3);
        expect(result.length).toBeGreaterThan(1);
        for (const chunk of result) {
            expect(Buffer.byteLength(chunk, 'utf8')).toBeLessThanOrEqual(3);
        }
    });

    it('round-trip: joining all chunks produces the original string', () => {
        const text = 'abcdefghij';
        const result = splitUtf8ByMaxBytes(text, 3);
        expect(result.join('')).toBe(text);
    });

    it('handles multi-byte UTF-8 characters without splitting mid-character (emoji)', () => {
        // 🔥 is 4 bytes in UTF-8
        const text = '🔥🔥🔥';
        const result = splitUtf8ByMaxBytes(text, 5); // each chunk fits at most one emoji
        for (const chunk of result) {
            expect(Buffer.byteLength(chunk, 'utf8')).toBeLessThanOrEqual(5);
        }
        expect(result.join('')).toBe(text);
    });

    it('handles multi-byte UTF-8 characters without splitting mid-character (Japanese)', () => {
        // Each Japanese character is 3 bytes in UTF-8
        const text = '日本語';
        const result = splitUtf8ByMaxBytes(text, 4); // fits one char (3 bytes) per chunk
        for (const chunk of result) {
            expect(Buffer.byteLength(chunk, 'utf8')).toBeLessThanOrEqual(4);
        }
        expect(result.join('')).toBe(text);
    });

    it('returns single chunk when text has multi-byte chars that all fit', () => {
        const text = '日本語'; // 9 bytes total
        const result = splitUtf8ByMaxBytes(text, 100);
        expect(result).toEqual(['日本語']);
    });

    it('splits a long string into chunks each within byte limit', () => {
        const text = 'a'.repeat(10);
        const result = splitUtf8ByMaxBytes(text, 3);
        expect(result).toEqual(['aaa', 'aaa', 'aaa', 'a']);
    });
});

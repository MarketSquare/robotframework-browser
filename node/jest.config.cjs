// Jest configuration for Node.js unit tests
// rootDir resolves to the node/ directory (location of this config file)
module.exports = {
    preset: 'ts-jest',
    testEnvironment: 'node',
    rootDir: '.',
    // Transform TypeScript and JS files using ts-jest so ESM-style deps can be transpiled
    transform: {
        '^.+\\.(ts|tsx|js|jsx)$': 'ts-jest',
    },
    // Allow transforming specific ESM dependencies inside node_modules (e.g. uuid)
    transformIgnorePatterns: ['/node_modules/(?!(uuid)/)'],
    testMatch: ['<rootDir>/playwright-wrapper/__tests__/**/*.test.ts'],
    collectCoverageFrom: [
        'playwright-wrapper/**/*.ts',
        '!playwright-wrapper/generated/**',
        '!playwright-wrapper/index.ts',
    ],
    coverageDirectory: 'coverage',
    coverageReporters: ['text', 'text-summary', 'html', 'lcov', 'json-summary'],
};

import eslint from '@eslint/js';
import globals from 'globals';
import simpleImportSort from 'eslint-plugin-simple-import-sort';
import tseslint from 'typescript-eslint';

export default tseslint.config(
    { ignores: ['**/generated/**', '**/dist/**', '**/static/**'] },
    eslint.configs.recommended,
    tseslint.configs.recommendedTypeChecked,
    {
        plugins: { 'simple-import-sort': simpleImportSort },
        languageOptions: {
            parserOptions: {
                project: true,
                tsconfigRootDir: import.meta.dirname,
            },
        },
        rules: {
            'simple-import-sort/imports': 'error',
            'simple-import-sort/exports': 'error',
            // `any` flows pervasively from proto-generated types; these rules
            // would require wholesale re-typing of the gRPC layer to satisfy.
            '@typescript-eslint/no-explicit-any': 'off',
            '@typescript-eslint/no-unsafe-assignment': 'off',
            '@typescript-eslint/no-unsafe-argument': 'off',
            '@typescript-eslint/no-unsafe-return': 'off',
            '@typescript-eslint/no-unsafe-call': 'off',
            '@typescript-eslint/no-unsafe-member-access': 'off',
            // Async-without-await is a valid pattern for interface consistency.
            '@typescript-eslint/require-await': 'off',
            '@typescript-eslint/ban-ts-comment': [
                'error',
                {
                    'ts-expect-error': false,
                    'ts-ignore': false,
                    'ts-nocheck': false,
                    'ts-check': false,
                    minimumDescriptionLength: 5,
                },
            ],
        },
    },
    {
        // Plain JS build scripts: disable type-aware rules and add Node globals.
        files: ['**/*.js'],
        extends: [tseslint.configs.disableTypeChecked],
        languageOptions: {
            globals: globals.node,
        },
        rules: {
            // CJS build scripts use require() — this is intentional.
            '@typescript-eslint/no-require-imports': 'off',
        },
    },
);
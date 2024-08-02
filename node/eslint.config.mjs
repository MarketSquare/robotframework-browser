import sortImportsEs6Autofix from "eslint-plugin-sort-imports-es6-autofix";
import tsParser from "@typescript-eslint/parser";
import path from "node:path";
import { fileURLToPath } from "node:url";
import js from "@eslint/js";
import { FlatCompat } from "@eslint/eslintrc";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const compat = new FlatCompat({
    baseDirectory: __dirname,
    recommendedConfig: js.configs.recommended,
    allConfig: js.configs.all
});

export default [{
    ignores: ["Browser/wrapper/generated/*"],
}, ...compat.extends(
    "plugin:@typescript-eslint/recommended",
    "prettier",
    "plugin:prettier/recommended",
), {
    plugins: {
        "sort-imports-es6-autofix": sortImportsEs6Autofix,
    },

    languageOptions: {
        parser: tsParser,
        ecmaVersion: 2020,
        sourceType: "module",

        parserOptions: {
            project: "./tsconfig.json",
            tsconfigRootDir: "./node",
        },
    },

    rules: {
        "@typescript-eslint/no-explicit-any": "off",

        "@typescript-eslint/ban-ts-comment": ["error", {
            "ts-expect-error": false,
            "ts-ignore": false,
            "ts-nocheck": false,
            "ts-check": false,
            minimumDescriptionLength: 5,
        }],

        "sort-imports-es6-autofix/sort-imports-es6": ["error", {}],
    },
}];
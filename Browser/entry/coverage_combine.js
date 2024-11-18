
const { argv } = require('node:process');
const { CoverageReport } = require('monocart-coverage-reports');

const coverageInput = argv[2];
const coverageOutput = argv[3];
const coverageConfig = argv[4];

const coverageOptions = {
    inputDir: coverageInput,
    outputDir: coverageOutput,
}


const report =  new CoverageReport(coverageOptions);
if (coverageConfig) {
    report.loadConfig(coverageConfig);
}
report.generate();

# Purpose
This folder contains test which are used to tidy parsing. It contains test data, 
which is not executed by `inv atest`, because test data transformmed by tidy and
library internal transformers. Example `Wait Until Network Is Idle` keyword
is transformmer to `Wait For Load State` keyword.

# Naming convension
Test data file which is transformed by tidy is names by: 
<transformer_name>_file.robot. File which tests the transformer
is named by: <transformer_name>_test.robot. Example: 
`network_idle_file.robot` is transformed by tidy
and `network_idle_test.robot` is the test which transforms the test
file.

# Excluding 
The test is exluded by adding `tidy-transformer` tag to the 
<transformer_name>_file.robot file.

*** Settings ***
Library  Browser

Test Setup	Open Browser	http://localhost:7272
Test Teardown	Close Browser


*** Test Cases ***
Invalids will raise error directly from Robot Framework
  run keyword and expect error  *'assertion_operator' got value 'invalidOperator' that cannot be converted to AssertionOperator*  Get Title  invalidOperator  value
  run keyword and expect error  *'assertion_operator' got value 'faultyOps' that cannot be converted to AssertionOperator*  Get URL  faultyOps
  run keyword and expect error  *'assertion_operator' got value '!=!' that cannot be converted to AssertionOperator*  get_text  h1  !=!  blaah
  run keyword and expect error  *'assertion_operator' got value 'huh' that cannot be converted to AssertionOperator*  Get Textfield Value  css=input#username_field  huh  hah
  run keyword and expect error  *'assertion_operator' got value 'equas' that cannot be converted to AssertionOperator*  Get Attribute  h1  innerText  equas  plaah
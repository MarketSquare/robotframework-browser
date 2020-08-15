*** Settings ***
Resource          imports.resource

*** Test Cases ***
Open PDF in another tab
   New Page    ${WELCOME_URL}
   Click   text=Open pdf
   ${b}=   get browser catalog

Open html in another tab
   New Page    ${WELCOME_URL}
   Click   text=Open html
   ${b}=   get browser catalog

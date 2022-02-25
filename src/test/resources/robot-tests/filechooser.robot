*** Settings ***
Suite Setup     createTestFileToTempDirectory
Library         OperatingSystem
Library         TestSwingLibrary

*** Variables ***
${fileChooserButton}  openFileChooser
${tempDir}  ${CURDIR}${/}test${/}tempdir
${fileToChoose}  ${tempDir}${/}test_file.txt
${anotherFile}  ${tempDir}${/}myFile.txt
${defaultFile}  ${tempDir}${/}someFile.txt

*** Test Cases ***
Choose From File Chooser Keyword Should Choose File From File Chooser
    pushButton  ${fileChooserButton}
    chooseFromFileChooser  ${fileToChoose}
    selectedFileShouldBe  ${fileToChoose}

Cancel File Chooser Keyword Should Cance File Choosing
    pushButton  ${fileChooserButton}
    cancelFileChooser
    fileChooserShouldHaveBeenCancelled

Save File In File Chooser With Non Existing File
    pushButton  ${fileChooserButton}
    chooseFromFileChooser  ${anotherFile}
    selectedFileShouldBe  ${anotherFile}

Choose File In File Chooser Without Args
    pushButton  ${fileChooserButton}
    chooseFromFileChooser
    selectedFileShouldBe  ${defaultFile}

*** Keywords ***
createTestFileToTempDirectory
    Create Directory  ${tempDir}
    touch  ${fileToChoose}


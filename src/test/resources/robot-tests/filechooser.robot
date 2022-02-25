*** Settings ***
Suite Setup     createTestFileToTempDirectory
Library         OperatingSystem
Library         TestSwingLibrary

*** Variables ***
${fileChooserButton}  openFileChooser
${temp_work_dir}  ${CURDIR}${/}test${/}tempdir
${fileToChoose}  ${temp_work_dir}${/}test_file.txt
${anotherFile}  ${temp_work_dir}${/}myFile.txt
${defaultFile}  ${temp_work_dir}${/}someFile.txt

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
    Create Directory  ${temp_work_dir}
    touch  ${fileToChoose}


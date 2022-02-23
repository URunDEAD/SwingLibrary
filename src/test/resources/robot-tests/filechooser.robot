*** Settings ***
Suite Setup     createTestFileToTempDirectory
Library         OperatingSystem
Library         TestSwingLibrary

*** Variables ***
${fileChooserButton}  openFileChooser
${fileToChoose}  c:\\Users\\runneradmin\\AppData\\Local\\Temp\\test_file.txt
${anotherFile}  c:\\Users\\runneradmin\\AppData\\Local\\Temp\\myFile.txt
${defaultFile}  c:\\Users\\runneradmin\\AppData\\Local\\Temp\\someFile.txt

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
    touch  ${fileToChoose}


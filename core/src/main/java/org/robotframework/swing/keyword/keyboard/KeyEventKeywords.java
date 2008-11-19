/*
 * Copyright 2008 Nokia Siemens Networks Oyj
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.robotframework.swing.keyword.keyboard;

import org.robotframework.javalib.annotation.ArgumentNames;
import org.robotframework.javalib.annotation.RobotKeyword;
import org.robotframework.javalib.annotation.RobotKeywords;

/**
 * @author Heikki Hulkko
 */
@RobotKeywords
public class KeyEventKeywords {
    private KeyEventSender keyEventSender = new KeyEventSender();
    
    @RobotKeyword("Sends key strokes to the currently selected component.\n\n"
        + "Example with textfield:\n"
        + "| Select Context        | _myTextfield_        |                      |\n"
        + "| Send Keyboard Event   | _VK_S_               |                      |\n"
        + "| Send Keyboard Event   | _VK_O_               |                      |\n"
        + "| Send Keyboard Event   | _VK_M_               |                      |\n"
        + "| Send Keyboard Event   | _VK_E_               |                      |\n"
        + "| Send Keyboard Event   | _VK_T_               | _SHIFT_MASK_         |\n"
        + "| Send Keyboard Event   | _VK_E_               |                      |\n"
        + "| Send Keyboard Event   | _VK_X_               |                      |\n"
        + "| Send Keyboard Event   | _VK_T_               |                      |\n"
        + "| ${textFieldContents}= | Get Text Field Value | _myTextfield_        |\n"
        + "| Should Be Equal       | someText             | ${textFieldContents} |\n\n"
        + "Example with table:\n"
        + "| SelectTableCell               | _myTable_ | _0_          | _0_ |\n"
        + "| Send Keyboard Event           | _VK_TAB_  |              |     |\n" 
        + "| Table Cell Should Be Selected | _myTable_ | _0_          | _1_ |\n"
        + "| Send Keyboard Event           | _VK_TAB_  | _SHIFT_MASK_ |     |\n" 
        + "| Table Cell Should Be Selected | _myTable_ | _0_          | _0_ |\n")
    @ArgumentNames({"keyCode", "*modifiers"})
    public void sendKeyboardEvent(String keyCode, String[] modifiers) {
        keyEventSender.sendEvent(keyCode, modifiers);
    }
}
/*global chrome*/

// Daksha
// Copyright (C) 2021 myKaarma.
// opensource@mykaarma.com
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Affero General Public License for more details.
// You should have received a copy of the GNU Affero General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.

import React, { useState } from 'react';
import '../ComponentCss/dakshaRecorderCustomHardwaitPage.css';
import GlobalVariables from './globalConfigs';
let dakshaRecorderMainPage = GlobalVariables.dakshaRecorderMainPage ;
function DakshaRecorderCustomHardwaitPage(props) {
    const [val, setval] = useState();
    const func = (value) => {
        if (value >= 0) {
            setval(value);
        }
    }
    return (
        <>
            <div className='custom-hardwait-main-container'>
                <div  className='custom-hardwait-back-function' onClick={() => props.setState(dakshaRecorderMainPage)}>
                    Back
                </div>
                <div className='custom-hardwait-input-container'>

                    <div className='custom-hardwait-title-div'>
                        CUSTOM HARD WAIT
                    </div>

                    <div>
                        <input id='custom-hardwait-inputbox' placeholder=" Enter # of seconds" type='number' value={val} onChange={(e) => func(e.target.value)} />
                    </div>
                    <div id='custom-hardwait-button' onClick={() => {
                        props.setState(2);
                        chrome.tabs.query({ active: true, lastFocusedWindow: true }, tabs => {
                            let obj = {
                                "type": "customSecondsWait",
                                "sec": val
                            }
                            chrome.tabs.sendMessage(tabs[0].id, obj, () => { return true; });
                        })
                    }}>
                        ADD HARD WAIT
                    </div>
                </div>
            </div>
        </>
    )
}

export default DakshaRecorderCustomHardwaitPage;
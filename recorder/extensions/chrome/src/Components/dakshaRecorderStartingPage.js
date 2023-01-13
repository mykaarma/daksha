/*
Daksha
Copyright (C) 2021 myKaarma.
opensource@mykaarma.com
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.
You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/
/*global chrome*/
import React from 'react'
import '../ComponentCss/dakshaRecorderStartingPage.css';
import setBadgeForRecording from './setBadgeForRecording';
import GlobalVariables from "./globalConfigs";
let dakshaRecorderMainPage = GlobalVariables.dakshaRecorderMainPage;

function DakshaRecorderStartingPage(props) {

    return (
        <>
            <div className="mainDiv">
                <div className="title-div">
                    Daksha Recorder
                </div>
                <div className="recording-button-div" id="record" onClick={() => {
                    props.setState(dakshaRecorderMainPage);
                    let url = "";
                    chrome.tabs.query({ active: true, lastFocusedWindow: true }, tabs => {
                        url = tabs[0].url;
                        let obj = {
                            "type": "start",
                            "msg": url
                        }
                        chrome.tabs.sendMessage(tabs[0].id, obj, () => { return true; });
                        setBadgeForRecording();
                    });

                }}>
                    START RECORDING
                </div>
            </div>
        </>
    )
}

export default DakshaRecorderStartingPage;
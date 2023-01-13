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
import React from "react";
import "../ComponentCss/dakshaRecorderMainPage.css";
import PlayButton from '../Icons/PlayButton.png';
import PauseButton from '../Icons/PauseButton.png';
import StopButton from '../Icons/StopButton.png';
import RightArrow from '../Icons/RightArrow.png';
import removeBadgeForRecording from "./removeBadgeForRecording";
import setBadgeForRecording from "./setBadgeForRecording";
import GlobalVariables from "./globalConfigs";
let dakshaRecorderCustomHardwaitPage = GlobalVariables.dakshaRecorderCustomHardwaitPage;
let dakshaRecorderEndPage = GlobalVariables.dakshaRecorderEndPage;
let play = 2 ;
let pause = 1 ;
function PlayPause(props) {

    if (props.image === pause)
        return (
            <img className="main-page-button" src={PauseButton} onClick={() => {
                props.changeImage(2);
                chrome.tabs.query({ active: true, lastFocusedWindow: true }, tabs => {
                    let obj = {
                        "type": "pause"
                    }
                    chrome.tabs.sendMessage(tabs[0].id, obj, () => { return true; });
                    removeBadgeForRecording();
                })
            }
            } />
        )
    else if (props.image === play) {
        return (
            <img className="main-page-button" src={PlayButton} onClick={() => {
                props.changeImage(1);
                chrome.tabs.query({ active: true, lastFocusedWindow: true }, tabs => {
                    let obj = {
                        "type": "resume"
                    }
                    chrome.tabs.sendMessage(tabs[0].id, obj, () => { return true; });
                    setBadgeForRecording();
                })
            }} />
        )
    }
}
function DakshaRecorderMainPage(props) {
    return (
        <>
            <div className="main-page-container">
                <div className="main-page-title-div">
                    Daksha Recorder
                </div>
                <div className="main-page-playpause-div">
                    <PlayPause image={props.image} changeImage={props.changeImage} />
                    <img className="main-page-button" src={StopButton} onClick={() => {
                        props.setState(dakshaRecorderEndPage);
                        removeBadgeForRecording();
                        chrome.tabs.query({ active: true, lastFocusedWindow: true }, tabs => {
                            let obj = {
                                "type": "stop"
                            }
                            chrome.tabs.sendMessage(tabs[0].id, obj, () => { return true; });
                        })
                    }} />
                </div>
                <div className="main-page-all-options-container">
                    <div className="main-page-first-option-container">
                        <div id="hardwait" onClick={() => {
                            chrome.tabs.query({ active: true, lastFocusedWindow: true }, tabs => {
                                let obj = {
                                    "type": "tenSecondsWait"
                                }
                                chrome.tabs.sendMessage(tabs[0].id, obj, () => { return true; });
                            })
                        }}>
                            HARD WAIT (10 SEC)
                        </div>
                        <div id="custom-hardwait" onClick={() => props.setState(dakshaRecorderCustomHardwaitPage)}>
                            <img id="main-page-right-arrow" src={RightArrow} />
                        </div>
                    </div>
                    <div className="main-page-other-option-div" onClick={() => {
                        chrome.tabs.query({ active: true, lastFocusedWindow: true }, tabs => {
                            let obj = {
                                "type": "viewYaml"
                            }
                            chrome.tabs.sendMessage(tabs[0].id, obj, () => { return true; });
                        })
                    }}>
                        VIEW YAML
                    </div>
                    <div className="main-page-other-option-div" onClick={() => {
                        chrome.tabs.query({ active: true, lastFocusedWindow: true }, tabs => {
                            let obj = {
                                "type": "undoLastStep"
                            }
                            chrome.tabs.sendMessage(tabs[0].id, obj, () => { return true; });
                        })
                    }}>
                        UNDO LAST STEP
                    </div>
                </div>
            </div>
        </>
    )
}

export default DakshaRecorderMainPage;
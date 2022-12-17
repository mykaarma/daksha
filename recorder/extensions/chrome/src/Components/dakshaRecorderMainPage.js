/*global chrome*/
import React from "react";
import "../ComponentCss/dakshaRecorderMainPage.css";
import PlayButton from '../Icons/PlayButton.png';
import PauseButton from '../Icons/PauseButton.png';
import StopButton from '../Icons/StopButton.png';
import RightArrow from '../Icons/RightArrow.png';
import removeBadgeForRecording from "./removeBadgeForRecording";
import setBadgeForRecording from "./setBadgeForRecording";

let dakshaRecorderStartingPage = 1;
let dakshaRecorderMainPage = 2 ;
let dakshaRecorderCustomHardwaitPage = 3 ;
let dakshaRecorderEndPage = 4 ;

function PlayPause(props) {

    if (props.image === 1)
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
    else if (props.image === 2) {
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
/*global chrome*/
import React from "react";
import "../ComponentCss/popup1.css";
import { useState, useEffect } from 'react';
import PlayButton from '../Svg/PlayButton.png';
import PauseButton from '../Svg/PauseButton.png';
import StopButton from '../Svg/StopButton.png';
import RightArrow from '../Svg/RightArrow.png';
import removeBadgeForRecording from "./removeBadgeForRecording";
import badgeForRecording from "./badgeForRecording";


function PlayPause(props) {

    if (props.image === 1)
        return (
            <img className="popup1-button" src={PauseButton} onClick={() => {
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
            <img className="popup1-button" src={PlayButton} onClick={() => {
                props.changeImage(1);
                chrome.tabs.query({ active: true, lastFocusedWindow: true }, tabs => {
                    let obj = {
                        "type": "resume"
                    }
                    chrome.tabs.sendMessage(tabs[0].id, obj, () => { return true; });
                    badgeForRecording();
                })
            }} />
        )
    }
}
function Popup1(props) {
    return (
        <>
            <div className="main-container">
                <div className="first-div">
                    Daksha Recorder
                </div>
                <div className="second-div">
                    <PlayPause image={props.image} changeImage={props.changeImage} />
                    <img className="popup1-button" src={StopButton} onClick={() => {
                        props.setState(4);
                        removeBadgeForRecording();
                        chrome.tabs.query({ active: true, lastFocusedWindow: true }, tabs => {
                            let obj = {
                                "type": "stop"
                            }
                            chrome.tabs.sendMessage(tabs[0].id, obj, () => { return true; });
                        })
                    }} />
                </div>
                <div className="third-container">
                    <div className="sub-third-container">
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
                        <div id="custom-hardwait" onClick={() => props.setState(3)}>
                            <img id="popup1-right-arrow" src={RightArrow} />
                        </div>
                    </div>
                    <div className="fourth-container" onClick={() => {
                        chrome.tabs.query({ active: true, lastFocusedWindow: true }, tabs => {
                            let obj = {
                                "type": "viewYaml"
                            }
                            chrome.tabs.sendMessage(tabs[0].id, obj, () => { return true; });
                        })
                    }}>
                        VIEW YAML
                    </div>
                    <div className="fourth-container" onClick={() => {
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

export default Popup1;
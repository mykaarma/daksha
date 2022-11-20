/*global chrome*/
import React from "react";
import '../ComponentCss/popup3.css'
import badgeForRecording from "./badgeForRecording";
function popup3(props) {
    return (
        <>
            <div className="popup3-container">
                <div>
                    Daksha Recorder
                </div>
                <div className="popup3-second-container">
                    <div className="popup3-second-div" onClick={() => {
                        props.setState(1);
                        chrome.tabs.query({ active: true, lastFocusedWindow: true }, tabs => {
                            let obj = {
                                "type": "download"
                            }
                            chrome.tabs.sendMessage(tabs[0].id, obj, () => { return true; });
                        })
                    }}>
                        DOWNLOAD
                    </div>
                    <div className="popup3-second-div" onClick={() => {
                        props.setState(1);
                        chrome.tabs.query({ active: true, lastFocusedWindow: true }, tabs => {
                            let obj = {
                                "type": "copy_to_clipboard"
                            }
                            chrome.tabs.sendMessage(tabs[0].id, obj, () => { return true; });
                        })
                    }}>
                        COPY TO CLIPBOARD
                    </div>
                    <div className="popup3-second-div" id="popup3-recording-button" onClick={() => {
                        props.changeImage(1);
                        props.setState(2);
                        let url = "" ;
                            chrome.tabs.query({ active: true, lastFocusedWindow: true }, tabs => {
                                url = tabs[0].url;
                                let obj = {
                                    "type": "start",
                                    "msg": url
                                }
                                chrome.tabs.sendMessage(tabs[0].id, obj, () => { return true; });
                                badgeForRecording() ;
                            })
                    }}>
                        START RECORDING
                    </div>
                </div>
            </div>
        </>
    )
}



export default popup3;
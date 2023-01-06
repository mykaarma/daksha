/*global chrome*/
import React from "react";
import '../ComponentCss/dakshaRecorderEndPage.css';
import setBadgeForRecording from "./setBadgeForRecording";
import GlobalVariables from "./globalConfigs";
let dakshaRecorderStartingPage = GlobalVariables.dakshaRecorderStartingPage;
let dakshaRecorderMainPage = GlobalVariables.dakshaRecorderMainPage;

function DakshaRecorderEndPage(props) {
    return (
        <>
            <div className="end-page-container">
                <div>
                    Daksha Recorder
                </div>
                <div className="end-page-all-options-container">
                    <div className="end-page-each-option-div" onClick={() => {
                        props.setState(dakshaRecorderStartingPage);
                        chrome.tabs.query({ active: true, lastFocusedWindow: true }, tabs => {
                            let obj = {
                                "type": "download"
                            }
                            chrome.tabs.sendMessage(tabs[0].id, obj, () => { return true; });
                        })
                    }}>
                        DOWNLOAD
                    </div>
                    <div className="end-page-each-option-div" onClick={() => {
                        props.setState(dakshaRecorderStartingPage);
                        chrome.tabs.query({ active: true, lastFocusedWindow: true }, tabs => {
                            let obj = {
                                "type": "copy_to_clipboard"
                            }
                            chrome.tabs.sendMessage(tabs[0].id, obj, () => { return true; });
                        })
                    }}>
                        COPY TO CLIPBOARD
                    </div>
                    <div className="end-page-each-option-div" id="end-page-recording-button" onClick={() => {
                        props.changeImage(1);
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
                        })
                    }}>
                        START RECORDING
                    </div>
                </div>
            </div>
        </>
    )
}



export default DakshaRecorderEndPage;
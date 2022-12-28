/*global chrome*/
import React, { useState } from 'react';
import '../ComponentCss/dakshaRecorderCustomHardwaitPage.css';
let dakshaRecorderStartingPage = 1;
let dakshaRecorderMainPage = 2 ;
let dakshaRecorderCustomHardwaitPage = 3 ;
let dakshaRecorderEndPage = 4 ;
let standardHardWaitTime = 10 ;
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
                            if(val === undefined){
                                alert("Kindly enter a numeric value") ;
                            }
                            else{
                            let obj = {
                                "type": "customSecondsWait",
                                "sec": val
                            }
                            chrome.tabs.sendMessage(tabs[0].id, obj, () => { return true; });
                        }
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
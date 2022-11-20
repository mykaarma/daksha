/*global chrome*/
import React, { useState } from 'react';
import '../ComponentCss/popup2.css';
import BackButton from '../Svg/BackButton.png'
function Popup2(props) {
    const [val, setval] = useState();
    const func = (value) => {
        if (value >= 0) {
            setval(value);
        }
    }
    return (
        <>
            <div className='popup2-container'>
                <div  className='back-function' onClick={() => props.setState(2)}>
                    {/* <img className='back-function' src={BackButton}  /> */}
                    Back
                </div>
                <div className='popup2-input-container'>

                    <div className='popup2-custom-hard-wait'>
                        CUSTOM HARD WAIT
                    </div>

                    <div>
                        <input id='popup2-custom-input' placeholder=" Enter # of seconds" type='number' value={val} onChange={(e) => func(e.target.value)} />
                    </div>
                    <div id='popup2-custom-hardwait' onClick={() => {
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

export default Popup2;
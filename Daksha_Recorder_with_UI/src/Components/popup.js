/*global chrome*/
import React from 'react'
import '../ComponentCss/style.css' ;
import badgeForRecording from './badgeForRecording';
function Popup(props){
 return (
    <>
    <div className="mainDiv">
    <div className="firstDiv">
        Daksha Recorder
    </div>
    <div className="secondDiv" id="record" onClick={()=>{
        props.setState(2) ;
        let url = "" ;
        chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
             url = tabs[0].url;
             let obj = {
                "type" : "start", 
                "msg"  :  url
            }
            chrome.tabs.sendMessage(tabs[0].id , obj , ()=>{ return true ;}) ;
            badgeForRecording();
    });
        
    }}>
        START RECORDING
    </div>
</div>
</>
 )
}

export default Popup ;
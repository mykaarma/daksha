/*global chrome*/
import React from 'react'
import '../ComponentCss/dakshaRecorderStartingPage.css' ;
import setBadgeForRecording from './setBadgeForRecording';

let dakshaRecorderStartingPage = 1;
let dakshaRecorderMainPage = 2 ;
let dakshaRecorderCustomHardwaitPage = 3 ;
let dakshaRecorderEndPage = 4 ;

function DakshaRecorderStartingPage(props){
    
 return (
    <>
    <div className="mainDiv">
    <div className="title-div">
        Daksha Recorder
    </div>
    <div className="recording-button-div" id="record" onClick={()=>{
        props.setState(dakshaRecorderMainPage) ;
        let url = "" ;
        chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
             url = tabs[0].url;
             let obj = {
                "type" : "start", 
                "msg"  :  url
            }
            chrome.tabs.sendMessage(tabs[0].id , obj , ()=>{ return true ;}) ;
            setBadgeForRecording();
    });
        
    }}>
        START RECORDING
    </div>
</div>
</>
 )
}

export default DakshaRecorderStartingPage ;
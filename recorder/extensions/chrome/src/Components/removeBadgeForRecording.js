/*global chrome*/
function removeBadgeForRecording() {
  return (
        chrome.action.setBadgeBackgroundColor({color:'#F00'} , ()=>{
            chrome.action.setBadgeText({text: ''}) ;
        })
  )
}

export default removeBadgeForRecording
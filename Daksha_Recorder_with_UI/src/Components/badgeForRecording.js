/*global chrome*/
function badgeForRecording() {
  return (
    chrome.action.setBadgeBackgroundColor({color:'#F00'} , ()=>{
        chrome.action.setBadgeText({text: 'REC'}) ;
    })
  )
}

export default badgeForRecording
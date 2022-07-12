// Daksha
// Copyright (C) 2021 myKaarma.
// opensource@mykaarma.com
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Affero General Public License for more details.
// You should have received a copy of the GNU Affero General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.



// Initialising Context Menus Which we want in our Chrome Extension.
let copy_to_clipboard = {
    "id" : "copy_to_clipboard" , 
    "title": "Stop And Copy to clipboard" , 
    "contexts":["all"]
}
let download = {
    "id" : "download" , 
    "title": "Stop And Download" , 
    "contexts":["all"]
}
let pause = {
    "id" : "pause" ,
    "title": "Pause" , 
    "contexts" : ["all"]
}
let start = {
    "id" : "start" ,
    "title" : "Start Daksha Recorder" , 
    "contexts" : ["all"]
}
let resume = {
    "id" : "resume" ,
    "title" : "Resume" , 
    "contexts" : ["all"]
}

//Installing Context Menus at the beginning of chrome Extension Installed.
chrome.runtime.onInstalled.addListener(() =>{
    chrome.contextMenus.create(start) ;
})

// Listening the Clicks on the Context menu and sending messages to index.js.
chrome.contextMenus.onClicked.addListener((info , tab) =>{
    if(info.menuItemId === "copy_to_clipboard"){
        let obj = {
            "type" : "copy_to_clipboard"
        }
        chrome.tabs.sendMessage(tab.id , obj , ()=>{ return true ;}) ;
        chrome.contextMenus.removeAll() ;
        chrome.contextMenus.create(start) ;
    }
    else if(info.menuItemId === "download"){
        let obj = {
            "type" : "download"
        }
        chrome.tabs.sendMessage(tab.id , obj , ()=>{ return true ;}) ;
        chrome.contextMenus.removeAll() ;
        chrome.contextMenus.create(start) ;
}
    else if(info.menuItemId === "pause"){
        let obj = {
            "type" : "pause"
        }
        chrome.tabs.sendMessage(tab.id , obj , ()=>{ return true ;}) ;
        chrome.contextMenus.removeAll() ;
        chrome.contextMenus.create(resume) ;
        chrome.contextMenus.create(copy_to_clipboard) ;
        chrome.contextMenus.create(download) ;
    }
    else if(info.menuItemId === "start"){
        let url = "" ;
        chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
             url = tabs[0].url;
             let obj = {
                "type" : "start", 
                "msg"  :  url
            }
        chrome.tabs.sendMessage(tab.id , obj , ()=>{ return true ;}) ;
        chrome.contextMenus.removeAll() ;
        chrome.contextMenus.create(pause) ;
        chrome.contextMenus.create(download) ; 
        chrome.contextMenus.create(copy_to_clipboard) ; 
        });
    }
    else if(info.menuItemId === "resume"){
        let obj = {
            "type" : "resume"
        }
        chrome.tabs.sendMessage(tab.id , obj , ()=>{ return true ;}) ;
        chrome.contextMenus.removeAll() ;
        chrome.contextMenus.create(pause) ;
        chrome.contextMenus.create(download) ;
        chrome.contextMenus.create(copy_to_clipboard) ;
    }
})
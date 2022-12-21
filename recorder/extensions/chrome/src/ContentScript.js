
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


let previousSelectedElementXpath = "";
let previousTargetElement;
// For parent window previousIframe === "" ;
let previousIframe = "";
let currentIframe = "";
let pauseVal = true;
let leftClickPressed = 0;
let dakshaYamlStorageKey = "generatedDakshaYaml";
let pauseValueStorageKey = "updatePauseValue";
let popupPageStorageKey = "popupPageNumber";
let playPauseStorageKey = "playPauseIcon";
let dakshaYamlFormatterRegex = />+-+\s*/g;
let yaml = require("js-yaml");
let RecordingCoordinates;
let recordingButton;
require('@webcomponents/custom-elements');
class WordCount extends HTMLElement {
    constructor() {
        super();
    }

    connectedCallback() {
        const shadow = this.attachShadow({ mode: 'open' });
        this.style.border = 'none';
        this.style.zIndex = '1000';
        this.style.position = 'absolute';

        this.style.top = `${RecordingCoordinates[1]}px`;
        this.style.left = `${RecordingCoordinates[0]}px`;
        this.style.height = '50px';
        this.style.width = '300px';
        let ifrm = document.createElement('iframe')
        ifrm.style.border = 'none';
        ifrm.style.position = 'relative';
        ifrm.style.height = '100%';
        ifrm.style.width = '100%';
        ifrm.style.padding = "0px";
        ifrm.style.boxShadow = "2px 4px 6px silver";
        ifrm.style.borderRadius = "5px";
        ifrm.src = chrome.runtime.getURL("./RecordingTab.html");

        shadow.appendChild(ifrm);
    }
}
let createRecordingButton = () => {
    recordingButton.style.display = '';
}
let removeRecordingButton = () => {
    recordingButton.style.display = 'none';

}
let draggabilityFunctionalityForrecordingDiv = () => {
    recordingButton = document.createElement('daksha-recorder');
    recordingButton.style.display = 'none';
    document.body.parentNode.appendChild(recordingButton);
    var dragItem = recordingButton
    var active = false;
    var currentX;
    var currentY;
    var initialX;
    var initialY;
    var startingX ;
    var startingY ;
    let xOffset = 0;
    var yOffset = 0;
    let dragStart = function (x, y) {
        initialX = x - xOffset;
        initialY = y - yOffset;
        active = true;
    }

    let dragEnd = function (e) {
        active = false;
    }
    let availableHeight = window.innerHeight;
    let totalHeight = window.screen.availHeight;
    let heightOfIframe = dragItem.offsetHeight;
    let drag = function (e) {

        if (active && e.screenY > totalHeight - availableHeight + heightOfIframe && e.screenY < totalHeight - heightOfIframe
            && e.screenX > 20 && e.screenX + 50 < window.innerWidth
        ) {
            currentX = e.screenX - initialX;
            currentY = e.screenY - initialY;
            xOffset = currentX;
            yOffset = currentY;

            setTranslate(currentX, currentY, dragItem);
        }
    }

    let setTranslate = function (xPos, yPos, el) {
        el.style.transform = "translate3d(" + xPos + "px, " + yPos + "px, 0)";
    }
    window.addEventListener('message', (e) => {

        if (e.data.type === "mousedown") {
            dragStart(e.data.x, e.data.y);
            startingX = e.data.x;
            startingY = e.data.y;
        }
        else if (e.data.type === "mousemove") {
            let obj = { screenX: e.data.x, screenY: e.data.y };
            drag(obj);
        }
        else if (e.data.type === "mouseup") {
            let obj = { screenX: e.data.x, screenY: e.data.y };
            dragEnd(obj);
            RecordingCoordinates[0] = obj.screenX - (startingX - RecordingCoordinates[0]);
            RecordingCoordinates[1] = obj.screenY - (startingY - RecordingCoordinates[1]);
            var dakshaYamlObject = {};
            dakshaYamlObject["RecordingCoordinates"] = RecordingCoordinates;
            chrome.storage.sync.set(dakshaYamlObject, () => {
            });
        }
    });
}
chrome.storage.sync.get(popupPageStorageKey, function (result) {
    var popupKey = result[popupPageStorageKey] ? result[popupPageStorageKey] : 1;
    var dakshaYamlObject = {};
    dakshaYamlObject[popupPageStorageKey] = popupKey;
    chrome.storage.sync.set(dakshaYamlObject, () => {
    });
});
chrome.storage.sync.get(playPauseStorageKey, function (result) {
    var playPauseKey = result[playPauseStorageKey] ? result[playPauseStorageKey] : 1;
    var dakshaYamlObject = {};
    dakshaYamlObject[playPauseStorageKey] = playPauseKey;
    chrome.storage.sync.set(dakshaYamlObject, () => {
    });
});
chrome.storage.sync.get("RecordingCoordinates", function (result) {
    RecordingCoordinates = result["RecordingCoordinates"];
    customElements.define('daksha-recorder', WordCount);
    draggabilityFunctionalityForrecordingDiv();
});

// Function to find XPath of a given Element in a given Document
function getXPath(selectedElement, selectedElementDocument) {

    var allNodes = selectedElementDocument.getElementsByTagName('*');
    for (var segs = []; selectedElement.parentNode && selectedElement.nodeType == 1; selectedElement = selectedElement.parentNode) {
        if (selectedElement.hasAttribute('id')) {
            var uniqueIdCount = 0;
            for (var n = 0; n < allNodes.length; n++) {
                if (allNodes[n].hasAttribute('id') && allNodes[n].id == selectedElement.id) uniqueIdCount++;
                if (uniqueIdCount > 1) break;
            };
            if (uniqueIdCount == 1) {
                segs.unshift('//' + selectedElement.localName.toLowerCase() + `[@id='${selectedElement.getAttribute('id')}']`);
                return segs.join('/');
            } else {
                segs.unshift(selectedElement.localName.toLowerCase() + `[@id='${selectedElement.getAttribute('id')}']`);
            }
        }
        else {
            for (i = 1, siblingsOfSelectedElement = selectedElement.previousSibling; siblingsOfSelectedElement; siblingsOfSelectedElement = siblingsOfSelectedElement.previousSibling) {
                if (siblingsOfSelectedElement.localName == selectedElement.localName) i++;
            };
            segs.unshift(selectedElement.localName.toLowerCase() + '[' + i + ']');
        };
    };
    return segs.length ? '//' + segs.join('/') : null;
};
// This function is used to update the Daksha Yaml and Add new dakshaYamlObjectss.
function updateDakshaYamlFile(dakshaYamlObjects) {

    chrome.storage.sync.get(dakshaYamlStorageKey, function (result) {
        var array = result[dakshaYamlStorageKey] ? result[dakshaYamlStorageKey] : [];
        array.push.apply(array, dakshaYamlObjects);
        var dakshaYamlObject = {};
        dakshaYamlObject[dakshaYamlStorageKey] = array;
        chrome.storage.sync.set(dakshaYamlObject, () => {
        });
    });
}
// Defined the dakshaYamlObjectss which will be added into the updateDakshaYamlFile function!!
let fill_data = (xpath, value) => {
    let json_obj = {
        "fill_data": {
            "xpath": `${xpath}`,
            "value": `${value}`
        }
    };
    return json_obj;
}
let hard_wait = (sec) => {
    let json_obj = {
        "wait_for": {
            "mode": 'hardwait',
            "value": sec
        }
    }

    return json_obj;
}
let switch_iframe = (xpath) => {
    let json_obj = {
        "switch_iframe": {
            "xpath": `${xpath}`
        }
    };

    return json_obj;
}
let switch_to_default_iframe = () => {
    let json_obj = {
        "switch_to_default_iframe": {}
    }

    return json_obj;
}
let click_button = (xpath) => {
    let json_obj = {
        "click_button": {
            "xpath": `${xpath}`
        }
    };

    return json_obj;
};
let open_url = (url) => {
    let json_obj = {
        "open_url": {
            "url": `${url}`
        }
    };

    return json_obj;
};
function getDakshaEventsArray(event) {
    // Adding objects to the dakshaYamlObjects array to push them updateDakshaYamlFile function 
    let dakshaYamlObjects = [];
    if (previousSelectedElementXpath !== "") {
        if (previousTargetElement !== null && previousTargetElement !== undefined) {
            let previousTargetElementTagName = previousTargetElement.tagName.toLowerCase();
            let previousTargetElementValue = previousTargetElement.value;
            if ((previousTargetElementTagName === "input" || previousTargetElementTagName === "textarea")) {
                dakshaYamlObjects.push(fill_data(previousSelectedElementXpath, previousTargetElementValue));
            }
        }
    }
    let targetElement = event.target;
    previousTargetElement = targetElement;
    let selectedElementDocument = event.view.document;
    let XPath = getXPath(targetElement, selectedElementDocument);
    previousSelectedElementXpath = XPath;
    dakshaYamlObjects.push(click_button(XPath));
    return dakshaYamlObjects;
}
function eventHandlerInIframe(event) {
    //Handling the events occurred inside the Iframes 
    if (event.button === leftClickPressed) {
        if (pauseVal === false) {
            let dakshaYamlObjects = [];
            let selectedIframeXpath = getXPath(document.activeElement, document);
            previousIframe = currentIframe;
            currentIframe = `${selectedIframeXpath}`;
            if (previousIframe != currentIframe) {
                if (previousIframe === "") {
                    dakshaYamlObjects.push(switch_iframe(selectedIframeXpath));
                }
                else {
                    dakshaYamlObjects.push(switch_to_default_iframe());
                    dakshaYamlObjects.push(switch_iframe(selectedIframeXpath));
                }

            }
            let dakshaEventsArray = getDakshaEventsArray(event);
            dakshaYamlObjects.push.apply(dakshaYamlObjects, dakshaEventsArray);
            updateDakshaYamlFile(dakshaYamlObjects);
        }
    }
}
function AddEventListenerToAllIframe(document) {
    //Adding Event Listener to all iframes 
    let allIframe = document.getElementsByTagName("iframe");
    Array.prototype.slice.call(allIframe).forEach(iframe => {
        let iwindow = iframe.contentWindow;

        iframe.onload = () => {
            iwindow.addEventListener('mousedown', eventHandlerInIframe);
        }
    });
}

function getYamlFileData(array) {
    var dakshaYamlObjects = {
        "config": {
            "env": "",
            "browser": "",
            "driverAddress": ""
        },
        "name": "",
        "alert_type": "", 'task': array
    };
    let data = yaml.dump(JSON.parse(JSON.stringify(dakshaYamlObjects)));
    let regexFormattedData = data.replace(dakshaYamlFormatterRegex, '');
    return regexFormattedData;

}
function resetAndStartAgain() {
    chrome.storage.sync.remove(dakshaYamlStorageKey, () => { });
    previousSelectedElementXpath = "";
    previousIframe = "";
    currentIframe = "";
    previousTargetElement = null;
    var dakshaYamlObject = {};
    dakshaYamlObject[pauseValueStorageKey] = true;
    chrome.storage.sync.set(dakshaYamlObject, () => {
    });
    pauseVal = true;

}

// Fetching the information whether the chrome extension is pauseVald or not 
chrome.storage.sync.get(pauseValueStorageKey, function (result) {
    if (result[pauseValueStorageKey] !== null) {
        pauseVal = result[pauseValueStorageKey];
        if (pauseVal === false) {
            createRecordingButton();
        }
    }
})
//Listening to the mutation to add dakshaEventsArrayeners of iframes.
let mutationObserver = new MutationObserver(function (mutations) {
    mutations.forEach(function (mutation) {
        AddEventListenerToAllIframe(document);
    });
});
mutationObserver.observe(document, {
    attributes: true,
    characterData: true,
    childList: true,
    subtree: true,
    attributeOldValue: true,
    characterDataOldValue: true
});
// Adding mousdown dakshaEventsArrayener to window.
window.addEventListener('mousedown', (event) => {
    if (event.button === leftClickPressed) {
        if (pauseVal === false) {
            let dakshaYamlObjects = [];
            previousIframe = currentIframe;
            currentIframe = "";
            if (previousIframe != currentIframe) {
                dakshaYamlObjects.push(switch_to_default_iframe);
            }
            let dakshaEventsArray = getDakshaEventsArray(event);
            dakshaYamlObjects.push.apply(dakshaYamlObjects, dakshaEventsArray);
            updateDakshaYamlFile(dakshaYamlObjects);
        }
    }
})

// Listening to the Context Menu Clicks.
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.type === "copy_to_clipboard") {
        chrome.storage.sync.get(dakshaYamlStorageKey, function (result) {
            var array = result[dakshaYamlStorageKey];
            let data = getYamlFileData(array);
            navigator.clipboard.writeText(data).then(() => {
                alert('All your data has been Copied to clipboard , You can now start again!');
            })
                .catch((e) => {
                    console.log(e);
                })
        });
        resetAndStartAgain();
    }
    else if (request.type === "download") {
        chrome.storage.sync.get(dakshaYamlStorageKey, function (result) {
            var array = result[dakshaYamlStorageKey];
            let data = getYamlFileData(array);
            let blob = new Blob([data], { type: 'application/yaml' });
            let url = URL.createObjectURL(blob);
            let windowOfNewTab = window.open("https://www.google.com");
            var anchorTag = windowOfNewTab.document.createElement('a');
            anchorTag.href = url;
            anchorTag.download = "daksha.yaml";
            anchorTag.style.display = 'none';
            windowOfNewTab.document.body.appendChild(anchorTag);
            anchorTag.click();
            delete anchorTag;
        });
        resetAndStartAgain();
        alert('All your data has been Downloaded , You can now start again!');
    }
    else if (request.type === "pause") {
        var dakshaYamlObject = {};
        dakshaYamlObject[pauseValueStorageKey] = true;
        chrome.storage.sync.set(dakshaYamlObject, () => {
        });
        pauseVal = true;
        removeRecordingButton();
    }
    else if (request.type === "start") {
        chrome.storage.sync.remove(dakshaYamlStorageKey, () => { });
        previousSelectedElementXpath = "";
        previousIframe = "";
        currentIframe = "";
        previousTargetElement = null;
        var dakshaYamlObject = {};
        dakshaYamlObject[pauseValueStorageKey] = false;
        chrome.storage.sync.set(dakshaYamlObject, () => {
        });
        pauseVal = false;
        updateDakshaYamlFile([open_url(request.msg)]);
        createRecordingButton();
    }
    else if (request.type === "resume") {
        var dakshaYamlObject = {};
        dakshaYamlObject[pauseValueStorageKey] = false;
        chrome.storage.sync.set(dakshaYamlObject, () => {
        });
        pauseVal = false;
        createRecordingButton();
    }
    else if (request.type === "customSecondsWait") {
        updateDakshaYamlFile([hard_wait(request.sec)]);
        alert(`${request.sec} seconds hard wait added!`);
    }
    else if (request.type === "tenSecondsWait") {
        var secs = 10;
        updateDakshaYamlFile([hard_wait(secs)]);
        alert("10 secs hard wait added!");
    }
    else if (request.type === "stop") {
        if (pauseVal === false) {
            var dakshaYamlObject = {};
            dakshaYamlObject[pauseValueStorageKey] = true;
            chrome.storage.sync.set(dakshaYamlObject, () => {
            });
            pauseVal = true;
            removeRecordingButton();
        };
    }
    else if (request.type === "viewYaml") {
        chrome.storage.sync.get(dakshaYamlStorageKey, function (result) {
            var array = result[dakshaYamlStorageKey];
            let data = getYamlFileData(array);
            var iframe = `<iframe width="100%" height="100%" srcdoc="` + `<pre>${data}</pre>` + `"></iframe>`
            var x = window.open("", "", "_blank");
            x.document.open();
            x.document.write(iframe);
        });
    }
    else if (request.type === "undoLastStep") {
        chrome.storage.sync.get(dakshaYamlStorageKey, function (result) {
            var array = result[dakshaYamlStorageKey];
            let length = array.length;
            if (length > 1) {
                array.pop();
                var dakshaYamlObject = {};
                dakshaYamlObject[dakshaYamlStorageKey] = array;
                chrome.storage.sync.set(dakshaYamlObject, () => {
                });
            }
        });
        alert("Last step has been removed!");
    }

    sendResponse({ msg: "Request Processed" });
    return Promise.resolve("Dummy response to keep the console quiet");
});
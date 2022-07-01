let prevXPath = "";
let prevTarelement;
let prevDefaultIframe = "";
let defaultIframe = "";
let pause = true;
let reg = />+-+\s*/g;
let yaml = require("js-yaml");
// Function to find XPath of a given Element in a given Document
function getXPath(elm, doc) {

    var allNodes = doc.getElementsByTagName('*');
    for (var segs = []; elm.parentNode && elm.nodeType == 1; elm = elm.parentNode) {
        if (elm.hasAttribute('id')) {
            var uniqueIdCount = 0;
            for (var n = 0; n < allNodes.length; n++) {
                if (allNodes[n].hasAttribute('id') && allNodes[n].id == elm.id) uniqueIdCount++;
                if (uniqueIdCount > 1) break;
            };
            if (uniqueIdCount == 1) {
                segs.unshift('//' + elm.localName.toLowerCase() + '[@id="' + elm.getAttribute('id') + '"]');
                return segs.join('/');
            } else {
                segs.unshift(elm.localName.toLowerCase() + '[@id="' + elm.getAttribute('id') + '"]');
            }
        }
        else {
            for (i = 1, sib = elm.previousSibling; sib; sib = sib.previousSibling) {
                if (sib.localName == elm.localName) i++;
            };
            segs.unshift(elm.localName.toLowerCase() + '[' + i + ']');
        };
    };
    return segs.length ? '//' + segs.join('/') : null;
};
// This function is used to update the Daksha Yaml and Add new tasks.
function updateTask(task) {

    chrome.storage.sync.get("storagekey", function (result) {
        var array = result["storagekey"] ? result["storagekey"] : [];
        array.push.apply(array, task);
        var jsonObj = {};
        jsonObj["storagekey"] = array;
        chrome.storage.sync.set(jsonObj, () => {
        });
    });
}
// Function tells us whether the chrome extension is paused and resumed.
function updateStatus() {

    chrome.storage.sync.get("updateKey", function (result) {
        let key = result["updateKey"] ? result["updateKey"] : true;
        pause = key;
    });
}
// Defined the tasks which will be added into the updateTask function!!
let fill_data = (xpath, value) => {
    let json_obj = {
        "fill_data": {
            "xpath": `${xpath}`,
            "value": `${value}`
        }
    };
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
let validate = (xpath) => {
    let json_obj = {
        "xpath": `${xpath}`
    }

    return json_obj;
};
function fillDataEvent(event) {
    // Adding objects to the task array to push them updateTask function 
    let task = [];
    if (prevXPath !== "") {
        if (prevTarelement !== null && prevTarelement !== undefined) {
            let prevTagName = prevTarelement.tagName.toLowerCase();
            let prevVal = prevTarelement.value;
            if ((prevTagName === "input" || prevTagName === "textarea")) {
                task.push(fill_data(prevXPath, prevVal));
            }
        }
    }
    let tarelement = event.target;
    prevTarelement = tarelement;
    let doc = event.view.document;
    let XPath = getXPath(tarelement, doc);
    prevXPath = XPath;
    task.push(click_button(XPath));
    return task;
}
function eventHandlerInIframe(event) {
    //Handling the events occurred inside the Iframes 
    if (pause === false) {
        let task = [];
        let XiPath = getXPath(document.activeElement, document);
        prevDefaultIframe = defaultIframe;
        defaultIframe = `${XiPath}`;
        if (prevDefaultIframe != defaultIframe) {
            if (prevDefaultIframe === "") {
                task.push(switch_iframe(XiPath));
            }
            else {
                task.push(switch_to_default_iframe());
                task.push(switch_iframe(XiPath));
            }

        }
        let tas = fillDataEvent(event);
        task.push.apply(task, tas);
        updateTask(task);
    }
}
function AddEventListenerToAllIframe(document) {
    //Adding Event Listener to all iframes 
    let allIframe = document.getElementsByTagName("iframe");
    Array.prototype.slice.call(allIframe).forEach(iframe => {
        let iwindow = iframe.contentWindow;

        iframe.onload = () => {
            iwindow.addEventListener('click', eventHandlerInIframe);
        }
    });
}
//Calling this function to fetch the state of the chrome Extension whether it is recording or not.
updateStatus();
//Listening to the mutation to add listeners of iframes.
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
// Adding mousdown listener to window.
window.addEventListener('mousedown', (event) => {
    if (event.button === 0) {
        if (pause === false) {
            let task = [];
            prevDefaultIframe = defaultIframe;
            defaultIframe = "";
            if (prevDefaultIframe != defaultIframe) {
                task.push(switch_to_default_iframe);
            }
            let tas = fillDataEvent(event);
            task.push.apply(task, tas);
            updateTask(task);
        }
    }
})

// Listening to the Context Menu Clicks.
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.type === "copy_to_clipboard") {
        chrome.storage.sync.get("storagekey", function (result) {
            var array = result["storagekey"];
            var task = { 'task': array };
            let data = yaml.dump(JSON.parse(JSON.stringify(task)));
            let dat = data.replace(reg, '');
            navigator.clipboard.writeText(dat);
        })
    }
    else if (request.type === "download") {
        chrome.storage.sync.get("storagekey", function (result) {
            var array = result["storagekey"];
            chrome.storage.sync.remove("storagekey", () => { });
            var task = { 'task': array };
            let data = yaml.dump(JSON.parse(JSON.stringify(task)));
            let dat = data.replace(reg, '');
            let blob = new Blob([dat], { type: 'application/yaml' });
            let url = URL.createObjectURL(blob);
            var a = document.createElement('a');
            a.href = url;
            a.download = "daksha.yaml";
            a.style.display = 'none';
            document.body.appendChild(a);
            a.click();
            delete a;
        });
    }
    else if (request.type === "pause") {
        var jsonObj = {};
        jsonObj["updateKey"] = true;
        chrome.storage.sync.set(jsonObj, () => {
        });
        pause = true;
    }
    else if (request.type === "start") {
        var jsonObj = {};
        jsonObj["updateKey"] = false;
        chrome.storage.sync.set(jsonObj, () => {
        });
        pause = false;
        updateTask([open_url(request.msg)]);
    }
    else if (request.type === "start_again") {
        chrome.storage.sync.remove("storagekey", () => { });
        chrome.storage.sync.remove("updateKey", () => { });
        prevXPath = "";
        prevDefaultIframe = "";
        defaultIframe = "";
        prevTarelement = null;
        var jsonObj = {};
        jsonObj["updateKey"] = true;
        chrome.storage.sync.set(jsonObj, () => {
        });
        pause = true;
        alert('All your data has been erased , You can now start again!');
    }
    else if (request.type === "resume") {
        var jsonObj = {};
        jsonObj["updateKey"] = false;
        chrome.storage.sync.set(jsonObj, () => {
        });
        pause = false;
    }
    else if (request.type === "stop") {
        var jsonObj = {};
        jsonObj["updateKey"] = true;
        chrome.storage.sync.set(jsonObj, () => {
        });
        pause = true;
    }

    sendResponse({ msg: "All good" });
    return true;
})
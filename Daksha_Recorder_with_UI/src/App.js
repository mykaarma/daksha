/*global chrome*/
import * as React from 'react';
import { useState, useEffect } from 'react';
import Popup from './Components/popup';
import Popup1 from './Components/popup1';
import Popup2 from './Components/popup2';
import Popup3 from './Components/popup3';
let pageNumber;
chrome.storage.sync.get("popupPageNumber", function (result) {
  pageNumber = result["popupPageNumber"] ;
  var dakshaYamlObject = {};
  dakshaYamlObject["popupPageNumber"] = pageNumber;
  chrome.storage.sync.set(dakshaYamlObject, () => {
  });
});

let iconChanger;
chrome.storage.sync.get("playPauseIcon", function (result) {
    iconChanger = result["playPauseIcon"];
});

const MainComponent = () => {

  const [state, setState] = useState(pageNumber);

  useEffect(() => {
    var dakshaYamlObject = {};
    dakshaYamlObject["popupPageNumber"] = state;
    chrome.storage.sync.set(dakshaYamlObject, () => {
    });
  }, [state]);

  const [image, changeImage] = useState(iconChanger);

    useEffect(() => {
        var dakshaYamlObject = {};
        dakshaYamlObject["playPauseIcon"] = image;
        chrome.storage.sync.set(dakshaYamlObject, () => {
        });
    }, [image]);
  
  if (state == 1)
    return (
      <Popup setState={setState} />

    )
  else if (state == 2)
    return (
      <Popup1 setState={setState} image={image} changeImage={changeImage}/>
    )
  else if (state == 3)
    return (
      <Popup2 setState={setState} />
    )
  else if (state == 4)
    return (
      <Popup3 setState={setState} image={image} changeImage={changeImage}/>
    )
};

const App = () => {
  return (
    <MainComponent />
  );
};
export default App;

/*global chrome*/
import * as React from 'react';
import { useState, useEffect } from 'react';
import DakshaRecorderStartingPage from './Components/dakshaRecorderStartingPage';
import DakshaRecorderMainPage from './Components/dakshaRecorderMainPage';
import DakshaRecorderCustomHardwaitPage from './Components/dakshaRecorderCustomHardwaitPage';
import DakshaRecorderEndPage from './Components/dakshaRecorderEndPage';

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
      <DakshaRecorderStartingPage setState={setState} />

    )
  else if (state == 2)
    return (
      <DakshaRecorderMainPage setState={setState} image={image} changeImage={changeImage}/>
    )
  else if (state == 3)
    return (
      <DakshaRecorderCustomHardwaitPage setState={setState} />
    )
  else if (state == 4)
    return (
      <DakshaRecorderEndPage setState={setState} image={image} changeImage={changeImage}/>
    )
};

const App = () => {
  return (
    <MainComponent />
  );
};
export default App;

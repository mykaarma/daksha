/*global chrome*/

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

import * as React from 'react';
import { useState, useEffect } from 'react';
import DakshaRecorderStartingPage from './Components/dakshaRecorderStartingPage';
import DakshaRecorderMainPage from './Components/dakshaRecorderMainPage';
import DakshaRecorderCustomHardwaitPage from './Components/dakshaRecorderCustomHardwaitPage';
import DakshaRecorderEndPage from './Components/dakshaRecorderEndPage';
import GlobalVariables from './Components/globalConfigs';
let dakshaRecorderStartingPage = GlobalVariables.dakshaRecorderStartingPage;
let dakshaRecorderMainPage = GlobalVariables.dakshaRecorderMainPage;
let dakshaRecorderCustomHardwaitPage = GlobalVariables.dakshaRecorderCustomHardwaitPage;
let dakshaRecorderEndPage = GlobalVariables.dakshaRecorderEndPage;
let pageNumber;
chrome.storage.sync.get("popupPageNumber", function (result) {
  pageNumber = result["popupPageNumber"];
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

  if (state == dakshaRecorderStartingPage)
    return (
      <DakshaRecorderStartingPage setState={setState} />

    )
  else if (state == dakshaRecorderMainPage)
    return (
      <DakshaRecorderMainPage setState={setState} image={image} changeImage={changeImage} />
    )
  else if (state == dakshaRecorderCustomHardwaitPage)
    return (
      <DakshaRecorderCustomHardwaitPage setState={setState} />
    )
  else if (state == dakshaRecorderEndPage)
    return (
      <DakshaRecorderEndPage setState={setState} image={image} changeImage={changeImage} />
    )
};

const App = () => {
  return (
    <MainComponent />
  );
};
export default App;

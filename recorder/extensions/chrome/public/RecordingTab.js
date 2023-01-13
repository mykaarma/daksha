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


window.addEventListener("mousedown", (e) => {
    const obj = { x: e.screenX, y: e.screenY, type: 'mousedown' };
    window.parent.postMessage(obj, '*');
});

window.addEventListener("mousemove", (e) => {
    const obj = { x: e.screenX, y: e.screenY, type: 'mousemove' };
    window.parent.postMessage(obj, '*');
})
window.addEventListener("mouseup", (e) => {
    const obj = { x: e.screenX, y: e.screenY, type: 'mouseup' };
    window.parent.postMessage(obj, '*');
})


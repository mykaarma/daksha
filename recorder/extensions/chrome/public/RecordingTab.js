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


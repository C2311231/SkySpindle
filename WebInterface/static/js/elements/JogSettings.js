const SpindleSpeed = document.getElementById('Spindle');
const Feedrate = document.getElementById('Feedrate');

window.spindlespeed = SpindleSpeed.value;
window.feedrate = Feedrate.value;
SpindleSpeed.addEventListener("change", function () {
    window.spindlespeed = SpindleSpeed.value;
});

Feedrate.addEventListener("change", function () {
    window.feedrate = Feedrate.value;
});
const SpindleSpeed = document.getElementById('Spindle');
const Feedrate = document.getElementById('Feedrate');


SpindleSpeed.onchange(function () {
    window.spindlespeed = SpindleSpeed.Value;
});

Feedrate.onchange(function () {
    window.feedrate = Feedrate.Value;
});
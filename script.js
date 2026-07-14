const text = [
    "BCA Student",
    "Learning Web Development",
    "Python Enthusiast",
    "Future Software Developer"
];

let count = 0;
let index = 0;
let currentText = "";
let letter = "";

(function type() {

    if (count === text.length) {
        count = 0;
    }

    currentText = text[count];
    letter = currentText.slice(0, ++index);

    document.getElementById("typing").textContent = letter;

    if (letter.length === currentText.length) {
        count++;
        index = 0;
        setTimeout(type, 1200);
    } else {
        setTimeout(type, 120);
    }

})();

particlesJS("particles-js", {
    particles: {
        number: { value: 80 },
        color: { value: "#38bdf8" },
        shape: { type: "circle" },
        opacity: { value: 0.5 },
        size: { value: 3, random: true },
        line_linked: {
            enable: true,
            distance: 150,
            color: "#38bdf8",
            opacity: 0.3,
            width: 1
        },
        move: {
            enable: true,
            speed: 2
        }
    },
    interactivity: {
        events: {
            onhover: {
                enable: true,
                mode: "repulse"
            }
        }
    },
    retina_detect: true
});
AOS.init({
    duration: 1000,
    once: true
});
const modal = document.getElementById("contactModal");
const btn = document.getElementById("contactBtn");
const close = document.querySelector(".close");

btn.onclick = function(e){
    e.preventDefault();
    modal.style.display = "block";
}

close.onclick = function(){
    modal.style.display = "none";
}

window.onclick = function(e){
    if(e.target == modal){
        modal.style.display = "none";
    }
}
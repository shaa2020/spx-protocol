// demo/cosmic.js
// SPX Protocol Cosmic Dashboard by Shaan (github.com/shaa2020)

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

const stars = [];
const comets = [];

function createStar() {
    const geometry = new THREE.SphereGeometry(0.1, 32, 32);
    const material = new THREE.MeshBasicMaterial({ color: 0xffffff });
    const star = new THREE.Mesh(geometry, material);
    star.position.set(
        Math.random() * 100 - 50,
        Math.random() * 100 - 50,
        Math.random() * 100 - 50
    );
    scene.add(star);
    stars.push(star);
}

function createComet(from, to, color) {
    const material = new THREE.LineBasicMaterial({ color: color });
    const geometry = new THREE.BufferGeometry().setFromPoints([
        new THREE.Vector3(from.x, from.y, from.z),
        new THREE.Vector3(to.x, to.y, to.z)
    ]);
    const comet = new THREE.Line(geometry, material);
    scene.add(comet);
    comets.push(comet);
}

for (let i = 0; i < 10; i++) createStar();
camera.position.z = 50;

function animate() {
    requestAnimationFrame(animate);
    stars.forEach(star => {
        star.rotation.x += 0.01;
        star.rotation.y += 0.01;
    });
    renderer.render(scene, camera);
}
animate();

// Simulate SPX events
setInterval(() => {
    const from = stars[Math.floor(Math.random() * stars.length)].position;
    const to = stars[Math.floor(Math.random() * stars.length)].position;
    createComet(from, to, 0x00ff00);
    document.getElementById("log").innerText = 🌌 Message sent: ${new Date().toLocaleTimeString()};
}, 2000);
import * as THREE from 'https://threejs.org/build/three.module.js';

// Get the canvas element and its dimensions
const canvas = document.querySelector('.webgl');
const canvasWidth = canvas.clientWidth;
const canvasHeight = canvas.clientHeight;

// Create a scene
const scene = new THREE.Scene();

// Create a camera
const camera = new THREE.PerspectiveCamera(75, canvasWidth / canvasHeight, 0.1, 1000);
camera.position.z = 5;

// Create a renderer and add it to the DOM
const renderer = new THREE.WebGLRenderer({ canvas: canvas });
renderer.setSize(canvasWidth, canvasHeight);

// Function to fetch a new object and add it to the scene
function generateObject() {
    fetch('/views/objects3d')
        .then(response => response.json())
        .then(data => {
            // For each object in the data, create a mesh and add it to the scene
            data.forEach(obj => {
                // Create a geometry
                const geometry = obj.shape === 'cube' ? new THREE.BoxGeometry(obj.size, obj.size, obj.size) : new THREE.SphereGeometry(obj.size, 32, 32);

                // Create a material
                const material = new THREE.MeshBasicMaterial({ color: new THREE.Color(obj.color[0] / 255, obj.color[1] / 255, obj.color[2] / 255) });

                // Create a mesh (geometry covered with material)
                const mesh = new THREE.Mesh(geometry, material);

                // Set the position of the mesh
                mesh.position.set(obj.x, obj.y, obj.z);

                // Add the mesh to the scene
                scene.add(mesh);
            });
        })
        .catch(error => console.error('Error:', error));
}

// Add an event listener to the "Generate Object" button
document.getElementById('generate').addEventListener('click', generateObject);

// Animation loop
function animate() {
    requestAnimationFrame(animate);

    // Render the scene with the camera
    renderer.render(scene, camera);
}

// Start the animation loop
animate();
import * as THREE from 'https://threejs.org/build/three.module.js';
// import { FBXLoader } from 'https://threejs.org/examples/jsm/loaders/FBXLoader.js';

// Get the canvas element and its dimensions
const canvas = document.querySelector('.webgl');
const canvasWidth = canvas.clientWidth;
const canvasHeight = canvas.clientHeight;
console.log(`Canvas Width: ${canvasWidth}, Canvas Height: ${canvasHeight}`);

// Create a scene
const scene = new THREE.Scene();

// Create a camera
const camera = new THREE.PerspectiveCamera(75, canvasWidth / canvasHeight, 0.1, 1000);
camera.position.z = 5;

// Create a renderer and add it to the DOM
const renderer = new THREE.WebGLRenderer({ canvas: canvas });
renderer.setSize(canvasWidth, canvasHeight);

// Enable shadows in the renderer
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap; // default THREE.PCFShadowMap

// Create a point light and add it to the scene
const pointLight = new THREE.PointLight(0xffffff, 1, 100);
pointLight.position.set(0, 0, 1);

// Enable shadows for the light
pointLight.castShadow = true;

scene.add(pointLight);

// Create an array to store the meshes
const meshes = [];

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
                mesh.position.set(
                    obj.x + (Math.random() - 0.5) * 10, // Random x position
                    obj.y + (Math.random() - 0.5) * 10, // Random y position
                    obj.z + (Math.random() - 0.5) * 10  // Random z position
                );

                // Add the rotation speed to the mesh
                mesh.rotationSpeed = new THREE.Vector3(obj.rotation[0], obj.rotation[1], obj.rotation[2]);

                // Add the mesh to the scene
                scene.add(mesh);

                // Add the mesh to the array
                meshes.push(mesh);
            });
        })
        .catch(error => console.error('Error:', error));
}

// Add an event listener to the "Generate Object" button
document.getElementById('generate').addEventListener('click', generateObject);

// Animation loop
function animate() {
    requestAnimationFrame(animate);

    // Rotate each mesh
    meshes.forEach(mesh => {
        mesh.rotation.x += mesh.rotationSpeed.x;
        mesh.rotation.y += mesh.rotationSpeed.y;
        mesh.rotation.z += mesh.rotationSpeed.z;
    });

    // Render the scene with the camera
    renderer.render(scene, camera);
}

// Start the animation loop
animate();

// Make the generateObject function accessible from the global scope
window.generateObject = generateObject;


///////// CLEAR CANVAS

function clearCanvas() {
    // Remove all meshes from the scene
    for (let i = scene.children.length - 1; i >= 0; i--) {
        const object = scene.children[i];
        if (object instanceof THREE.Mesh) {
            scene.remove(object);
        }
    }

    // Clear the meshes array
    meshes.length = 0;
}

document.getElementById('clear').addEventListener('click', clearCanvas);
window.clearCanvas = clearCanvas;





///////// CAPUTE IMAGE

function captureImage() {
    // Render the scene first to ensure it's up to date
    renderer.render(scene, camera);

    // Get the image data URL from the canvas
    var imgData = renderer.domElement.toDataURL("image/png");

    // Generate a random 10-digit number
    var randomNumber = Math.floor(Math.random() * 1e10);

    // Create a link element
    var link = document.createElement('a');

    // Set the link's href to image data URL
    link.href = imgData;

    // Set the download attribute of the link to the random number
    link.download = randomNumber + '.png';

    // Trigger a click event on the link to start the download
    link.click();
}

// Add an event listener to the "Capture Image" button
document.getElementById('capture').addEventListener('click', captureImage);

// Make the captureImage function accessible from the global scope
window.captureImage = captureImage;




// /////// RUN LOOPS TO SAVE IMAGES

// async function runLoops() {
//     // Prompt the user for the number of loops
//     const numLoops = 4150
    
//     // Run the loop
//     for (let i = 0; i < numLoops; i++) {
//         // Generate a random number between 1 and 4
//         const numObjects = Math.floor(Math.random() * 40) + 1;

//         // Call generateObject a random number of times
//         for (let j = 0; j < numObjects; j++) {
//             generateObject();
//         }

//         // Wait for 2 seconds before capturing the image
//         await new Promise(resolve => setTimeout(resolve, 500));

//         // Call captureImage and clearCanvas
//         captureImage();
//         clearCanvas();
//         console.log(`Loop ${i + 1} of ${numLoops} complete`);
//     }
// }

// // Add an event listener to the "Run Loops" button
// document.getElementById('runLoops').addEventListener('click', runLoops);

// // Make the runLoops function accessible from the global scope
// window.runLoops = runLoops;


/////
fetch('/run_test', {
    method: 'POST',
  })
  .then(response => response.text())
  .then(data => {
    // Print the result
    console.log(data);
    // And display it in your frontend, e.g., in a div with id 'result'
    document.getElementById('model_result').textContent = data;
  })
  .catch((error) => {
    console.error('Error:', error);
  });
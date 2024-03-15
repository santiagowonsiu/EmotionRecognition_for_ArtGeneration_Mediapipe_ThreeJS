1. (REQUIRED) Initialize

- Installations (from the package.json and requirements.txt)

  - npm install
  - pip install -r requirements.txt

- Initialize web app: python.app.py

- Remember to go to http://127.0.0.1:5000/views/ as the “/views” blueprint is being used

- Remember to add the "cut_model": folder that wasn't possible to upload in the GitHub. Test.py was uploaded to the repo but actually should be inside "cut_model" folder


2. (REQUIRED) Functions that require “path” updating for them to work in the Views.py file 

- /run_test
- /latest_Fake1
- /latest_Capture
- /latest_Landscape


3. (SHOULD READ) I am still having trouble to initialise the client, sometimes:


a) it usually take a 1-2 of times of debugging before the project actually works

b) before opening http://127.0.0.1:5000/views/, Wait for the terminal to print:
 * Debugger is active!
 * Debugger PIN: 986-931-929 

c) if trying to reload it was working and now it is not, go to the terminal and kill all process in port 500
	First type loss -I:5000
	Second type kill NumberOfThePRocess (do so por as many current processes)
	Third make sure you killed them while http://127.0.0.1:5000/views/ was not open

d) restarting the computer once should also work to try again



4. (OPTIONAL TO READ) Other important tips regarding the GAN important routes:

- Where is the trained model stored: ./checkpoints/cat2dog_cut_pretrained/latest_net_G.pth”

- Where should be the 1 input image of 3D Image Captures to run the GAN be: “./cut_master/datasets/afhq/cat2dog/TestA”

- Where should be the 1 input image of the Landscape to run the GAN be: “./cut_master/datasets/afhq/cat2dog/TestA”


5. (OPTIONAL TO READ) Files Glossary (as guidance)

- Views.py and app.py contain the main backend code

- Socketio_instance.py initializes SocketIO

- Cut_master folder contains the CUT GAN Model repository. Inside the main python code is contained in test.py as well as the Landscapes datasets (inside grumpifycat/Dataset – Landscapes folder) as well as the folders where input images for inference will be required

- Body_language.pkl is the pre-trained model I made with Media Pipe for Happy-Sad pose classification

- Checkpoints is the folder to store the GAN model I trained: /cat2dog_cut_pretrained/latest_net_G.pth

- The folders that are required for the GAN to store and find the root to display images in the website are: gen_image_png, gen_image_display, landscape_image, capture_image

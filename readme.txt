Abstract

This project explores the integration of pose classification, 3D environments, and deep learning in image generation with the aim of eventually being able to convey into a more matured solution that enables personal growth tools through art and technology.

The project’s trajectory includes tools like Google’s MediaPipe for pose classification, and Generative Adversarial Networks for image transformation, specifically Contrastive Unpaired Translation (CUT), CycleGAN and pix2pix models.

The system's architecture combines front-end interactions with Three.js and a Flask-powered backend, covering the user journey from pose recognition to image generation. Challenges in server setup led to a deep dive into HTTP protocols. OpenCV is integrated for real-time camera functionality, seamlessly capturing user poses for recognition and image generation.

In the end, a GAN (Generative Adversarial Network) was added, and it made the project better and took it further than what was first planned. Training this model with pictures of landscapes and 3D objects helped it learn to create images, but it wasn’t easy to adapt the model to run in a web-based system. Getting the GAN to work just right involved careful changes, like understanding in depth the relationships between the different functions.

For the future, there's a chance to make the system better by having it recognize more kinds of poses, improving the GAN’s training images, and making it smart enough to generate 3D objects that change based on what it “sees”.

This project is a first step towards using AI and 3D tech to make personal growth and emotion awareness more fun and engaging. However, it could also end up developing towards developing tools for inclusive art creation.




1. (REQUIRED) Initialize

- Installations (from the package.json and requirements.txt)

  - npm install
  - pip install -r requirements.txt

- Initialize web app: python.app.py

- Remember to go to http://127.0.0.1:5000/views/ as the “/views” blueprint is being used

- Remember to add the "cut_model": folder that wasn't possible to upload in the GitHub. Test.py was uploaded to the repo but actually should be inside "cut_model" folder: https://www.dropbox.com/scl/fo/8l8qsdk3x8rsyogvwyx62/h?rlkey=qqsu11pfmoy3ekqjuogoh3w87&dl=0



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


4. (DEMO VIDEO) https://www.dropbox.com/scl/fi/igivhpog47i3axdqne3y8/Screen-Recording-2024-03-14-at-17.25.36.mov?rlkey=nnuvuf3ouq68vnzacf2nhf7t2&dl=0

5. (OPTIONAL TO READ) Other important tips regarding the GAN important routes:

- Where is the trained model stored: ./checkpoints/cat2dog_cut_pretrained/latest_net_G.pth”

- Where should be the 1 input image of 3D Image Captures to run the GAN be: “./cut_master/datasets/afhq/cat2dog/TestA”

- Where should be the 1 input image of the Landscape to run the GAN be: “./cut_master/datasets/afhq/cat2dog/TestA”


6. (OPTIONAL TO READ) Files Glossary (as guidance)

- Views.py and app.py contain the main backend code

- Socketio_instance.py initializes SocketIO

- Cut_master folder contains the CUT GAN Model repository. Inside the main python code is contained in test.py as well as the Landscapes datasets (inside grumpifycat/Dataset – Landscapes folder) as well as the folders where input images for inference will be required

- Body_language.pkl is the pre-trained model I made with Media Pipe for Happy-Sad pose classification

- Checkpoints is the folder to store the GAN model I trained: /cat2dog_cut_pretrained/latest_net_G.pth

- The folders that are required for the GAN to store and find the root to display images in the website are: gen_image_png, gen_image_display, landscape_image, capture_image

7. REFERENCES

Renotte, N., 2021. Body Language Decoder. [Online]
Available at: https://github.com/nicknochnack/Body-Language-Decoder
Taesung Park, A. A. E. R. Z. J.-Y. Z., 2020. Contrastive Learning for Unpaired Image-to-Image Translation. [Online]
Available at: https://arxiv.org/pdf/2007.15651.pdf
Park, T., 2021. [Online]
Available at: https://github.com/taesungp/contrastive-unpaired-translation
Phillip Isola, J.-Y. Z. T. Z. A. A. E., 2017. Image-to-Image Translation with Conditional Adversarial Nets. [Online]
Available at: https://phillipi.github.io/pix2pix/
Jun-Yan Zhu*, T. P. P. I. A. A. E., 2017. Unpaired Image-to-Image Translation using Cycle-Consistent Adversarial Networks. [Online]
Available at: https://junyanz.github.io/CycleGAN/
Rougetet, A., n.d. Landscape Pictures Dataset. [Online]
Available at: https://www.kaggle.com/datasets/arnaud58/landscape-pictures

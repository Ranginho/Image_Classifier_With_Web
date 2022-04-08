## PROJECT:
I needed to create a simple web-page, where user can upload any number of photos and after clicking on button 'predict' user will see all photos with predictions. Prediction is just classifing images in five classes: 1. Image contains TV 2.Image contains Laptop 3.Image contains Mobile 4.Image contains Camera. 5. Image doesn't contain any of these four classes(TV, Laptop, Mobile, Camera).

## FILES & DESCRIPTION: 
There is ipynb notebook in folder 'model' where you can see how I trained model, it has comments and I hope everything is clear. Also we have h5 files there and it is neccessary to deploy project. The main.py file is in 'app' folder named 'web_part'. You can see there whole pythonic code with comments. There is html file in 'templates' folder and in static folder you can see css file and uploads folder, uploads folder is needed for save uploaded images, then model reads images from that file and makes predictions.

## RUN:
If you are in app directory(there are folders static, templates and file web_part) you can write 'python web_part.py' in your cmd and it will automatically open browser, project will be deployed on 'localhost:3000' but you can change it from 'web_part.py' file on line 89. You can upload any number of images(only 'jpg' and 'png' format) and after clicking on 'predict' button you will see results. After you  have finished using this project, you can close your tab in browser and quit from your cmd(ctrl + c).

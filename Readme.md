# How to run the application
Using cmd, inside the project directory, follow these steps

## 1.Dependecies installation
    py -m pip install flask
    py -m pip install pandas[excel]
    py -m pip install dlib
    py -m pip install Pillow
    py -m pip install requests

## 2.Edit IPWebcam config.json IPAdress attribute

## 3.Run the application
    py app.py

## Using command lines declaration
    ...\custom_lipstick_machine_app>py app.py

## Application terminatation
    ctrl + c

# Load application page on desktop
Running the application shows an IP adresses on cmd which you can use to load the application page 

# Load application page on phone
Before running the application you should

## 1.install IPWebcam application on your phone

## 2.Set phone camera options
Open the app, go to the video preferences to set the **Main camera** and the **Video orintation** options to the following:<br></br>
- If you set the **Main camera** to the **Front camera**, then the **Video orintation** has to be set to **Upside Down Portrait**<br></br>
- If you set the **Main camera** to the **Primary camera**, then the **Video orintation** has to be set to **Portrait**<br></br>

## 3.IPWebcam start server
Choose **Start server** option

## 4.Edit IPWebcam url
Change the url variable in the app.py file into the IPWebcam previewed IPAdresses
### For example:
- IPWebcam adress: -.-.1.10:8080
### Then the url variable in the app.py should be:
- url = "http://-.-.1.10:8080/shot.jpg"

## 5.Run IPWebcam in background
Choose **Run in background** option from the Actions tab on the previewed page

##Building server output file:
    1. cd server
    2. make compile
    3. make run PORT=[Port Number]
        1. *e.g make run PORT=1234*

##Starting GUI
    1. cd client
    2. python3 main.py

##Justifications:
    1. I chose to use matplotlib instead of pyqtgraph because it has more robust features and graph exporting is higher quality
    2. I chose fpdf instead of PyPDF2 because formatting was better. Additionally, fpdf didn't require me to concatenate multiple pdf's.
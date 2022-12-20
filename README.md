Building server output file:
    1) make compile
    2) make run PORT=[Port Number]
        - e.g make run PORT=65432

Starting GUI
    1) python3 main.py
        - Note: GUI inputs validate against expected value types

Justifications:
    1) I chose to use matplotlib instead of pyqtgraph because it has more robust features and graph exporting is higher quality
    
    2) I chose fpdf instead of PyPDF2 because formatting was better and didn't require me to concatenate multiple pdf's. I could just place to png to the pdf.

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.pagesizes import portrait
from reportlab.lib.units import inch
from reportlab.lib.colors import white, red, darkred, black
import os

class PDF_Gen:
    def __init__(self):
        pass
    def create_awards(self,awards, folder, tournament, team_pic=None):
        print("Awards accepted.")
        award_count = 0
        pdf_file_name = tournament.replace("/", "-")
        folder = f"{folder}/{pdf_file_name}.pdf"
        pdf = canvas.Canvas(folder, pagesize=portrait(letter))

        ix_pos = 0
        iy_pos = 0
        xpos = 88
        first_ypos = 320
        last_ypos = 295
        event_ypos = 250
        place_ypos = 70

        gold = '.\\images\\gold.jpg'
        silver = '.\\images\\silver.jpg'
        bronze = '.\\images\\bronze.jpg'
        print("Cycling through awards.")
        for award in awards:
            print("Making award...")
            # Assign the proper image for this award
            if int(award.place) == 1:
                image = gold
            elif int(award.place) == 2:
                image = silver
            else:
                image = bronze
            print(f"{image}  is a good path: {os.path.isfile(image)}")

            # Insert the image
            print(f"Image: {image}, X: {ix_pos}, Y: {iy_pos}")

            pdf.drawImage(image, ix_pos, iy_pos)

            print("Image drawn.")
            # Set the font size for names
            name_font = 24

            # Check the length of the strings to see if the font size needs to change.
            if len(award.first) or len(award.last) > 9:
                name_font = 18

            event_font = 44 - 2.3 * len(award.event)

            print("Inserting Text...")
            # Insert the text
            pdf.setFont('Courier', name_font, leading=None)
            pdf.drawCentredString(xpos + ix_pos, first_ypos + iy_pos, award.first)
            pdf.drawCentredString(xpos + ix_pos, last_ypos + iy_pos, award.last)
            pdf.setFont('Courier', event_font, leading=None)
            pdf.drawCentredString(xpos + ix_pos, event_ypos + iy_pos, award.event)
            pdf.setFont('Courier', 60, leading=None)
            pdf.drawCentredString(xpos + ix_pos, place_ypos + iy_pos, award.place)

            award_count += 1
            ix_pos += 200

            if award_count == 3:
                iy_pos += 400
                ix_pos = 0
            if award_count > 5:
                award_count = 0
                ix_pos = 0
                iy_pos = 0
                pdf.showPage()
            print("Award Made")
        print("showing page")
        pdf.showPage()

        print("Skip team picture")
        if team_pic is not None:
            self.team_picture(pdf, tournament, team_pic)

        print("Save pdf")
        try:
            pdf.save()
        except Exception as e:
            print(f"Error saving file: {e}")
        print("Saved - carry on. ")
    def team_picture(self,pdf, tournament, team_pic):

        team_name = 'Osage City High School'
        center_pic_x = 4.5 * inch
        tn_y = 4.25 * inch
        tourn_y = 1.25 * inch
        pdf.drawImage(team_pic, inch, inch, 7 * inch, 4 * inch)
        pdf.setFont('Courier', 32)
        pdf.drawCentredString(center_pic_x, tn_y, team_name)
        pdf.setFillColor(white)
        pdf.drawCentredString(center_pic_x, tourn_y, tournament)
        pdf.showPage()
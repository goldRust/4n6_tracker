
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.pagesizes import portrait
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import Table, SimpleDocTemplate, TableStyle, Paragraph
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

        ix_pos = 12
        iy_pos = 20
        xpos = .75 * inch
        first_ypos = 2.6 * inch
        last_ypos = 2.35 * inch
        event_ypos = 2 * inch
        place_ypos = .5 * inch

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
            pdf.drawImage(image, ix_pos, iy_pos, width=1.5 * inch, height=3 * inch)

            # Set the font size for names
            name_font = 24

            # Check the length of the strings to see if the font size needs to change.
            if len(award.first) or len(award.last) > 8:
                name_font = 16
            if len(award.first) or len(award.last)>10:
                name_font = 14

            event_font = 28 - 2.3 * len(award.event)

            # Insert the text
            pdf.setFont('Times-Roman', name_font, leading=None)
            pdf.drawCentredString(xpos + ix_pos, first_ypos + iy_pos, award.first)
            pdf.drawCentredString(xpos + ix_pos, last_ypos + iy_pos, award.last)
            pdf.setFont('Times-Roman', event_font, leading=None)
            pdf.drawCentredString(xpos + ix_pos, event_ypos + iy_pos, award.event)
            pdf.setFont('Times-Roman', 60, leading=None)
            pdf.drawCentredString(xpos + ix_pos, place_ypos + iy_pos, award.place)

            award_count += 1
            ix_pos += 150

            if award_count == 4 or award_count == 8:
                iy_pos += 3 * inch + 10
                ix_pos = 12
            if award_count > 11:
                award_count = 0
                ix_pos = 12
                iy_pos = 20
                pdf.showPage()
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

    def team_report(self, team, folder):
        file_name = f"{folder}/{team.name}-Season_Report.pdf"
        pdf = SimpleDocTemplate(file_name, pagesize=letter)
        data = [["Student","Tournaments","Events"]]
        for student in team.students:
            row = [student.full_name]
            tournaments = ""
            events = ""
            for perf in student.performances:
                if str(perf.tournament) not in tournaments:
                    tournaments += f"{str(perf.tournament)}\n"
                if perf.event not in events:
                    events += f"{perf.event}, "
            row.append(tournaments)
            row.append(events)
            data.append(row)

        all_items = []
        all_items.append(Paragraph(f"{team.name} Full Season Report\n\n"))



        t_style = TableStyle(
    [('LINEABOVE', (0,0), (-1,0), 2, colors.green),
    ('LINEABOVE', (0,1), (-1,-1), 0.25, colors.black),
    ('LINEBELOW', (0,-1), (-1,-1), 2, colors.green),
    ('ALIGN', (1,1), (-1,-1), 'RIGHT'),]
    )
        print("Style set.")
        #t_style.add('INNERGRID', (0,0), (-1,-1), 0.25, colors.black)
        print("Grid Added")
        table = Table(data)
        print("Setting the style.")
        table.setStyle(t_style)
        print("Style set.")

        all_items.append(table)
        print("Table Appeneded")
        pdf.build(all_items)
        print("Done")



    def student_report(self, student, folder):
        pdf = canvas.Canvas(folder, pagesize=portrait(letter))

    def tournament_report(self, tournament, folder):
        pdf = canvas.Canvas(folder, pagesize=portrait(letter))
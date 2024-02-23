
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.pagesizes import portrait
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import Table, SimpleDocTemplate, TableStyle, Paragraph
import os
from PIL import Image
import numpy as np

class PDF_Gen:
    def __init__(self):
        pass
    def create_awards(self,awards, folder, tournament, team, team_pic=None):
        self.team = team
        award_count = 0
        pdf_file_name = tournament.replace("/", "-")
        folder = f"{folder}/Awards for {pdf_file_name}.pdf"
        pdf = canvas.Canvas(folder, pagesize=portrait(letter))

        ix_pos = 12
        iy_pos = 20
        xpos = .75 * inch
        first_ypos = 2.6 * inch
        last_ypos = 2.35 * inch
        event_ypos = 2 * inch
        place_ypos = .5 * inch

        gold = './images/gold.jpg'
        silver = './images/silver.jpg'
        bronze = './images/bronze.jpg'

        for award in awards:

            # Assign the proper image for this award
            if int(award.place) == 1:
                image = gold
            elif int(award.place) == 2:
                image = silver
            else:
                image = bronze


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


        if team_pic is not None:
            self.team_picture(pdf, tournament, team_pic)


        try:
            pdf.save()
        except Exception as e:
            print(e)

    def team_picture(self,pdf, tournament, team_pic):

        # The plan is to load the image as an Image file, find the correct pixels for the top and bottom text, then pick white for dark colors and white for light ones.
        # This proves to be rather difficult. Looking for a new library to do so.

        team_pic = team_pic
        team_name = self.team.name
        center_pic_x = 4.5 * inch
        tn_y = 5.75 * inch
        tourn_y = 1.5 * inch


        pdf.drawImage(team_pic, inch, inch, 7 * inch, 5.27* inch)
        pdf.setFont('Courier', 32)
        pdf.setFillColor(colors.black)
        pdf.drawCentredString(center_pic_x, tn_y, team_name)
        pdf.setFillColor(colors.white)
        max_font = 48 - len(tournament)
        if max_font > 34:
            max_font = 34
        pdf.setFont('Courier', max_font)
        pdf.drawCentredString(center_pic_x, tourn_y, tournament)
        pdf.showPage()

    def team_report(self, team, folder):
        file_name = f"{folder}/{team.name}-Season_Report.pdf"
        pdf = SimpleDocTemplate(file_name, pagesize=letter)
        data = [["Student","Tournaments","Events"]]
        empty = [[" ", " ", " "]]
        empty_table = Table(empty)
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


        all_items.append(Paragraph(f"<font size=16>{team.name} Full Season Report</font>"))

        all_items.append((empty_table))



        t_style = TableStyle(
    [('LINEABOVE', (0,0), (-1,0), 2, colors.crimson),
    ('LINEABOVE', (0,1), (-1,-1), 0.25, colors.black),
    ('LINEBELOW', (0,-1), (-1,-1), 2, colors.crimson),
    ('ALIGN', (1,1), (-1,-1), 'LEFT'),]
    )

        t_style.add('INNERGRID', (0,0), (-1,-1), 0.25, colors.black)
        table = Table(data)
        table.setStyle(t_style)
        all_items.append(table)
        pdf.build(all_items)


    def student_report(self, student, folder):
        file_name = f"{folder}/{student.full_name}-Season_Report.pdf"
        pdf = SimpleDocTemplate(file_name, pagesize=letter)
        data = [["Event", "Rank", "Tournament"]]
        empty = [[" ", " ", " "]]
        empty_table = Table(empty)
        for performance in student.performances:
            placement = performance.placement
            if placement == "100":
                placement = "Unranked"
            row = [performance.event,placement,str(performance.tournament)]
            data.append(row)

        all_items = []
        all_items.append(Paragraph(f"<font size=16>{student.full_name} Full Season Report</font>"))

        all_items.append((empty_table))

        t_style = TableStyle(
            [('LINEABOVE', (0, 0), (-1, 0), 2, colors.crimson),
             ('LINEABOVE', (0, 1), (-1, -1), 0.25, colors.black),
             ('LINEBELOW', (0, -1), (-1, -1), 2, colors.crimson),
             ('ALIGN', (1, 1), (-1, -1), 'RIGHT'), ]
        )

        t_style.add('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black)
        table = Table(data)
        table.setStyle(t_style)
        all_items.append(table)
        pdf.build(all_items)

    def tournament_report(self, team, tournament, folder):
        file_name = f"{folder}/{tournament.school}_Report.pdf"
        pdf = SimpleDocTemplate(file_name, pagesize=letter)
        data = [["Student","Event", "Rank"]]
        empty = [[" ", " ", " "]]
        empty_table = Table(empty)
        partner_performances = []
        for student in team.students:
            for performance in student.performances:
                name = student.full_name
                if performance.tournament != tournament:
                    continue
                if performance.partner:
                    perf_found = False
                    for perf in partner_performances:
                        if perf.partner == student:
                            perf_found = True
                    if perf_found:
                        continue
                    partner_performances.append(performance)
                    name = name + " & " + performance.partner.full_name

                placement = performance.placement
                if int(placement) > 10:
                    placement = "Unranked"
                if performance.tournament == tournament:
                    row = [name, performance.event, placement]
                    data.append(row)

        all_items = []
        all_items.append(Paragraph(f"<font size=16>{tournament} Report</font>"))

        all_items.append((empty_table))

        t_style = TableStyle(
            [('LINEABOVE', (0, 0), (-1, 0), 2, colors.crimson),
             ('LINEABOVE', (0, 1), (-1, -1), 0.25, colors.black),
             ('LINEBELOW', (0, -1), (-1, -1), 2, colors.crimson),
             ('ALIGN', (1, 1), (-1, -1), 'RIGHT'), ]
        )
        t_style.add('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black)
        table = Table(data)
        table.setStyle(t_style)
        all_items.append(table)
        pdf.build(all_items)

    def event_report(self, team, event, folder):
        file_name = f"{folder}/{event}_Report.pdf"
        pdf = SimpleDocTemplate(file_name, pagesize=letter)
        data = [["Student", "Rank", "Tournament"]]
        empty = [[" ", " ", " "]]
        empty_table = Table(empty)
        for student in team.students:
            for performance in student.performances:
                if performance.event == event:

                    row = [student.full_name, performance.placement, str(performance.tournament)]
                    data.append(row)

        all_items = []
        all_items.append(Paragraph(f"<font size=16>{event} Report</font>"))

        all_items.append((empty_table))

        t_style = TableStyle(
            [('LINEABOVE', (0, 0), (-1, 0), 2, colors.crimson),
             ('LINEABOVE', (0, 1), (-1, -1), 0.25, colors.black),
             ('LINEBELOW', (0, -1), (-1, -1), 2, colors.crimson),
             ('ALIGN', (1, 1), (-1, -1), 'RIGHT'), ]
        )

        t_style.add('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black)
        table = Table(data)
        table.setStyle(t_style)
        all_items.append(table)
        pdf.build(all_items)

    def state_qualifier_report(self, team, folder):
        file_name = f"{folder}/{team.name}_State_Qualifier_Report.pdf"
        pdf = SimpleDocTemplate(file_name, pagesize=letter)
        data = [["Student","Event", "Rank", "Tournament"]]
        empty = [[" ", " ", " "," "]]
        empty_table = Table(empty)

        try:
            for student in team.students:

                for performance in student.performances:
                    if performance.qualifier:
                        if "Champ" in performance.qualifier:
                            row = [student.full_name,performance.event , performance.placement, str(performance.tournament)]
                            data.append(row)


            all_items = []
            all_items.append(Paragraph(f"<font size=16>{team.name} State Qualifier Report</font>"))

            all_items.append((empty_table))

            t_style = TableStyle(
                [('LINEABOVE', (0, 0), (-1, 0), 2, colors.crimson),
                 ('LINEABOVE', (0, 1), (-1, -1), 0.25, colors.black),
                 ('LINEBELOW', (0, -1), (-1, -1), 2, colors.crimson),
                 ('ALIGN', (1, 1), (-1, -1), 'RIGHT'), ]
            )

            t_style.add('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black)
            table = Table(data)
            table.setStyle(t_style)
            all_items.append(table)
            pdf.build(all_items)
        except Exception as e:
            print(e)
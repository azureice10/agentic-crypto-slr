"""Render the supplied reporting map; no independent PRISMA certification."""
from pathlib import Path
import re
from html import escape
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, LongTable, TableStyle

ROOT=Path(__file__).resolve().parent.parent


def main():
    source=ROOT/'protocol/prisma_checklist.md'
    dest=ROOT/'protocol/prisma_checklist.pdf'
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='MapBody',fontName='Helvetica',fontSize=8.7,leading=11,spaceAfter=6,textColor=colors.HexColor('#263445')))
    styles.add(ParagraphStyle(name='MapCell',fontName='Helvetica',fontSize=8,leading=10.2,textColor=colors.HexColor('#263445')))
    styles.add(ParagraphStyle(name='MapHeading',fontName='Helvetica-Bold',fontSize=11.5,leading=14,spaceBefore=10,spaceAfter=6,keepWithNext=True,textColor=colors.HexColor('#17385B')))
    story=[];table_rows=[]
    def flush():
        nonlocal table_rows
        if not table_rows:return
        rows=[[Paragraph(escape(x),styles['MapCell']) for x in row] for row in table_rows]
        table=LongTable(rows,colWidths=[125,386],repeatRows=1,hAlign='LEFT')
        table.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#E7EEF6')),
            ('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),
            ('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),5),
            ('BOTTOMPADDING',(0,0),(-1,-1),5),('LINEBELOW',(0,0),(-1,0),.6,colors.HexColor('#47617B')),
            ('LINEBELOW',(0,1),(-1,-1),.25,colors.HexColor('#D5DDE5')),
        ]))
        story.extend([table,Spacer(1,7)]);table_rows=[]
    for line in source.read_text(encoding='utf-8').splitlines():
        if line.startswith('|'):
            if re.fullmatch(r'[| :\-]+',line):continue
            table_rows.append([x.strip() for x in line.strip('|').split('|')]);continue
        flush()
        if not line.strip():continue
        if line.startswith('# '):story.append(Paragraph(escape(line[2:]),styles['Title']))
        elif line.startswith('## '):story.append(Paragraph(escape(line[3:]),styles['MapHeading']))
        else:story.append(Paragraph(escape(line),styles['MapBody']))
    flush()
    def footer(canvas,doc):
        canvas.setStrokeColor(colors.HexColor('#D5DDE5'));canvas.line(42,35,553,35)
        canvas.setFont('Helvetica',8);canvas.setFillColor(colors.HexColor('#47617B'))
        canvas.drawString(42,23,'SLR reporting map | release 3.6.3 / manuscript CS1 | unchanged data')
        canvas.drawRightString(553,23,str(doc.page))
    doc=SimpleDocTemplate(str(dest),pagesize=A4,leftMargin=42,rightMargin=42,topMargin=38,bottomMargin=48,
                          title='PRISMA reporting and availability map - release 3.6.3 / CS1',author='SLR supplementary package')
    doc.build(story,onFirstPage=footer,onLaterPages=footer)
    print(dest)


if __name__=='__main__':main()

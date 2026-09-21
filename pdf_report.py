from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from datetime import datetime
from typing import List, Dict, Any

def generate_pdf_report(file_name: str, event_logs_data: List[Dict[str, Any]], tanks_data: List[Dict[str, Any]]) -> None:
  """
  Generates a PDF report summarizing the farm's health digest, including biomass,
  critical hazards, and tank details.

  Args:
    file_name (str): The base name for the PDF file.
    event_logs_data (List[Dict[str, Any]]): List of dictionaries representing event logs.
    tanks_data (List[Dict[str, Any]]): List of dictionaries representing tank data.
  """
  doc_path: str = f"{file_name}.pdf"
  doc = SimpleDocTemplate(doc_path, pagesize= letter)
  story: List[Any] = []
  total_biomass_count: float = 0.0
  critical_count: int = 0

  styles = getSampleStyleSheet()
  title_style: ParagraphStyle = styles["Heading1"]
  normal_style: ParagraphStyle = styles["Normal"]

  title = Paragraph(f"<b>Yaro Smart Farm Enterprises. Daily Health Digest</b>", title_style)
  date_str = Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", normal_style)
  story.append(title)
  story.append(date_str)
  story.append(Spacer(1, 5))

  for tank_info in tanks_data:
      total_biomass_count += tank_info.get('total_biomass_kg', 0.0)

  for log in event_logs_data:
    if log.get('status') == 'Critical':
      critical_count += 1

  summary_text = Paragraph(
      f"<b>Total Live biomass:</b> {total_biomass_count:,.2f} kg | <b>Active Critical Hazards:</b> <font color= 'red'> {critical_count}</font>",
      normal_style
  )
  story.append(summary_text)
  story.append(Spacer(1, 15))

  table_data: List[List[Any]] = [
      ['Tank ID', 'Batch ID', 'Total Biomass (kg)', 'Daily Feed (kg)', 'Ammonia (ppm)', 'pH', 'Temperature']
  ]
  for tank_info in tanks_data:
      table_data.append(
          [
              tank_info.get('tank_id'),
              tank_info.get('batch_id'),
              f"{tank_info.get('total_biomass_kg', 0.0):.2f}",
              f"{tank_info.get('daily_feed_kg', 0.0):.2f}",
              tank_info.get('ammonia_ppm'),
              tank_info.get('ph'),
              tank_info.get('temp_c')
          ]
      )

  if len(table_data) > 1:
    table = Table(table_data)
    table.setStyle(TableStyle(
        [
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]
    ))
    story.append(table)
    story.append(Spacer(1, 15))

  doc.build(story)
  print(f"PDF Daily Digest successfully generated at '{doc_path}'!")

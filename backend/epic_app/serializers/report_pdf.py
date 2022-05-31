from io import BytesIO
from typing import Any, List

from reportlab.graphics import renderPDF
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.shapes import Drawing
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm, inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from reportlab.rl_config import defaultPageSize


class EpicPdfReport:
    # Create the PDF object, using the buffer as its "file."
    PAGE_HEIGHT = defaultPageSize[1]
    PAGE_WIDTH = defaultPageSize[0]
    styles = getSampleStyleSheet()
    Title = "Epic Report"
    pageinfo = "Epic Report"

    def myFirstPage(self, canvas, doc):
        canvas.saveState()
        canvas.setFont("Times-Bold", 16)
        canvas.drawCentredString(
            self.PAGE_WIDTH / 2.0, self.PAGE_HEIGHT - 108, self.Title
        )
        canvas.setFont("Times-Roman", 9)
        canvas.drawString(inch, 0.75 * inch, "First Page / %s" % self.pageinfo)
        canvas.restoreState()

    def myLaterPages(self, canvas, doc):
        canvas.saveState()
        canvas.setFont("Times-Roman", 9)
        canvas.drawString(inch, 0.75 * inch, "Page %d %s" % (doc.page, self.pageinfo))
        canvas.restoreState()

    def _draw_charts(self, input_data) -> Drawing:
        drawing = Drawing(400, 200)
        id_keys = [id_k for id_k in input_data.keys() if not "_justify" in str(id_k)]
        if not id_keys:
            return
        id_values = [input_data[id_k] for id_k in id_keys]

        bc = VerticalBarChart()
        bc.x = 50
        bc.y = 50
        bc.height = 125
        bc.width = 300
        bc.data = [id_values]
        # bc.strokeColor = colors.black
        bc.valueAxis.valueMin = 0
        bc.valueAxis.valueMax = sum(id_values)
        bc.valueAxis.valueStep = 1
        #
        bc.categoryAxis.categoryNames = list(map(str, id_keys))
        drawing.add(bc)
        return drawing

    def _add_line(self, line: str, flowables: List[Any]):
        style = self.styles["Normal"]
        flowables.append(Paragraph(line, style))
        flowables.append(Spacer(1, 0.2 * inch))

    def _report_justify(self, q_qa: dict, flowables: List[Any]):
        q_summary = q_qa["summary"]
        if not q_qa["answers"]:
            self._add_line("No recorded answers.", flowables)
            return

        for k_j in q_summary.keys():
            if "justify" not in str(k_j):
                continue
            "Justify {}:".format(str(k_j).split("_")[0])
            for line in q_summary[k_j]:
                self._add_line(line, flowables)

    def _append_questions(self, report_data: dict, flowables: List[Any]):
        for p_entry in report_data:
            program_name = p_entry["name"]
            self._add_line(f"Program: {program_name}", flowables)
            for q_entry in p_entry["questions"]:
                q_summary = q_entry["question_answers"]["summary"]
                q_title = q_entry["title"]
                self._add_line(q_title, flowables)
                self._report_justify(q_entry["question_answers"], flowables)
                dc = self._draw_charts(q_summary)
                if dc:
                    flowables.append(dc)

    def generate_report(self, buffer: BytesIO, report_data: dict):
        doc = SimpleDocTemplate(buffer)
        Story = [Spacer(1, 2 * inch)]
        self._append_questions(report_data, Story)
        doc.build(Story, onFirstPage=self.myFirstPage, onLaterPages=self.myLaterPages)

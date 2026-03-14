from flask import Flask, render_template, request, send_file
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

app = Flask(__name__)
INVOICES_DIR = "invoices"
os.makedirs(INVOICES_DIR, exist_ok=True)
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.form
    # PDF generation goes here

    filename = f"{data.get('invoiceNum', 'invoice')}.pdf"
    filepath = os.path.join(INVOICES_DIR, filename)

    c = canvas.Canvas(filepath, pagesize=A4)
    w, h = A4

    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, h - 60, data.get("bizName", ""))

    c.setFont("Helvetica", 11)
    c.drawString(50, h - 85, data.get("bizEmail", ""))

    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, h - 130, f"Bill To: {data.get('clientName', '')}")

    c.setFont("Helvetica", 11)
    c.drawString(50, h - 150, data.get("clientAddress", ""))

    c.line(50, h - 170, w - 50, h - 170)

    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, h - 195, f"Invoice: {data.get('invoiceNum', '')}   Date: {data.get('issueDate', '')}   Due: {data.get('dueDate', '')}")

    c.save()
    return send_file(filepath, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)     
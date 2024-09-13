from docxtpl import DocxTemplate

doc = DocxTemplate("templates/test.docx")
context = {"title": "Trim Your Tummy"}
doc.render(context)
doc.save("generated_doc.docx")

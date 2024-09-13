from pypdf import PdfMerger


class PdfUtil:
    def merge_pdfs(self, input_files, output_file):
        merger = PdfMerger()

        for pdf in input_files:
            merger.append(pdf)

        merger.write(output_file)
        merger.close()

    def pdf_to_png(self, pdf):
        pass


if __name__ == "__main__":
    pdfMerger = PdfUtil()
    pdfMerger.merge_pdfs(
        ["mvp/retirement_asset.pdf", "docs/demo9.pdf"],
        "mvp/cupertino_retirement_ebook.pdf",
    )

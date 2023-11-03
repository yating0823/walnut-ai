import os
import fitz
import xlsxwriter

def split_range_page(input, output, range):
    if not os.path.exists(output):
        os.makedirs(output)
    doc = fitz.open(input)
    start = range[0] - 1
    end = range[1] - 1
    dst_doc = fitz.open()
    dst_doc.insert_pdf(doc, from_page=start, to_page=end)
    dst_doc.save(os.path.join(output,'range_page.pdf'))
    dst_doc.close()
    doc.close()

split_range_page('keppel-corporation-limited-annual-report-2018.pdf','test', [12,12])

doc = fitz.open('./test/range_page.pdf')
result = []
for page in doc:
    text = page.get_text()
    output = page.get_text("blocks")
    for block in output:
        if block[6] == 0: # (x0, y0, x1, y1, "lines in the block", block_no, block_type)
            result.append(block[4].replace("\n", ""))

workbook = xlsxwriter.Workbook('block_text.xlsx')
worksheet = workbook.add_worksheet()
row = 0
column = 0
for i in result:
    worksheet.write(row, column, i)
    row += 1
workbook.close()


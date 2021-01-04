import PyPDF2
import subprocess
import pdfkit
import os
import sys
# pdfが入っている二つのフォルダを指定してくっつける
connect_dir1 = "./004_tsuchiya_radiation/bachelor/pdf/"
connect_dir2 = "./004_tsuchiya_radiation/bachelor/pdf_discription/"
#出力pdfの名前
out_pdf_path = "./004_tsuchiya_radiation/bachelor_score.pdf"

test_list1 = os.listdir(connect_dir1)
test_list2 = os.listdir(connect_dir2)
if test_list1 !=test_list2:
    sys.error("多分pdfうまく結合できないからpdfのディレクトリ見直して")
    sys.exit()
list1 = [os.path.join(connect_dir1, x) for x in os.listdir(connect_dir1)]
list2 = [os.path.join(connect_dir2, x) for x in os.listdir(connect_dir2)]


merger = PyPDF2.PdfFileMerger()
for x, y in zip(list1, list2):
    merger.append(x)
    merger.append(y)

merger.write(out_pdf_path)
merger.close()

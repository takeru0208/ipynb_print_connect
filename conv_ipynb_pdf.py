import os
import subprocess

"""
このプログラムについて

# やること
ipynb to pdfの変換

# 入出力
入力：ipynbがいっぱい入ったディレクトリと出力ディレクトリと、pdfの分割数
出力：プリントしやすくなったpdfファイル

# 変えるべきところ
WANT_GET_PATH:授業用のipynbがあるディレクトリのパスを指定。ncとかdocxは削除しておく
OUT_MERGED_DIR:pdfの出力先のディレクトリ
flag: 横n列*縦m列で9*9でpdfを分割するか2*1でpdfを分割するかの選択
      9*9の時 flag = 1を
      2*1の時 flag = 0を

# 注意
おんなじディレクトリにpdf_merge_multipages.pyがあること
cdo.sifをimageshareからとってくること

# 実行方法
$ singularity run ./cdo.sif python3 conv_ipynb_pdf.py
"""

# 変換したいプログラムがあるディレクトリ
# あらかじめ.docxとか.ipynb_checkpoints/とか~.ncとかをそのディレクトリから移動もとい削除しておく
# 最後スラッシュつけ忘れないようにすること！
WANT_GET_PATH = "./004_tsuchiya_radiation/master/SSEO_003_submit08_discription"

# 出力先のディレクトリ, 演習全てと、記述のみのやつそれぞれpdfディレクトリを作るのがおすすめ
# 最後スラッシュつけ忘れないようにすること！
OUT_MERGED_DIR = "./004_tsuchiya_radiation/master/pdf_description/"
# 横n列*縦m列で9*9でpdfを分割するか2*1でpdfを分割するかの選択
# 9*9の時 flag = 1を
# 2*1の時 flag = 0を
flag = 1










#　基本的に以下は変えない
############################################################################################
def local_chdir(func):
    def _inner(*args, **kwargs):
        # 元のカレントディレクトリを変数に代入
        dir_original = os.getcwd()
        # 渡された関数実行
        ret = func(*args, **kwargs)
        # カレントディレクトリを元に戻す
        os.chdir(dir_original)
        return ret
    return _inner

@local_chdir
def make_pdf(from_path_list, out_path_list):
    for from_path, out_path in zip(from_path_list, out_path_list):
        # jupyterのnbconvertを使ってipynbから中間htmlファイルを作成
        args = ['jupyter', 'nbconvert', '--to=html', 'from_path', '--output', "out_path"]
        print(from_path)
        print(out_path)
        args[3] = from_path
        args[5] = out_path
        try:
            res = subprocess.check_output(args)
        except:
            print("jupyter nbconvert error")

        # wkhtmltopdfというアプリを使って中間htmlファイルからpdfを作成
        html_file_path = WANT_GET_PATH + "/" + out_path + ".html"
        middle_pdf_path = "./" + out_path + ".pdf"

        from_path = html_file_path
        to_path = middle_pdf_path

        html_pdf_args = ["wkhtmltopdf", from_path, to_path]
        try:
            res = subprocess.check_output(html_pdf_args)
        except:
            print("wkhtmltopdf error")
        
        
        # pdf_merge_multipages.pyを使って１ページに複数のページがあるpdfを作成
        out_pdf_path = OUT_MERGED_DIR + out_path + ".pdf"
        
        # 9*9の時 flag = 1を
        # 2*1の時 flag = 0を
        if flag == 1:
            div_pdf_args = ['python3', "./pdf_merge_multipages.py", middle_pdf_path, '-output', out_pdf_path,
            '-columns', '3', '-lines', '3', '-page-order', 'left2bottom']
        else:
            div_pdf_args = ['python3', "./pdf_merge_multipages.py", middle_pdf_path, '-output', out_pdf_path,
            '-columns', '2', '-lines', '1', '-page-order', 'left2bottom']
        try:
            res = subprocess.check_output(div_pdf_args)
        except:
            print("pdf_merge_multipages.py error")

        # 作った中間ファイルの削除
        print("middle_pdf_path:")
        print(middle_pdf_path)
        print("save path:")
        print(out_pdf_path)
        os.remove(html_file_path)
        os.remove(middle_pdf_path)
        

# os.makedirs(MIDDLE_PATH, exist_ok=True)
#　pdfに変換するipnbファイルのリストの作成
ipynb_path = os.listdir(WANT_GET_PATH)
from_path_list = [os.path.join(WANT_GET_PATH, path) for path in ipynb_path]

#中間生成ファイルのhtmlファイルのパスのリスト
out_path_list = [x.split('.')[0] for x in ipynb_path]

make_pdf(from_path_list, out_path_list)


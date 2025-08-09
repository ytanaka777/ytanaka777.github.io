import os
import glob
import sys

def remove_last_line(text):
    return "\n".join(text.strip().splitlines()[:-1])

def convert_markdown_pairs(input_dir, output_dir):
    # 絶対パスに正規化
    input_dir  = os.path.abspath(input_dir)
    output_dir = os.path.abspath(output_dir)

    # 出力先を用意
    os.makedirs(output_dir, exist_ok=True)

    # 入力: input_dir の *-ja.md を列挙
    ja_files = sorted(glob.glob(os.path.join(input_dir, "*-ja.md")))

    for ja_path in ja_files:
        base_name = os.path.basename(ja_path).replace("-ja.md", "")
        en_path   = os.path.join(input_dir,  f"{base_name}-en.md")
        out_path  = os.path.join(output_dir, f"{base_name}.md")

        if not os.path.exists(en_path):
            print(f"{en_path} が見つかりません. スキップします.")
            continue

        with open(ja_path, "r", encoding="utf-8") as f:
            ja_content = remove_last_line(f.read())
        with open(en_path, "r", encoding="utf-8") as f:
            en_content = remove_last_line(f.read())

        with open(out_path, "w", encoding="utf-8") as f:
            f.write("::: {.lang .lang-ja}\n")
            if ja_content:
                f.write(ja_content + "\n")
            f.write(":::\n\n")
            f.write("::: {.lang .lang-en}\n")
            if en_content:
                f.write(en_content + "\n")
            f.write(":::\n")

        print(f"生成完了: {out_path}")

if __name__ == "__main__":
    argc = len(sys.argv)
    if argc == 1:
        inp = os.getcwd()
        out = os.getcwd()
    elif argc == 2:
        inp = sys.argv[1]
        out = os.getcwd()          # 出力はカレント
    elif argc == 3:
        inp = sys.argv[1]
        out = sys.argv[2]
    else:
        print("使い方: python convert.py [<入力ディレクトリ> [<出力ディレクトリ>]]")
        sys.exit(1)

    if not os.path.isdir(inp):
        print(f"エラー: {inp} は存在しないかディレクトリではありません.")
        sys.exit(1)

    convert_markdown_pairs(inp, out)
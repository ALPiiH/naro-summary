import json

def clean_jsonl():
    input_file = 'n2267be_summaries_gemini-2.5-pro_include_text.jsonl'
    # 出力ファイル名（元ファイルを上書きしたい場合は同じ名前に変更してください）
    output_file = 'n2267be_summaries_gemini-2.5-pro.jsonl'

    print(f"処理を開始します: {input_file} -> {output_file}")
    
    count = 0
    try:
        with open(input_file, 'r', encoding='utf-8') as fin, \
             open(output_file, 'w', encoding='utf-8') as fout:
            
            for line in fin:
                line = line.strip()
                if not line:
                    continue
                
                try:
                    data = json.loads(line)
                    
                    # 'text' フィールドがあれば削除
                    if 'text' in data:
                        del data['text']
                    
                    # 軽量化したデータを書き込み
                    json.dump(data, fout, ensure_ascii=False)
                    fout.write('\n')
                    count += 1
                    
                except json.JSONDecodeError:
                    continue
                    
        print(f"完了しました。合計 {count} 件のデータを処理しました。")
        print(f"生成されたファイル: {output_file}")
        print("※このファイルを元の 'n2267be_summaries.jsonl' と置き換えて使用してください。")

    except FileNotFoundError:
        print(f"エラー: '{input_file}' が見つかりませんでした。")

if __name__ == "__main__":
    clean_jsonl()
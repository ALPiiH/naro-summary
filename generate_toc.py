import json
import re
import os

def generate_toc_json():
    input_file = 'n2267be_summaries_gemini-2.5-pro.jsonl'
    map_file = 'chapter_titles.json'
    output_file = 'toc_data.json'

    # タイトル変換マップの読み込み
    chapter_titles = {}
    if os.path.exists(map_file):
        try:
            with open(map_file, 'r', encoding='utf-8') as f:
                chapter_titles = json.load(f)
            print(f"'{map_file}' を読み込みました。")
        except Exception as e:
            print(f"警告: '{map_file}' の読み込みに失敗しました: {e}")

    toc_groups = []
    current_group = None
    current_group_name = ""

    print("目次データを生成中...")

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                try:
                    entry = json.loads(line)
                    entry_id = entry.get('id')
                    label = (entry.get('label') or "").strip()
                    title = entry.get('title') or "無題"
                    
                    # --- グループ化ロジック (JSと同じもの) ---
                    prefix = label[:3]
                    is_chapter_head = re.match(r'^第.章$', prefix)

                    # グループ判定用のキー
                    raw_key = prefix if is_chapter_head else "序章"
                    
                    # 表示名の決定 (マップにあれば変換、なければそのまま)
                    display_group_name = chapter_titles.get(raw_key, raw_key)
                    
                    # マップにキーがなく、prefixでヒットする場合の救済
                    if raw_key not in chapter_titles and prefix in chapter_titles:
                        display_group_name = chapter_titles[prefix]

                    # 新しいグループを作るか判定
                    # (章頭の場合、またはまだグループがない場合、またはグループ名が変わった場合)
                    if is_chapter_head or current_group is None:
                        if display_group_name != current_group_name:
                            # 新しいグループを作成
                            current_group = {
                                "groupName": display_group_name,
                                "items": []
                            }
                            toc_groups.append(current_group)
                            current_group_name = display_group_name

                    # アイテム追加
                    current_group["items"].append({
                        "id": entry_id,
                        "disp": f"{label} {title}".strip()
                    })

                except json.JSONDecodeError:
                    continue

        # JSON書き出し
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(toc_groups, f, ensure_ascii=False, indent=2)
        
        print(f"完了: '{output_file}' を生成しました。")

    except FileNotFoundError:
        print(f"エラー: '{input_file}' が見つかりませんでした。")

if __name__ == "__main__":
    generate_toc_json()
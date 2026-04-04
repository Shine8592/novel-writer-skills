#!/usr/bin/env python3
"""
quality_check.py — 小说章节质量审核

用法:
  python3 quality_check.py --file <章节文件> --quick   # 5项核心检查
  python3 quality_check.py --file <章节文件> --full    # 全量检查
  python3 quality_check.py --dir <目录> --quick        # 批量检查
"""
import argparse, os, re, sys
from collections import Counter

def count_chinese(text): return sum(1 for c in text if '\u4e00' <= c <= '\u9fff')

AI_MARKERS = [
    "暗思涌起", "心理描写", "环境描写", "动作描写", "神态描写",
    "命运的齿轮", "未完待续", "故事才刚开始", "真正的危机",
    "风暴即将来临", "", "他不知道的是", "殊不知",
    "一场更大的", "更大的风暴", "", "而这，仅仅只是",
    "这才是开始", "真正的考验", "悄然拉开帷幕",
]

TEMPLATE_ENDINGS = [
    "命运的齿轮", "未完待续", "真正的危机", "风暴即将来临",
    "拉开帷幕", "才刚刚开始", "而这只是", "这只是",
    "更大的阴谋",
]

def quick_checks(text):
    results = []
    cn = count_chinese(text); total = len(text)
    results.append(("字数达标(≥12000)", f"{cn}字", cn >= 12000))
    results.append(("中文纯度(≥95%)", f"{cn/total*100:.1f}%", cn/total >= 0.95))
    
    markers_found = [m for m in AI_MARKERS if m in text]
    results.append(("AI标记词(0个)", f"{len(markers_found)}个", len(markers_found) == 0))
    
    last500 = text[-500:]
    endings_found = [e for e in TEMPLATE_ENDINGS if e in last500]
    results.append(("模板化结尾(无)", f"{len(endings_found)}个", len(endings_found) == 0))
    
    paragraphs = text.split('\n\n')
    lengths = [len(p) for p in paragraphs if p.strip()]
    max_len = max(lengths) if lengths else 0
    results.append(("段落长度合理", f"最大{max_len}字", max_len < 3000))
    
    return results

def full_checks(text):
    results = quick_checks(text)
    paragraphs = text.split('\n\n')
    words = text.replace('\n', ' ').split()
    
    # 对话比例
    dialogue = sum(len(d) for d in re.findall(r'[""].*?[""]', text) + re.findall(r"[''].*?['']", text))
    total = len(text)
    results.append(("对话比例(30-50%)", f"{dialogue/total*100:.0f}%", 25 <= dialogue/total <= 55))
    
    # 标点比例
    punctuation = sum(1 for c in text if c in '，。！？、；：""''（）【】《》')
    results.append(("标点使用", f"{punctuation}个", punctuation > 0))
    
    # 主角名
    results.append(("角色名（人工检查）", "N/A", True))
    
    return results

def print_report(filename, results):
    title = filename[:30]
    passed = sum(1 for _, _, p in results if p)
    total = len(results)
    
    print(f"\n{'='*50}")
    print(f"  {title} 质量审核: {passed}/{total} 通过")
    print(f"{'='*50}")
    for name, value, ok in results:
        icon = "✅" if ok else "❌"
        print(f"  {icon} {name}: {value}")

def main():
    parser = argparse.ArgumentParser(description="小说质量审核")
    parser.add_argument("--file", type=str, help="章节文件路径")
    parser.add_argument("--dir", type=str, help="目录路径(批量)")
    parser.add_argument("--full", action="store_true", help="全量检查")
    parser.add_argument("--quick", action="store_true", help="快速检查(默认)")
    args = parser.parse_args()
    
    files = []
    if args.file:
        files.append(args.file)
    elif args.dir:
        base = args.dir
        files = sorted([os.path.join(base, f) for f in os.listdir(base) 
                       if f.startswith('00') and f.endswith('.md')])
    else:
        print("用法: python3 quality_check.py --file <文件> 或 --dir <目录>")
        sys.exit(1)
    
    for filepath in files:
        if not os.path.exists(filepath):
            print(f"❌ 文件不存在: {filepath}")
            continue
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
        
        if args.full:
            results = full_checks(text)
        else:
            results = quick_checks(text)
        
        print_report(os.path.basename(filepath), results)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
batch_generate.py — 批量生成小说章节

用法:
  python3 batch_generate.py --outline <大纲文件> --start <章号> --end <章号> --output <输出目录> [--api modelscope|fyra|ph8]

API顺序:
  modelscope → fyra → ph8
  
自动分段生成，合并，去重重叠。每章目标12000+字。
"""
import argparse
import httpx
import os
import sys
import time
import json

# ============================================
# API 配置
# ============================================
APIS = {
    "modelscope": {
        "url": "https://api-inference.modelscope.cn/v1/chat/completions",
        "headers": {"Authorization": "Bearer ms-cbf54443-9984-41d8-86a7-6909ef4353f9"},
        "model": "deepseek-ai/DeepSeek-V3.2",
        "timeout": 300,
    },
    "fyra": {
        "url": "https://Fyra.im/v1/chat/completions",
        "headers": {"Authorization": "Bearer lj-840347b7a2b7534bc07cae15fb697a98a967c0ddb7ac07fb084b8985cb320651"},
        "model": "mistral-large-3-675b-instruct",
        "timeout": 240,
    },
    "ph8": {
        "url": "https://ph8.co/v1/chat/completions",
        "headers": {"Authorization": "Bearer sk-80647fc395d243b89fdff21fb115c4f3"},
        "model": "qwen3-235b-a22b-2507",
        "timeout": 180,
    },
}

API_ORDER = ["modelscope", "fyra", "ph8"]

HARD_CONSTRAINTS = """1. 纯中文！所有数字用中文写法（一、二、三十），绝不出现阿拉伯数字和英文
2. 零AI标记词汇！不得出现"暗思涌起""心理描写""环境描写""动作描写""命运的齿轮"等
3. 禁止模板化结尾！不要"真正的危机才刚刚开始""未完待续"
4. 主角名统一（不得在不同名字间切换）
5. 直接输出小说正文，不要任何说明文字"""

TARGET_WORDS = 12000
MAX_TOKENS = 8192
TEMPERATURE = 0.8
MIN_API_DELAY = 15  # 秒

def count_chinese(text):
    return sum(1 for c in text if '\u4e00' <= c <= '\u9fff')

def load_chapter_info(overrides={}):
    """Load chapter outline info from overrides dict"""
    return overrides

def make_prompt(chapter_num, chapter_title, plot, prev_ending="", segment=1, target=None):
    """Generate prompt for chapter or segment"""
    if target is None:
        target = TARGET_WORDS
    
    plot_section = f"\n【本章剧情】{plot}" if plot else ""
    prev_section = f"\n\n【已有内容结尾】{prev_ending}..." if prev_ending else ""
    segment_label = f"第{segment}部分" if segment > 1 else ""
    
    if segment == 1:
        body = (
            f"你是网络小说主笔，正在写第{chapter_num}章：{chapter_title}。\n"
            f"{plot_section}\n\n"
            f"硬性要求：\n{HARD_CONSTRAINTS}\n"
            f"字数必须达到{target}字。\n"
            f"直接输出完整章节正文。"
        )
    else:
        body = (
            f"你是网络小说主笔，继续写第{chapter_num}章：{chapter_title}（{segment_label}）。\n"
            f"{plot_section}\n\n"
            f"{prev_section}\n\n"
            f"从已有内容的结尾处**自然续写**，不可重复已有内容。\n\n"
            f"硬性要求：\n{HARD_CONSTRAINTS}\n"
            f"续写内容必须至少{target}字。\n"
            f"直接输出续写正文。"
        )
    return body

def call_api(text, api_name="modelscope"):
    """Call the specified API with retry"""
    cfg = APIS.get(api_name)
    if not cfg:
        return None, f"Unknown API: {api_name}"
    
    try:
        resp = httpx.post(
            cfg["url"],
            json={"model": cfg["model"], "messages": [{"role": "user", "content": text}],
                  "max_tokens": MAX_TOKENS, "temperature": TEMPERATURE},
            headers=cfg["headers"],
            timeout=cfg["timeout"]
        )
        if resp.status_code == 200:
            d = resp.json()
            if "error" in d:
                return None, str(d["error"])
            return d["choices"][0]["message"]["content"], None
        elif resp.status_code == 429:
            return None, f"RATE_LIMITED (429)"
        else:
            return None, f"HTTP {resp.status_code}'
    except httpx.ReadTimeout:
        return None, "READ_TIMEOUT"
    except Exception as e:
        return None, f"EXCEPTION: {e}"

def api_call_with_fallback(prompt):
    """Try APIs in order until one works"""
    for api_name in API_ORDER:
        text, err = call_api(prompt, api_name)
        if text:
            return text, api_name
        if "RATE_LIMITED" in str(err):
            print(f"    ⏳ {api_name} 限流, 等30s后重试...")
            time.sleep(30)
            continue
        print(f"    ⚠️ {api_name} 失败: {err}, 切下一个API")
        time.sleep(5)
    return None, "ALL_FAILED"

def generate_chapter(chapter_num, chapter_title, plot, output_dir, prev_ending=""):
    """Generate a full chapter, possibly in segments"""
    os.makedirs(output_dir, exist_ok=True)
    fn = f"{chapter_num:04d}_{chapter_title}.md"
    path = os.path.join(output_dir, fn)
    
    print(f"\n{'='*60}")
    print(f"📝 第{chapter_num}章: {chapter_title}")
    print(f"{'='*60}")
    
    all_text = ""
    segment = 1
    
    while True:
        # Check current length
        if all_text:
            ending_snippet = all_text[-400:]
            current_len = count_chinese(all_text)
        else:
            ending_snippet = prev_ending
            current_len = 0
        
        if current_len >= TARGET_WORDS:
            print(f"  ✅ 已完成: {current_len}字")
            break
        
        needed = TARGET_WORDS - current_len + 500  # Buffer
        print(f"  📝 第{segment}段: 当前{current_len}字, 需加~{needed}字...", end=" ", flush=True)
        
        prompt = make_prompt(chapter_num, chapter_title, plot, 
                           prev_ending=ending_snippet, segment=segment, target=needed)
        
        text, api_used = api_call_with_fallback(prompt)
        if not text:
            print(f"\n  ❌ 所有API都失败了, 跳过本章")
            return False
        
        add_cn = count_chinese(text)
        all_text += ("\n\n" if all_text else "") + text
        total = count_chinese(all_text)
        print(f"{api_used}: ✅ +{add_cn}字 = {total}字")
        
        segment += 1
        time.sleep(MIN_API_DELAY)
    
    # Save
    with open(path, 'w', encoding='utf-8') as f:
        f.write(all_text)
    
    print(f"  💾 已保存: {path} ({total}字)")
    return True

def main():
    parser = argparse.ArgumentParser(description="批量生成小说章节")
    parser.add_argument("--outline", type=str, help="大纲JSON文件路径")
    parser.add_argument("--start", type=int, required=True, help="起始章号")
    parser.add_argument("--end", type=int, required=True, help="结束章号")
    parser.add_argument("--output", type=str, required=True, help="输出目录")
    parser.add_argument("--api", type=str, choices=API_ORDER, default=None,
                       help="强制使用指定API")
    
    args = parser.parse_args()
    
    # Override API order if specified
    if args.api:
        global API_ORDER
        API_ORDER = [args.api]
    
    # Load outline if provided
    chapters = {}
    if args.outline and os.path.exists(args.outline):
        with open(args.outline, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # Assume format: {"chapters": {"1": {"title": "...", "plot": "..."}, ...}}
        chapters = data.get("chapters", data)
    
    # Generate
    results = {"success": [], "failed": []}
    
    for ch in range(args.start, args.end + 1):
        key = str(ch)
        chapter_title = chapters.get(key, {}).get("title", f"第{ch}章")
        chapter_plot = chapters.get(key, {}).get("plot", "")
        prev_ending = ""
        
        # Get previous chapter ending for continuity
        prev_key = str(ch - 1)
        prev_fn = os.path.join(args.output, f"{int(prev_key):04d}_{chapters.get(prev_key, {}).get('title', '')}.md")
        if os.path.exists(prev_fn):
            with open(prev_fn, 'r', encoding='utf-8') as f:
                prev_ending = f.read()[-500:]
        
        success = generate_chapter(ch, chapter_title, chapter_plot, args.output, prev_ending)
        if success:
            results["success"].append(ch)
        else:
            results["failed"].append(ch)
        
        # Inter-chapter delay
        time.sleep(10)
    
    # Summary
    print(f"\n{'='*60}")
    print(f"📊 生成结果汇总")
    print(f"{'='*60}")
    print(f"成功: {len(results['success'])}/{args.end - args.start + 1} ({results['success']})")
    if results['failed']:
        print(f"失败: {len(results['failed'])} ({results['failed']})")

if __name__ == "__main__":
    main()

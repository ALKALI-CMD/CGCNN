import gzip
import json

def load_matbench_phonons(file_path):
    """加载 matbench_phonons.json.gz 文件"""
    try:
        with gzip.open(file_path, "rt", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"读取文件错误: {e}")
        return None

def print_single_molecule_data(data, index=0):
    """
    提取并打印单个分子（材料条目）的所有数据
    
    Args:
        data (dict/list): 完整数据集
        index (int): 要提取的条目索引（默认第1个）
    """
    if not data:
        return
    
    # 根据 matbench 数据集的格式，处理不同的数据结构
    if isinstance(data, dict):
        # 情况1：数据是字典，包含 "entries" 或 "data" 键
        if "entries" in data:
            entries = data["entries"]
        elif "data" in data:
            entries = data["data"]
        else:
            # 如果是键值对形式的字典，取第一个键对应的数据
            entries = list(data.values())
    elif isinstance(data, list):
        # 情况2：数据本身是条目列表
        entries = data
    else:
        print("数据格式不支持")
        return
    
    # 检查索引是否有效
    if index < 0 or index >= len(entries):
        print(f"索引 {index} 无效，数据共有 {len(entries)} 条")
        return
    
    # 提取单个分子的所有数据
    single_entry = entries[index]
    print(f"=== 单个分子（索引 {index}）的完整数据 ===")
    print(f"数据类型: {type(single_entry)}")
    print(f"包含字段数: {len(single_entry) if isinstance(single_entry, dict) else 'N/A'}\n")
    
    # 逐字段打印所有数据
    if isinstance(single_entry, dict):
        for key, value in single_entry.items():
            print(f"【{key}】")
            # 处理嵌套结构，确保清晰展示
            if isinstance(value, (dict, list)) and len(str(value)) > 200:
                print(f"  类型: {type(value)}")
                if isinstance(value, list):
                    print(f"  长度: {len(value)}")
                    print(f"  前5个元素: {value[:5] if len(value) > 5 else value}")
                elif isinstance(value, dict):
                    print(f"  键列表: {list(value.keys())}")
            else:
                print(f"  值: {value}")
            print()  # 空行分隔
    else:
        print(f"完整数据: {single_entry}")

# 主程序
if __name__ == "__main__":
    file_path = "matbench_phonons.json.gz"  # 替换为你的文件路径
    data = load_matbench_phonons(file_path)
    
    if data:
        # 提取第1个分子的数据（索引0），可修改index参数选择其他分子
        print_single_molecule_data(data, index=0)
        
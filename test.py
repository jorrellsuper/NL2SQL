import re
import json


def main(arg1: str) -> dict:
    # 默认返回值
    default_output = {
        "results": "",
        "ECHarts": "0",
        "chartType": "",
        "chartTitle": "",
        "chartData": "",
        "chartXAxis": ""
    }

    try:
        # 使用正则表达式提取被 ```json 和 ``` 包裹的内容
        match = re.search(r'```json\s*([\s\S]*?)\s*```', arg1)
        if not match:
            raise ValueError("输入字符串中未找到有效的 JSON 数据")

        # 提取 JSON 字符串
        json_str = match.group(1).strip()

        # 将 JSON 字符串解析为 Python 字典
        result_dict = json.loads(json_str)
    except Exception as e:
        # 如果解析失败，打印错误信息并返回默认输出
        print(f"解析失败: {e}")
        return default_output

    # 检查是否包含 ECHarts 字段
    if "ECHarts" not in result_dict:
        result_dict["ECHarts"] = "0"  # 默认设置为 "0"

    # 根据 ECHarts 的值动态检查图表相关字段
    if result_dict["ECHarts"] == "1":
        required_chart_fields = ["chartType", "chartTitle", "chartData", "chartXAxis"]
        for field in required_chart_fields:
            if field not in result_dict:
                result_dict[field] = ""  # 自动补全缺失字段为空字符串

    # 构造返回值
    return {
        "results": str(result_dict.get("results", "")),
        "ECHarts": str(result_dict.get("ECHarts", "0")),
        "chartType": str(result_dict.get("chartType", "")),
        "chartTitle": str(result_dict.get("chartTitle", "")),
        "chartData": str(result_dict.get("chartData", "")),
        "chartXAxis": str(result_dict.get("chartXAxis", ""))
    }

arg1="```json\n{ \"results\": \"以下是员工年龄分布的数据分析结果：\\n\\- **20-25岁**：221人\\n- **26-30岁**：312人\\n- **31-35岁**：3019人\\n- **36-40岁**：98人\\n- **41-45岁**：68人\\n- **其他**：192人\\n从数据可以看出，31-35岁的员工数量最多，占比最高。\",\n \"ECHarts\": \"1\",\n \"chartType\": \"柱状图\",\n \"chartTitle\": \"员工年龄分布\",\n \"chartData\": \"221;312;3019;98;68;192\",\n \"chartXAxis\": \"20-25;26-30;31-35;36-40;41-45;Other\"\n}\n```"

print(main(arg1))
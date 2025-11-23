# ...existing code...
import json
import os

def convert_doccano_to_uie_with_rel(input_path, output_path, include_course=False):
    """
    将 doccano 导出的 jsonl 转换为 UIE 微调格式（支持实体 description 分配与 relations 嵌套）
    参数:
      input_path: doccano 导出的 all.jsonl 路径
      output_path: 输出 uie.jsonl 路径（每行一条）
      include_course: 是否将 Course 实体也输出为 top-level 标签（默认为 False）
    """
    with open(input_path, encoding="utf-8") as fin, open(output_path, "w", encoding="utf-8") as fout:
        for line in fin:
            if not line.strip():
                continue
            data = json.loads(line)
            text = data.get("text", "")
            entities = data.get("entities", [])
            relations = data.get("relations", []) or []

            # 按 start_offset 排序（保证顺序遍历）
            entities.sort(key=lambda x: x.get("start_offset", 0))

            # id -> entity 映射（便于通过 relations 查找）
            ent_by_id = {e["id"]: e for e in entities if "id" in e}

            # 构造 Concept 列表（保留对应 entity id 以便后续关系挂载）
            concept_items = {}   # ent_id -> item
            label_list = []      # 最终 Concept 列表（UIE 要求）

            last_concept_item = None
            for ent in entities:
                eid = ent.get("id")
                lab = ent.get("label")
                s = ent.get("start_offset")
                e = ent.get("end_offset")
                if s is None or e is None:
                    continue
                txt = text[s:e]

                if lab == "Concept":
                    item = {"start": s, "end": e, "text": txt}
                    concept_items[eid] = item
                    label_list.append(item)
                    last_concept_item = item

                elif lab == "description":
                    # 分配给前一个 Concept（如果没有则忽略）
                    if last_concept_item is not None:
                        # 如果已有 description，转为列表或追加
                        desc = {"start": s, "end": e, "text": txt}
                        if "description" not in last_concept_item:
                            last_concept_item["description"] = desc
                        else:
                            # 如果已有单个对象，改为列表
                            if isinstance(last_concept_item["description"], list):
                                last_concept_item["description"].append(desc)
                            else:
                                last_concept_item["description"] = [last_concept_item["description"], desc]
                    # description 本身也可能作为独立知识点的候选，按需保留（此处不额外创建节点）

                elif lab == "Course":
                    # 可选: 如果 include_course True，则把 Course 当成一个独立 label（放入输出）
                    if include_course:
                        # 把 Course 当成顶层单个实体 label (放在 "Course" 下)
                        # 这里我们将 Course 放入 label_map，以便一次性输出
                        # Do nothing here (we will handle Course separately after loop)
                        pass

            # 处理 relations: 把关系挂载到对应的 from_id 的 concept_item 下
            for rel in relations:
                from_id = rel.get("from_id")
                to_id = rel.get("to_id")
                rtype = rel.get("type", "relation")
                if from_id is None or to_id is None:
                    continue
                # 只在 from entity 是 Concept 时挂载（UIE 常把关系作为主实体的子字段）
                from_ent = ent_by_id.get(from_id)
                to_ent = ent_by_id.get(to_id)
                if from_ent is None or to_ent is None:
                    continue
                if from_ent.get("label") != "Concept":
                    # 如果 from 不是 Concept，尝试把关系挂在 nearest upper Concept（可扩展）
                    continue

                # 保证 concept item 存在
                concept_item = concept_items.get(from_id)
                if concept_item is None:
                    # 有时关系的 from 在实体序列中不在 Concept（跳过）
                    continue

                # 构造目标实体表示
                ts = to_ent.get("start_offset")
                te = to_ent.get("end_offset")
                ttext = text[ts:te] if ts is not None and te is not None else to_ent.get("text", "")
                target_obj = {"start": ts, "end": te, "text": ttext}

                # 按关系类型追加（同一类型可能有多个目标）
                if rtype not in concept_item:
                    concept_item[rtype] = [target_obj]
                else:
                    concept_item[rtype].append(target_obj)

            # 构造最终 UIE 格式字典
            uie_item = {"text": text, "label": {"Concept": label_list}}

            # 如果需要包含 Course，并且文件中有 Course 实体，则构造 Course 字段
            if include_course:
                course_list = []
                for ent in entities:
                    if ent.get("label") == "Course":
                        s = ent.get("start_offset"); e = ent.get("end_offset")
                        if s is None or e is None:
                            continue
                        course_list.append({"start": s, "end": e, "text": text[s:e]})
                if course_list:
                    uie_item["label"]["Course"] = course_list

            fout.write(json.dumps(uie_item, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    src = r"f:\StudyFiles\ZYGC2025\aicourse\backend\output\标注数据\all.jsonl"
    dst = r"f:\StudyFiles\ZYGC2025\aicourse\backend\output\标注数据\uie_train_rel.json"
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    # 默认不把 Course 当训练标签(include_course=False)，如果想包含请改为 True
    convert_doccano_to_uie_with_rel(src, dst, include_course=False)
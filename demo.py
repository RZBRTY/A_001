#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能招聘多Agent系统 - 演示脚本
"""

import sys
import io

# 设置标准输出为UTF-8编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from orchestrator import RecruitingOrchestrator


def main():
    print("=" * 70)
    print("[*] 智能招聘多Agent系统")
    print("=" * 70)
    print()
    
    # 示例简历
    sample_resume = """姓名: 张明
教育背景: 某某大学 计算机科学与技术 硕士
工作经验: 5年Python开发经验，3年机器学习项目经验
技能: Python, Java, MySQL, Redis, Docker, 机器学习, 数据分析
项目经验: 主导过多个电商推荐系统项目，参与过大数据平台建设"""
    
    # 示例岗位要求
    sample_job = {
        "title": "高级算法工程师",
        "description": "负责推荐算法研发，需要团队协作能力",
        "required_skills": ["Python", "机器学习", "数据分析", "MySQL", "Redis"]
    }
    
    print("[*] 候选人简历:")
    print("-" * 50)
    print(sample_resume)
    print()
    
    print("[*] 岗位要求:")
    print("-" * 50)
    print(f"岗位名称: {sample_job['title']}")
    print(f"岗位描述: {sample_job['description']}")
    print(f"技能要求: {', '.join(sample_job['required_skills'])}")
    print()
    
    print("[*] 启动多Agent招聘评估流程...")
    print()
    
    # 创建编排器
    orchestrator = RecruitingOrchestrator()
    
    # 运行完整流程
    results = orchestrator.run_full_recruiting_process(
        resume_text=sample_resume,
        job_requirements=sample_job
    )
    
    print()
    print("=" * 70)
    print("[*] 评估结果")
    print("=" * 70)
    print()
    
    orchestrator.print_summary(results)
    
    print()
    print("=" * 70)
    print("[*] 演示完成！")
    print("=" * 70)
    print()
    print("[*] 项目说明:")
    print("  - 本项目包含5个专业Agent，形成完整的招聘评估流程")
    print("  - 支持自定义简历和岗位要求")
    print("  - 提供完整的推理过程和决策依据")
    print("  - 可扩展性强，易于接入真实的LLM模型")
    print()


if __name__ == "__main__":
    main()

from agents import (
    ResumeParserAgent,
    JobMatchingAgent,
    InterviewQuestionAgent,
    InterviewEvaluationAgent,
    DecisionRecommendationAgent
)
from typing import Dict, Any


class RecruitingOrchestrator:
    def __init__(self):
        self.resume_parser = ResumeParserAgent()
        self.job_matcher = JobMatchingAgent()
        self.question_generator = InterviewQuestionAgent()
        self.interview_evaluator = InterviewEvaluationAgent()
        self.decision_maker = DecisionRecommendationAgent()
        
        self.workflow_log = []

    def run_full_recruiting_process(self, resume_text: str, job_requirements: Dict, interview_answers: list = None) -> Dict[str, Any]:
        print("=" * 60)
        print("智能招聘全流程多Agent协作系统启动")
        print("=" * 60)
        
        results = {}
        
        print("\n[阶段1] 简历解析...")
        parser_result = self.resume_parser.execute({"resume_text": resume_text})
        results["parsed_resume"] = parser_result["data"]
        self._log_workflow(parser_result)
        
        print("\n[阶段2] 岗位匹配...")
        matcher_result = self.job_matcher.execute({
            "parsed_resume": results["parsed_resume"],
            "job_requirements": job_requirements
        })
        results["match_data"] = matcher_result["data"]
        self._log_workflow(matcher_result)
        
        print("\n[阶段3] 生成面试问题...")
        question_result = self.question_generator.execute({
            "parsed_resume": results["parsed_resume"],
            "job_requirements": job_requirements,
            "match_data": results["match_data"]
        })
        results["interview_questions"] = question_result["data"]
        self._log_workflow(question_result)
        
        if interview_answers is None:
            interview_answers = self._generate_sample_answers(results["interview_questions"]["questions"])
        
        print("\n[阶段4] 面试评估...")
        evaluation_result = self.interview_evaluator.execute({
            "interview_answers": interview_answers
        })
        results["evaluation_data"] = evaluation_result["data"]
        self._log_workflow(evaluation_result)
        
        print("\n[阶段5] 决策推荐（长链推理）...")
        decision_result = self.decision_maker.execute({
            "parsed_resume": results["parsed_resume"],
            "match_data": results["match_data"],
            "evaluation_data": results["evaluation_data"]
        })
        results["decision_data"] = decision_result["data"]
        self._log_workflow(decision_result)
        
        print("\n" + "=" * 60)
        print("招聘流程完成！")
        print("=" * 60)
        
        return results

    def _log_workflow(self, agent_result: Dict):
        self.workflow_log.append({
            "agent": agent_result["agent"],
            "status": agent_result["status"]
        })
        print(f"[OK] {agent_result['agent']} 执行完成")

    def _generate_sample_answers(self, questions: list) -> list:
        answers = []
        for q in questions:
            answer = f"这是一个很好的问题。关于{q['question'][:20]}...，我认为应该从以下几个方面考虑：首先，明确问题的核心；其次，制定详细的计划；然后，逐步执行并及时调整；最后，总结经验教训。在我过去的项目中，我曾经遇到过类似的情况，通过这种方法成功地解决了问题。"
            answers.append({
                "question": q["question"],
                "answer": answer
            })
        return answers

    def print_summary(self, results: Dict):
        print("\n" + "=" * 60)
        print("招聘评估报告摘要")
        print("=" * 60)
        
        parsed = results["parsed_resume"]
        print(f"\n候选人: {parsed['name']}")
        print(f"学历: {', '.join(parsed['education'])}")
        print(f"技能: {', '.join(parsed['skills'])}")
        
        match = results["match_data"]
        print(f"\n岗位匹配度: {match['match_score']}分 ({match['match_level']})")
        print("匹配理由:")
        for reason in match["match_reasons"]:
            print(f"  - {reason}")
        
        eval_data = results["evaluation_data"]
        print(f"\n面试综合得分: {eval_data['overall_score']}分")
        print("各维度评分:")
        for dim, score in eval_data["dimension_scores"].items():
            print(f"  - {dim}: {score}分")
        
        decision = results["decision_data"]["recommendation"]
        print(f"\n最终推荐: {decision['decision']}")
        print(f"综合评分: {decision['total_score']}分")
        print(f"薪资建议: {decision['salary_suggestion']}")
        print(f"置信度: {decision['confidence']}")
        
        if decision["probation_focus"]:
            print("试用期关注重点:")
            for focus in decision["probation_focus"]:
                print(f"  - {focus}")
        
        print("\n长链推理过程:")
        for step in results["decision_data"]["reasoning_chain"]:
            print(f"  {step}")

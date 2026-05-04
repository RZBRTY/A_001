from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import uvicorn
from orchestrator import RecruitingOrchestrator


app = FastAPI(title="智能招聘多Agent系统", version="1.0.0")

orchestrator = RecruitingOrchestrator()


class InterviewAnswer(BaseModel):
    question: str
    answer: str


class RecruitingRequest(BaseModel):
    resume_text: str
    job_title: str
    job_description: str
    required_skills: List[str] = []
    interview_answers: Optional[List[InterviewAnswer]] = None


@app.get("/")
async def root():
    html_content = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎯 智能招聘多Agent系统</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        .header {
            text-align: center;
            color: white;
            padding: 40px 20px;
        }
        .header h1 { font-size: 3em; margin-bottom: 10px; }
        .header p { font-size: 1.2em; opacity: 0.9; }
        .grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        @media (max-width: 1000px) {
            .grid { grid-template-columns: 1fr; }
        }
        .card {
            background: white;
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }
        .input-section { margin-bottom: 20px; }
        .input-section label {
            display: block;
            font-weight: 600;
            margin-bottom: 8px;
            color: #333;
        }
        .input-section input, .input-section textarea {
            width: 100%;
            padding: 12px 16px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        .input-section input:focus, .input-section textarea:focus {
            outline: none;
            border-color: #11998e;
        }
        .input-section textarea {
            min-height: 120px;
            resize: vertical;
        }
        .btn {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
            border: none;
            padding: 14px 32px;
            font-size: 18px;
            font-weight: 600;
            border-radius: 8px;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            width: 100%;
        }
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(17,153,142,0.4);
        }
        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        .agent-workflow {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 10px;
            margin-top: 20px;
        }
        @media (max-width: 1000px) {
            .agent-workflow { grid-template-columns: repeat(2, 1fr); }
        }
        .agent-node {
            background: #f8f9fa;
            border-radius: 12px;
            padding: 15px;
            text-align: center;
            border: 3px solid transparent;
            transition: all 0.3s;
        }
        .agent-node.active {
            border-color: #11998e;
            background: #ecfdf5;
            animation: pulse 1s infinite;
        }
        .agent-node.completed {
            border-color: #10b981;
            background: #ecfdf5;
        }
        .agent-icon {
            font-size: 32px;
            margin-bottom: 8px;
        }
        .agent-name {
            font-weight: 600;
            color: #333;
            font-size: 14px;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        .results-section { display: none; margin-top: 20px; }
        .results-section.show { display: block; }
        .decision-card {
            text-align: center;
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 20px;
        }
        .decision-hire {
            background: linear-gradient(135deg, #10b981, #059669);
            color: white;
        }
        .decision-wait {
            background: linear-gradient(135deg, #f59e0b, #d97706);
            color: white;
        }
        .decision-reject {
            background: linear-gradient(135deg, #ef4444, #dc2626);
            color: white;
        }
        .decision-title { font-size: 1.5em; font-weight: bold; margin-bottom: 10px; }
        .decision-score { font-size: 3em; font-weight: bold; }
        .tab-buttons {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
        .tab-btn {
            padding: 10px 20px;
            border: none;
            background: #e0e0e0;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
        }
        .tab-btn.active {
            background: #11998e;
            color: white;
        }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        pre {
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            max-height: 400px;
            overflow-y: auto;
            font-size: 13px;
        }
        .score-row {
            display: flex;
            justify-content: space-between;
            padding: 12px 0;
            border-bottom: 1px solid #eee;
        }
        .score-label { font-weight: 600; }
        .score-value { font-weight: bold; color: #11998e; }
        .reason-item {
            background: #f0fdf4;
            border-left: 4px solid #10b981;
            padding: 12px;
            margin-bottom: 8px;
            border-radius: 0 8px 8px 0;
        }
        .question-item {
            background: #fef3c7;
            border-left: 4px solid #f59e0b;
            padding: 12px;
            margin-bottom: 8px;
            border-radius: 0 8px 8px 0;
        }
        .question-type {
            display: inline-block;
            background: #f59e0b;
            color: white;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 600;
            margin-right: 8px;
        }
        .reasoning-step {
            padding: 10px;
            border-left: 3px solid #11998e;
            margin-bottom: 8px;
            padding-left: 15px;
            background: #f8f9fa;
            border-radius: 0 8px 8px 0;
        }
        .focus-item {
            display: inline-block;
            background: #dbeafe;
            color: #1e40af;
            padding: 6px 12px;
            border-radius: 20px;
            margin: 4px;
            font-size: 14px;
        }
        .sample-btn {
            background: #6366f1;
            margin-top: 10px;
        }
        .sample-btn:hover {
            box-shadow: 0 5px 20px rgba(99,102,241,0.4);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 智能招聘多Agent系统</h1>
            <p>基于多Agent协作的全流程智能招聘解决方案</p>
        </div>
        
        <div class="grid">
            <div class="card">
                <h2 style="margin-bottom: 20px; color: #333;">📄 候选人简历</h2>
                <div class="input-section">
                    <textarea id="resumeText" placeholder="请输入简历文本，例如：&#10;姓名: 张明&#10;教育背景: 某某大学 计算机科学与技术 硕士&#10;工作经验: 5年Python开发经验&#10;技能: Python, MySQL, 机器学习"></textarea>
                </div>
                <button class="btn sample-btn" onclick="fillSampleResume()">📋 填入示例简历</button>
            </div>
            
            <div class="card">
                <h2 style="margin-bottom: 20px; color: #333;">💼 岗位要求</h2>
                <div class="input-section">
                    <label for="jobTitle">岗位名称</label>
                    <input type="text" id="jobTitle" placeholder="例如：高级算法工程师">
                </div>
                <div class="input-section">
                    <label for="jobDescription">岗位描述</label>
                    <textarea id="jobDescription" placeholder="请描述岗位要求..."></textarea>
                </div>
                <div class="input-section">
                    <label for="requiredSkills">技能要求 (逗号分隔)</label>
                    <input type="text" id="requiredSkills" placeholder="例如：Python, 机器学习, MySQL">
                </div>
                <button class="btn sample-btn" onclick="fillSampleJob()">📋 填入示例岗位</button>
            </div>
        </div>
        
        <div class="card">
            <button class="btn" id="generateBtn" onclick="startRecruiting()">✨ 启动招聘评估流程</button>
        </div>
        
        <div class="card" id="workflowCard" style="display: none;">
            <h2 style="margin-bottom: 20px; color: #333;">🤖 Agent协作工作流</h2>
            <div class="agent-workflow" id="agentWorkflow">
                <div class="agent-node" id="agent1">
                    <div class="agent-icon">📄</div>
                    <div class="agent-name">简历解析Agent</div>
                </div>
                <div class="agent-node" id="agent2">
                    <div class="agent-icon">🎯</div>
                    <div class="agent-name">岗位匹配Agent</div>
                </div>
                <div class="agent-node" id="agent3">
                    <div class="agent-icon">❓</div>
                    <div class="agent-name">面试问题Agent</div>
                </div>
                <div class="agent-node" id="agent4">
                    <div class="agent-icon">📊</div>
                    <div class="agent-name">面试评估Agent</div>
                </div>
                <div class="agent-node" id="agent5">
                    <div class="agent-icon">🤔</div>
                    <div class="agent-name">决策推荐Agent</div>
                </div>
            </div>
        </div>
        
        <div class="card results-section" id="resultsCard">
            <h2 style="margin-bottom: 20px; color: #333;">📋 评估结果</h2>
            <div id="decisionCard" class="decision-card">
                <div class="decision-title" id="decisionTitle">--</div>
                <div class="decision-score" id="decisionScore">--</div>
                <div id="salarySuggestion"></div>
                <div id="probationFocus" style="margin-top: 15px;"></div>
            </div>
            
            <div class="tab-buttons">
                <button class="tab-btn active" onclick="showTab('resume')">📄 简历解析</button>
                <button class="tab-btn" onclick="showTab('matching')">🎯 岗位匹配</button>
                <button class="tab-btn" onclick="showTab('questions')">❓ 面试问题</button>
                <button class="tab-btn" onclick="showTab('evaluation')">📊 面试评估</button>
                <button class="tab-btn" onclick="showTab('reasoning')">🤔 推理过程</button>
            </div>
            
            <div class="tab-content active" id="resume">
                <pre id="resumeContent"></pre>
            </div>
            <div class="tab-content" id="matching">
                <div id="matchingScore"></div>
                <div id="matchingReasons"></div>
            </div>
            <div class="tab-content" id="questions">
                <div id="questionsContent"></div>
            </div>
            <div class="tab-content" id="evaluation">
                <div id="evaluationContent"></div>
            </div>
            <div class="tab-content" id="reasoning">
                <div id="reasoningContent"></div>
            </div>
        </div>
    </div>

    <script>
        let currentResult = null;
        
        function fillSampleResume() {
            document.getElementById('resumeText').value = `姓名: 张明
教育背景: 某某大学 计算机科学与技术 硕士
工作经验: 5年Python开发经验，3年机器学习项目经验
技能: Python, Java, MySQL, Redis, Docker, 机器学习, 数据分析
项目经验: 主导过多个电商推荐系统项目，参与过大数据平台建设`;
        }
        
        function fillSampleJob() {
            document.getElementById('jobTitle').value = '高级算法工程师';
            document.getElementById('jobDescription').value = '负责推荐算法研发，需要团队协作能力';
            document.getElementById('requiredSkills').value = 'Python, 机器学习, 数据分析, MySQL, Redis';
        }
        
        async function startRecruiting() {
            const resumeText = document.getElementById('resumeText').value;
            const jobTitle = document.getElementById('jobTitle').value;
            const jobDescription = document.getElementById('jobDescription').value;
            const requiredSkills = document.getElementById('requiredSkills').value.split(',').map(s => s.trim()).filter(s => s);
            
            if (!resumeText || !jobTitle) {
                alert('请填写简历和岗位信息！');
                return;
            }
            
            const btn = document.getElementById('generateBtn');
            btn.disabled = true;
            btn.textContent = '⏳ 评估中...';
            
            document.getElementById('workflowCard').style.display = 'block';
            document.getElementById('resultsCard').classList.remove('show');
            
            try {
                for (let i = 1; i <= 5; i++) {
                    setTimeout(() => {
                        document.getElementById('agent' + i).classList.add('active');
                    }, i * 800);
                }
                
                const response = await fetch('/api/recruit', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        resume_text: resumeText,
                        job_title: jobTitle,
                        job_description: jobDescription,
                        required_skills: requiredSkills
                    })
                });
                
                currentResult = await response.json();
                
                for (let i = 1; i <= 5; i++) {
                    document.getElementById('agent' + i).classList.remove('active');
                    document.getElementById('agent' + i).classList.add('completed');
                }
                
                showResults(currentResult);
                
            } catch (error) {
                console.error(error);
                alert('评估过程出错，请重试！');
            } finally {
                btn.disabled = false;
                btn.textContent = '✨ 启动招聘评估流程';
            }
        }
        
        function showResults(result) {
            document.getElementById('resultsCard').classList.add('show');
            
            const decision = result.decision_data?.recommendation;
            const decisionCard = document.getElementById('decisionCard');
            decisionCard.className = 'decision-card';
            
            if (decision?.decision?.includes('强烈推荐') || decision?.decision?.includes('推荐录用')) {
                decisionCard.classList.add('decision-hire');
            } else if (decision?.decision?.includes('待定')) {
                decisionCard.classList.add('decision-wait');
            } else {
                decisionCard.classList.add('decision-reject');
            }
            
            document.getElementById('decisionTitle').textContent = decision?.decision || '--';
            document.getElementById('decisionScore').textContent = decision?.total_score + '分' || '--';
            document.getElementById('salarySuggestion').textContent = decision?.salary_suggestion || '';
            
            const focusHtml = (decision?.probation_focus || []).map(f => 
                `<span class="focus-item">${f}</span>`
            ).join('');
            document.getElementById('probationFocus').innerHTML = focusHtml;
            
            document.getElementById('resumeContent').textContent = 
                JSON.stringify(result.parsed_resume, null, 2);
            
            const matchData = result.match_data;
            document.getElementById('matchingScore').innerHTML = `
                <div class="score-row">
                    <span class="score-label">匹配得分</span>
                    <span class="score-value">${matchData?.match_score}分 (${matchData?.match_level})</span>
                </div>
            `;
            document.getElementById('matchingReasons').innerHTML = (matchData?.match_reasons || []).map(r =>
                `<div class="reason-item">${r}</div>`
            ).join('');
            
            document.getElementById('questionsContent').innerHTML = (result.interview_questions?.questions || []).map(q =>
                `<div class="question-item"><span class="question-type">${q.type}</span>${q.question}</div>`
            ).join('');
            
            const evalData = result.evaluation_data;
            const scoresHtml = Object.entries(evalData?.dimension_scores || {}).map(([k, v]) =>
                `<div class="score-row"><span class="score-label">${k}</span><span class="score-value">${v}分</span></div>`
            ).join('');
            document.getElementById('evaluationContent').innerHTML = `
                <div class="score-row"><span class="score-label">综合得分</span><span class="score-value">${evalData?.overall_score}分</span></div>
                ${scoresHtml}
                <h4 style="margin-top: 20px;">评估反馈</h4>
                ${(evalData?.feedback || []).map(f => `<div class="reason-item">${f}</div>`).join('')}
            `;
            
            document.getElementById('reasoningContent').innerHTML = (result.decision_data?.reasoning_chain || []).map(r =>
                `<div class="reasoning-step">${r}</div>`
            ).join('');
        }
        
        function showTab(tabName) {
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
        }
    </script>
</body>
</html>
    """
    return HTMLResponse(content=html_content)


@app.post("/api/recruit")
async def recruit(request: RecruitingRequest):
    try:
        job_requirements = {
            "title": request.job_title,
            "description": request.job_description,
            "required_skills": request.required_skills
        }
        
        interview_answers = None
        if request.interview_answers:
            interview_answers = [a.dict() for a in request.interview_answers]
        
        results = orchestrator.run_full_recruiting_process(
            resume_text=request.resume_text,
            job_requirements=job_requirements,
            interview_answers=interview_answers
        )
        
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    print("🎯 启动智能招聘多Agent系统...")
    print("📝 访问地址: http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)

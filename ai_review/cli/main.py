from analyzers.ast_parser import ASTAnalyzer
from rules import style, security

def code_review(file_path):
    # AST解析
    with open(file_path) as f:
        tree = ast.parse(f.read())
    
    # 执行静态分析
    analyzer = ASTAnalyzer()
    analyzer.visit(tree)
    
    # 应用规则检查
    style_violations = StyleRules.check_naming_convention(tree)
    security_issues = SecurityRules.check_injection(tree)
    
    # AI增强审查
    if config['ai']['enable']:
        ai_reviewer = AICodeReviewer(config['ai']['api_key'])
        ai_suggestions = ai_reviewer.get_optimization_suggestion(code_snippet)
    
    # 生成报告
    generate_report({
        'static_analysis': analyzer.findings,
        'style_violations': style_violations,
        'ai_suggestions': ai_suggestions
    })
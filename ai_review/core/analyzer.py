from typing import Dict, List
from .parser import ASTParser

class CodeAnalyzer:
    def __init__(self, rule_modules: List[str]):
        self.rules = self._load_rules(rule_modules)
        
    def _load_rules(self, modules) -> Dict:
        """动态加载规则检测器"""
        return {rule_name: getattr(__import__(mod), rule_name) 
                for mod in modules 
                for rule_name in dir(mod) 
                if callable(getattr(mod, rule_name)) and not rule_name.startswith('_')}

    def analyze(self, code: str) -> List[dict]:
        """执行多维度代码审查"""
        ast_parser = ASTParser(code)
        findings = []
        
        # 执行静态规则检查
        for rule_name, check_func in self.rules.items():
            if issues := check_func(ast_parser.tree):
                findings.extend({
                    'rule': rule_name,
                    'message': issue['msg'],
                    'severity': issue['level'],
                    'line': issue['lineno']
                } for issue in issues)
        
        return findings
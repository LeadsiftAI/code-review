from typing import Dict, List
from .parser import ASTParser

import importlib
from typing import Dict, List, Callable

class CodeAnalyzer:
    def __init__(self, rule_modules: List[str]):
        """Initialize the analyzer with rule modules."""
        if not rule_modules:
            raise ValueError("No rule modules specified")
        self.rules = self._load_rules(rule_modules)
        
    def _load_rules(self, modules: List[str]) -> Dict[str, Callable]:
        """动态加载规则检测器"""
        rules = {}
        for module_name in modules:
            try:
                module = importlib.import_module(module_name)
                for rule_name in dir(module):
                    if rule_name.startswith('_'):
                        continue
                    rule = getattr(module, rule_name)
                    if callable(rule):
                        rules[rule_name] = rule
            except ImportError as e:
                raise ImportError(f"Failed to import rule module {module_name}: {e}")
            except Exception as e:
                raise RuntimeError(f"Error loading rules from {module_name}: {e}")
        return rules
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
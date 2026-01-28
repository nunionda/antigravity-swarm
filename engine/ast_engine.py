"""
Omni-Scribe AST Engine
Optimized for high-speed source code parsing and AST extraction.
"""
import ast
import time
from typing import Dict, Any
from utils.hpc_utils import HPCUtils

class ASTEngine:
    @HPCUtils.benchmark_latency
    def parse_source(self, source_code: str, file_path: str = "unknown") -> Dict[str, Any]:
        """
        Parses source code into a structured AST representation.
        In a production version, this would use a faster parser (like tree-sitter)
        bound with C/C++ via the 128-bit protocol.
        """
        try:
            tree = ast.parse(source_code)
            ast_data = self._summarize_tree(tree)
            return {
                "file": file_path,
                "timestamp": time.time(),
                "nodes": ast_data,
                "status": "PARSED"
            }
        except SyntaxError as e:
            return {"file": file_path, "status": "ERROR", "message": str(e)}

    def _summarize_tree(self, tree: ast.AST) -> Dict[str, Any]:
        """
        Extracts key metadata from the AST for the shared memory bus.
        """
        summary = {
            "functions": [],
            "classes": [],
            "imports": []
        }
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                summary["functions"].append(node.name)
            elif isinstance(node, ast.ClassDef):
                summary["classes"].append(node.name)
            elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                summary["imports"].append(ast.dump(node))
                
        return summary

if __name__ == "__main__":
    engine = ASTEngine()
    test_code = """
def hello():
    print("World")

class Greeter:
    def __init__(self):
        pass
"""
    result = engine.parse_source(test_code)
    print(f"[AST] Parsed functions: {result['nodes']['functions']}")

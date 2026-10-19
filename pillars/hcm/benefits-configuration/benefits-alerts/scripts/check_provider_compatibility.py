"""Read-only provider transport check. No imports of provider code or live calls."""
import ast
import inspect
import json
from pathlib import Path
import sys


def check_transport(transport_source, adapter_source):
    functions = [n for n in ast.parse(transport_source).body
                 if isinstance(n, ast.FunctionDef) and n.name == "request_bytes"]
    if len(functions) != 1:
        raise ValueError("Shared transport signature could not be resolved.")
    args = functions[0].args
    parameters = []
    positional = args.posonlyargs + args.args
    required_count = len(positional) - len(args.defaults)
    for i, arg in enumerate(positional):
        kind = (inspect.Parameter.POSITIONAL_ONLY if i < len(args.posonlyargs)
                else inspect.Parameter.POSITIONAL_OR_KEYWORD)
        parameters.append(inspect.Parameter(arg.arg, kind,
                          default=inspect.Parameter.empty if i < required_count else None))
    if args.vararg:
        parameters.append(inspect.Parameter(args.vararg.arg, inspect.Parameter.VAR_POSITIONAL))
    for arg, default in zip(args.kwonlyargs, args.kw_defaults):
        parameters.append(inspect.Parameter(arg.arg, inspect.Parameter.KEYWORD_ONLY,
                          default=inspect.Parameter.empty if default is None else None))
    if args.kwarg:
        parameters.append(inspect.Parameter(args.kwarg.arg, inspect.Parameter.VAR_KEYWORD))
    signature = inspect.Signature(parameters)
    calls = [n for n in ast.walk(ast.parse(adapter_source))
             if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
             and n.func.id == "request_bytes"]
    if not calls:
        raise ValueError("Provider transport call could not be resolved.")
    for call in calls:
        if any(isinstance(a, ast.Starred) for a in call.args) or any(k.arg is None for k in call.keywords):
            raise ValueError("Dynamic provider call requires compatibility review.")
        try:
            signature.bind(*([None] * len(call.args)), **{k.arg: None for k in call.keywords})
        except TypeError as exc:
            raise ValueError("Provider/shared transport signature mismatch: " + str(exc)) from exc


def main():
    root = Path(__file__).resolve().parents[5]
    provider = root / "pillars/hcm/hcm-tool/alert-foundation/scripts/execute-alert-mutation.py"
    transport = root / "core/fusion-api/rest-api-client/scripts/rest_client_common.py"
    try:
        check_transport(transport.read_text(), provider.read_text())
    except (OSError, SyntaxError, ValueError) as exc:
        print(json.dumps({"status": "blocked", "failure_class": "provider_compatibility",
                          "message": str(exc), "submitted": False}))
        return 1
    print(json.dumps({"status": "transport_signature_compatible",
                      "note": "Provider contract, runtime gates, and approval still required."}))
    return 0


if __name__ == "__main__":
    sys.exit(main())

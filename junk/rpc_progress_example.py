import argparse
import bootstrap as bs
import json
from src.core.rpc.client import call_with_progress

parser = argparse.ArgumentParser(description="RPC call example")
parser.add_argument('success', help="1/0 - return success result or simulate error")
args = parser.parse_args()

result = call_with_progress('http://localhost:%i/examples-rpc-progress' % bs.SERVER_PORT, json.dumps({"success": bool(int(args.success))}), lambda p: print(p))

print(result)
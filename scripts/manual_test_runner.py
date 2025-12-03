"""
Quick sanity checks for the refactored process-isolated runner.

Scenarios:
1) Legacy mode (no ProcessContext) using ./data.
2) Isolated single run with its own process_id.
3) Two isolated runs concurrently to check for collisions.

Optional MCP/Data Analyst path:
- Drop a dataset (csv/xls/xlsx) into data/uploaded/<file>.
- Ensure your MCP Jupyter server is running at http://127.0.0.1:4040/mcp.
- The dataset branch triggers only if a dataset is present.
"""


import asyncio, shutil
from pathlib import Path
from core.process_context import ProcessContext
from core.new_agent_architecture import the_runner



files_to_use = [
    "data/uploaded/ssrn-5233576.pdf",
    "data/uploaded/inflation-interest-rate-and-unemployment.ipynb",
    "data/uploaded/inflation.csv"]


async def main():
    with ProcessContext(process_id="upload-test", cleanup=False) as ctx:
        for f in files_to_use:
            src = Path(f)
            if src.exists():
                shutil.copy(src, ctx.uploaded_dir / src.name)
            else:
                print(f" Missing: {src}")
        result = await the_runner(
            user_query="Create a presentation on inflation , unemployment and interest rates",
            num_slides=5,
            process_context=ctx,
        )
        print("Result:", result)



async def concurrent_runs():
    async def run_one(pid: str):
        with ProcessContext(process_id=pid, cleanup=True) as ctx:
            for f in files_to_use:
                src = Path(f)
                if src.exists():
                    shutil.copy(src, ctx.uploaded_dir / src.name)
            return await the_runner(
                user_query=f"Create a presentation on inflation, unemployment and interest rates ({pid})",
                num_slides=5,
                process_context=ctx,
            )


    results = await asyncio.gather(
        run_one("upload-parallel-A"),
        run_one("upload-parallel-B"),
    )
    for res in results:
        print("Concurrent result:", res)



if __name__ == "__main__":
    asyncio.run(concurrent_runs())

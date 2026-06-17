import os
import re

root_dir = "insuredaily.github.io"
js_tag = """<script type="text/javascript">
    aclib.runAutoTag({
        zoneId: 'qyrn8d3vem',
    });
</script>"""

for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            
            if "qyrn8d3vem" not in content:
                content = re.sub(
                    r'(</body>)',
                    lambda m: f"{js_tag}\n{m.group(1)}",
                    content,
                    flags=re.IGNORECASE
                )
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"Injected aclib script into {path}")
            else:
                print(f"Already verified in {path}")

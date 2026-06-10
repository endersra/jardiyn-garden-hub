/* server.mjs — minimal static server for the JarDIYn demo. No dependencies. */
import { createServer } from "http";
import { readFile } from "fs/promises";
import { extname, join } from "path";

const ROOT = join(process.cwd(), "src");
const PORT = process.env.PORT || 8080;
const TYPES = { ".html":"text/html", ".js":"text/javascript", ".css":"text/css",
  ".json":"application/json", ".mjs":"text/javascript" };

createServer(async (req, res) => {
  let path = req.url === "/" ? "/index.html" : req.url.split("?")[0];
  try {
    const data = await readFile(join(ROOT, path));
    res.writeHead(200, { "Content-Type": TYPES[extname(path)] || "text/plain" });
    res.end(data);
  } catch {
    res.writeHead(404); res.end("Not found");
  }
}).listen(PORT, () => console.log(`JarDIYn demo running at http://localhost:${PORT}`));

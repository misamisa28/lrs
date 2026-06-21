import { chromium } from 'playwright';
import { mkdir } from 'fs/promises';
import { spawn } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const outDir = path.join(root, '图片');
const PORT = 8765;

const shots = [
  {
    file: '01-赛季排行.png',
    async setup(page) {
      await page.click('[data-view="bar"]');
    },
  },
  {
    file: '02-个人数据-详细数据.png',
    async setup(page) {
      await page.click('[data-view="radar"]');
      await page.click('[data-radar-mode="table"]');
    },
  },
  {
    file: '03-个人数据-雷达图.png',
    async setup(page) {
      await page.click('[data-view="radar"]');
      await page.click('[data-radar-mode="radar"]');
    },
  },
  {
    file: '04-个人数据-胜率.png',
    async setup(page) {
      await page.click('[data-view="radar"]');
      await page.click('[data-radar-mode="winrate"]');
    },
  },
  {
    file: '05-个人数据-参与场次.png',
    async setup(page) {
      await page.click('[data-view="radar"]');
      await page.click('[data-radar-mode="games"]');
    },
  },
  {
    file: '06-赛季对比.png',
    async setup(page) {
      await page.click('[data-view="compare"]');
    },
  },
  {
    file: '07-版型统计.png',
    async setup(page) {
      await page.click('[data-view="banxing"]');
    },
  },
  {
    file: '08-同边数据.png',
    async setup(page) {
      await page.click('[data-view="tongbian"]');
    },
  },
  {
    file: '09-原始数据.png',
    async setup(page) {
      await page.click('[data-view="table"]');
    },
  },
];

function startServer() {
  return spawn('python', ['-m', 'http.server', String(PORT)], {
    cwd: root,
    stdio: 'ignore',
    shell: true,
  });
}

async function waitForApp(page) {
  await page.goto(`http://127.0.0.1:${PORT}/index.html`, { waitUntil: 'networkidle' });
  await page.waitForSelector('#nameSelect option[value="JY"]', { timeout: 60000 });
  await page.waitForFunction(() => {
    const err = document.getElementById('error');
    return !err || err.style.display === 'none';
  }, { timeout: 60000 });
  await page.waitForTimeout(2500);
}

const server = startServer();
await new Promise((resolve) => setTimeout(resolve, 1200));

try {
  await mkdir(outDir, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1400, height: 900 } });
  await waitForApp(page);

  for (const shot of shots) {
    await shot.setup(page);
    await page.waitForTimeout(2500);
    await page.screenshot({
      path: path.join(outDir, shot.file),
      fullPage: true,
    });
    console.log(`saved ${shot.file}`);
  }

  await browser.close();
} finally {
  server.kill();
}

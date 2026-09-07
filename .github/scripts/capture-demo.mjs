import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';

const baseUrl = process.env.DEMO_BASE_URL ?? 'http://127.0.0.1:8000';
const outputDir = path.resolve('assets/demo');
const videoDir = path.resolve('assets/demo-video');
fs.mkdirSync(outputDir, { recursive: true });
fs.mkdirSync(videoDir, { recursive: true });

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({
  viewport: { width: 1440, height: 1000 },
  recordVideo: { dir: videoDir, size: { width: 1200, height: 820 } },
});
const page = await context.newPage();

await page.goto(baseUrl, { waitUntil: 'networkidle' });
await page.locator('#healthStatus').filter({ hasText: 'API online' }).waitFor();
await page.screenshot({
  path: path.join(outputDir, 'safe-agent-playground.png'),
  fullPage: true,
});

const scenarios = [
  ['Cross-tenant deny', 'tenant_mismatch'],
  ['Needs approval', 'human_approval_required'],
  ['Approved action', 'policy_allowed'],
  ['Blocked delete', 'destructive_tool_disabled_in_demo'],
];

for (const [buttonName, reason] of scenarios) {
  await page.getByRole('button', { name: buttonName }).click();
  await page.locator('#reason').filter({ hasText: reason }).waitFor();
  await page.waitForTimeout(700);
}

const video = page.video();
await context.close();
await browser.close();

if (!video) {
  throw new Error('Playwright did not produce a demo video');
}

const videoPath = await video.path();
console.log(`DEMO_VIDEO_PATH=${videoPath}`);

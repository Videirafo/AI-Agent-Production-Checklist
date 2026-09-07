import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';

const baseUrl = process.env.DEMO_BASE_URL ?? 'http://127.0.0.1:8000';
const outputDir = path.resolve('assets/demo');
const frameDir = path.resolve('assets/demo-frames');
fs.mkdirSync(outputDir, { recursive: true });
fs.mkdirSync(frameDir, { recursive: true });

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1440, height: 1000 } });
const page = await context.newPage();

await page.addInitScript(() => {
  Object.defineProperty(Crypto.prototype, 'randomUUID', {
    configurable: true,
    value: () => '00000000-0000-4000-8000-000000000001',
  });
});

await page.goto(baseUrl, { waitUntil: 'networkidle' });
await page.locator('#healthStatus').filter({ hasText: 'API online' }).waitFor();

async function captureFrame(index) {
  await page.screenshot({
    path: path.join(frameDir, `frame-${String(index).padStart(2, '0')}.png`),
    fullPage: true,
  });
}

await page.screenshot({
  path: path.join(outputDir, 'safe-agent-playground.png'),
  fullPage: true,
});
await captureFrame(1);

const scenarios = [
  ['Cross-tenant deny', 'tenant_mismatch'],
  ['Needs approval', 'human_approval_required'],
  ['Approved action', 'policy_allowed'],
  ['Blocked delete', 'destructive_tool_disabled_in_demo'],
];

let frame = 2;
for (const [buttonName, reason] of scenarios) {
  await page.getByRole('button', { name: buttonName }).click();
  await page.locator('#reason').filter({ hasText: reason }).waitFor();
  await page.waitForTimeout(250);
  await captureFrame(frame++);
}

await context.close();
await browser.close();

console.log(`DEMO_FRAMES=${frameDir}`);

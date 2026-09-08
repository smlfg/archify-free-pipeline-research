// Check the real local report without adding a browser dependency.
import fs from 'node:fs';
import path from 'node:path';
import {pathToFileURL} from 'node:url';

const [directory, archify] = process.argv.slice(2).map(p => path.resolve(p));
const {ChromeVisualBrowser, findChrome} = await import(pathToFileURL(path.join(archify, 'bin/visual-check.mjs')));
const receipt = {status: 'skipped', viewportChecks: [], interactions: [], perceptualReview: 'not_run'};
let browser;
try {
  const chrome = findChrome();
  if (!chrome) throw new Error('Chrome unavailable');
  browser = new ChromeVisualBrowser(chrome);
  const session = await browser.sessionPromise;
  const evaluate = async expression => {
    const r = await browser.cdp.send('Runtime.evaluate', {expression, returnByValue: true, awaitPromise: true}, session);
    if (r.exceptionDetails) throw new Error(JSON.stringify(r.exceptionDetails));
    return r.result.value;
  };
  for (const [width,height] of [[1440,900],[1600,1000],[1920,1080],[2048,1320]]) {
    await browser.cdp.send('Emulation.setDeviceMetricsOverride', {width,height,deviceScaleFactor:1,mobile:false},session);
    const loaded=browser.cdp.waitFor('Page.loadEventFired',session);
    await browser.cdp.send('Page.navigate',{url:pathToFileURL(path.join(directory,'index.html')).href},session);
    await loaded;
    const metrics=await evaluate(`({tabs:document.querySelectorAll('[role=tab]').length, overflow:document.documentElement.scrollWidth>innerWidth})`);
    receipt.viewportChecks.push({width,height,...metrics});
    if(metrics.tabs!==5 || metrics.overflow) throw new Error('Report tabs/overflow check failed');
  }
  for (const view of ['architecture','workflow','sequence','dataflow','lifecycle']) {
    const result=await evaluate(`(()=>{const tab=document.querySelector('[data-view="${view}"]');tab.click();const panel=document.getElementById('view-${view}');const select=panel.querySelector('select');if(select){select.selectedIndex=select.options.length-1;select.dispatchEvent(new Event('change'));}return {view:'${view}',active:!panel.hidden,selected:tab.getAttribute('aria-selected'),visibleEntities:panel.querySelectorAll('article:not([hidden])').length,hasSelector:!!select};})()`);
    if(!result.active || result.selected!=='true' || (result.hasSelector && result.visibleEntities!==1)) throw new Error('Tab/selector interaction failed');
    receipt.interactions.push(result);
  }
  await evaluate(`document.querySelector('[data-view="architecture"]').click()`);
  const screenshot = await browser.cdp.send('Page.captureScreenshot',{format:'png',captureBeyondViewport:false},session);
  fs.writeFileSync(path.join(directory,'report-browser.png'),Buffer.from(screenshot.data,'base64'));
  const link=await evaluate(`document.querySelector('a[href="evidence.html"]').href`);
  const loaded=browser.cdp.waitFor('Page.loadEventFired',session);
  await browser.cdp.send('Page.navigate',{url:link},session);await loaded;
  if(!await evaluate(`document.querySelectorAll('pre').length>0`)) throw new Error('Missing source excerpts');
  receipt.status='passed';
} catch(error) {
  receipt.status=browser?'failed':'skipped';receipt.error=String(error);
} finally {
  if(browser) await browser.close();
  fs.writeFileSync(path.join(directory,'report-browser.json'),JSON.stringify(receipt,null,2)+'\n');
}
console.log(JSON.stringify(receipt));
process.exitCode=receipt.status==='passed'?0:2;

import { firefox } from 'playwright';

const sleep = (ms: number) =>
  new Promise((resolve) => setTimeout(resolve, ms));

(async () => {
    const browser = await firefox.launch({headless:false});
    // Create pages, interact with UI elements, assert values
    await sleep(5000);
    await browser.close();
  })();
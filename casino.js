const endpoint = 'http://127.0.0.1:5000/api/roulette';

const configuration = {
    interval: 15000,
};


const selectors = {
    numbers: 'div[class*="number-container"] span',
    arrow: 'div[class*="statisticsBranding_triangle"]',
    paginatorNumbers: 'div[data-role="paginator-item-numbers"]',
};

const state = {
    values: [],
    running: false,
    timeout: null
};

const getValues = () => {
    const scrapedNumbers = document.querySelectorAll(selectors.numbers);
    return Array.from(scrapedNumbers).map(e => +e.innerText);
};

const loop = async () => {
    if (state.running) {
        const currentValues = getValues();
        state.values = [...currentValues]
    }

    console.log(`Successfully scraped ${state.values.length} items from page.`);

    state.timeout = setTimeout(loop, configuration.interval);

    await postData(endpoint, {numbers: state.values, source: 'grosvenorcasinos'})
};

const postData = async (url, data) => {
    const config = {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        method: "POST",
        body: JSON.stringify(data)
    };

    const response = await fetch(url, config);

    console.log(`Response Status: ${response.ok}`);

    return await response.json()
};

const showHistoryNumbers = () => {
    document.querySelector(selectors.arrow).click();
    document.querySelector(selectors.paginatorNumbers).click();
};

const start = async () => {
    state.running = true;
    showHistoryNumbers();
    await loop()
};

const stop = async () => {
    state.running = false;
    await clearTimeout(state.timeout);
    showHistoryNumbers();
};

await start();

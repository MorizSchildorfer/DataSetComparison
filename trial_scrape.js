const puppeteer = require("puppeteer-extra");
const fs = require('fs')
const unzipper = require("unzipper");
var path = 'search_result.zip'
var count = 1932
function sleep( millisecondsToWait )
{
	var now = new Date().getTime();
	while ( new Date().getTime() < now + millisecondsToWait )
	{
	/* do nothing; this will exit once it reaches the time limit */
	/* if you want you could do something and exit */
	}
}
var dir = process.cwd ()
puppeteer.use(require('puppeteer-extra-plugin-user-preferences')
	(
	{userPrefs: {
	download: {
	behavior: 'allow',
	prompt_for_download: false,
	open_pdf_in_system_reader: true,
	default_directory:dir+"zips",
	},
	plugins: {
	always_open_pdf_externally: true
	},
	}}));
  
async function main() {
  
	
  const browser = await puppeteer.launch({headless: false});
  const page = await browser.newPage();
  await page.setViewport({width: 1200, height: 720});
  page.on('console', consoleObj => console.log(consoleObj.text()));
  //await germanScrape(page)
  await euSearch(page)
}

async function clinicalTrialsScrape(page){
  var year_start = 1999;
  var year_end = 1999;
  var year_limit = 2022;
  var day_start = 1;
  var day_end = 1;
  var month_start = 1;
  var month_end = 1;
  while (year_start<year_limit){
	  
	  day_start = 1;
	  day_end = 4;
	  month_start = 12;
	  month_end = 12;
	  year_start++;
	  year_end++;
	  
	  while (day_end <= 31){
		  let page_string = 'https://clinicaltrials.gov/ct2/results?strd_s='+(day_start)+'%2F'+(month_start)+'%2F'+(year_start)+'&strd_e='+(day_end)+'%2F'+(month_end)+'%2F'+(year_end)
		  let date_string = (day_start)+'/'+(month_start)+'/'+(year_start)+' - '+(day_end)+'/'+(month_end)+'/'+(year_end)
		  await page.goto(page_string, { waitUntil: 'networkidle0' }); // wait until page load
	  
		  y = await page.evaluate((selector) => {
				  //emulate a click on the Account Selection to open the popup
				  var out = []
				  
				  targetElement = document.querySelector('div[id="theDataTable_info"] > b');
				  out = targetElement.innerText
				  targetElement = document.querySelector('a[id="save-list-link"]');
				  
				  targetElement && targetElement.click();
				  
				  return out;
				}, 'tr.rowASRLodd');	  
		  console.log(y);
		  if(parseInt(y)<10000 && parseInt(y)>0){
			  //await downloadResultsFromTrialsPage(page)
		  }
		  else{
			  console.log("Too many: "+y);
		  }
		  day_start+= 3
		  day_end+= 3
		  	  
		  console.log('Date String', date_string);
	  }
  }
  
  
}

async function germanScrape(page){
  var year_start = 2010;
  var year_end = 2011;
  var year_limit = 2022;
  var day_start = 1;
  var day_end = 1;
  var month_start = 1;
  var month_end = 1;
  while (year_start<year_limit){
	  
	  if (year_start < 2016){
		  day_start = 1;
		  day_end = 1;
		  month_start = 1;
		  month_end = 1;
	  }
	  else if (year_start == 2020){
		  day_start = 1;
		  day_end = 1;
		  month_start = 1;
		  month_end = 6;
		  year_end = year_start;
		  await germanSearch(page, day_start+"."+month_start+"."+year_start, day_end+"."+month_end+"."+year_end)
		  
		  day_start = 1;
		  day_end = 1;
		  month_start = 6;
		  month_end = 10;
		  await germanSearch(page, day_start+"."+month_start+"."+year_start, day_end+"."+month_end+"."+year_end)
		  
		  day_start = 1;
		  day_end = 1;
		  month_start = 10;
		  month_end = 12;
		  await germanSearch(page, day_start+"."+month_start+"."+year_start, day_end+"."+month_end+"."+year_end)
		  month_start = 12;
		  year_end++;
		  month_end = 1;
		  
	  }
	  
	  else if (year_start == 2021){
		  day_start = 1;
		  day_end = 1;
		  month_start = 1;
		  month_end = 3;
		  year_end = year_start;
		  await germanSearch(page, day_start+"."+month_start+"."+year_start, day_end+"."+month_end+"."+year_end)
		  
		  day_start = 1;
		  day_end = 1;
		  month_start = 3;
		  month_end = 5;
		  
	  }
	  else{
		  day_start = 1;
		  day_end = 1;
		  month_start = 1;
		  month_end = 7;
		  year_end = year_start;
		  
		  await germanSearch(page, day_start+"."+month_start+"."+year_start, day_end+"."+month_end+"."+year_end)
		  
		  month_start = 7;
		  month_end = 1;
		  year_end++;
		  
	  }
	  
	  await germanSearch(page, day_start+"."+month_start+"."+year_start, day_end+"."+month_end+"."+year_end)
		
	  year_start++;
	  year_end++;
  }
}
  
async function germanSearch(page, start_date, end_date){
	
  console.log('Date String', start_date+" - "+end_date);
  let page_string = 'https://www.drks.de/drks_web/navigate.do?navigationId=search&reset=true#updDateFrom'
  await page.goto(page_string, { waitUntil: 'networkidle0' }); // wait until page load
  
  await page.type("input[name='criteria.updateDateFrom']", start_date);
  await page.type("input[name='criteria.updateDateTo']", end_date);
  y = await page.evaluate(() => {
		  
		  var out = []
		  // Scrape all contact info and names of the stored people
		  targetElement = document.querySelector('input[id="searchExtended"]');
		  
		  // Specifically select Send money on some one with the given Name. As far as I have seen the name matches the contact name 
		  targetElement && targetElement.click();
		  
		  return out;
		});
	
	  await Promise.all([
		page.waitForNavigation({ waitUntil: 'networkidle0' }),
		console.log( 
		  "Waiting for Search Load"
	  ), 
	  ]);
  y = await page.evaluate((selector) => {
		  //emulate a click on the Account Selection to open the popup
		  var out = []
		  
		  targetElement = document.querySelector('li[class="header bgHighlight"]');
		  out = targetElement.innerText.split("|", 1)[0].split("von", 2)[1]
		  targetElement = document.querySelector('button[class="downloadButton"]');
		  
		  targetElement && targetElement.click();
		  
		  return out;
		}, 'tr.rowASRLodd');	  
  console.log(y);
  if(parseInt(y)<1000 && parseInt(y)>0){
	  await downloadResultsFromGermanPage(page)
  }
  else{
	  console.log("Too many: "+y);
  }
  
}


async function downloadResultsFromTrialsPage(page)  {
  
  y = await page.evaluate((selector) => {
		  
		  var out = []
		  function pollDOM () {
			  const el = targetElement = document.querySelector('li > input[value="Download"]');
			  //wait until the popup is loaded in
			  if (el) {
				  targetElement && targetElement.click();
				  return targetElement
			  } else {
				setTimeout(pollDOM, 300); // try again in 300 milliseconds
			  }
		  }
		  targetElement = pollDOM ()
		  
		  return targetElement;
		}, 'tr.rowASRLodd');	
  console.log(y);
  
  var counter = 1
  while (!fs.existsSync(path)) {
    //file exists
	sleep( 100 );
	console.log(counter)
	counter += 1
  }
  fs.createReadStream('search_result.zip').pipe(unzipper.Extract({ path: 'unzips/trials' }));
  
  console.log("Success")

  
}

async function unzipsGerman(){
  
  var path = "zips/download"
  if (count > 0){
	  path += " ("+count+")"
  }
  path += ".zip"
  while (fs.existsSync(path)) {
	  var path = "zips/download"
	  if (count > 0){
		  path += " ("+count+")"
	  }
	  path += ".zip"
	  if(!fs.existsSync(path)){
		  return
	  }
	  count += 1;
	  fs.createReadStream(path).pipe(unzipper.Extract({ path: 'unzips/german' }));
	  
	  console.log("Success "+path)
  }
}

async function downloadResultsFromGermanPage(page)  {
  
  y = await page.evaluate((selector) => {
		  
		  var out = []
		  function pollDOM () {
			  const el = targetElement = document.querySelector('button[class="formButton"][type="submit"]');
			  //wait until the popup is loaded in
			  if (el) {
				  targetElement && targetElement.click();
				  return targetElement
			  } else {
				setTimeout(pollDOM, 300); // try again in 300 milliseconds
			  }
		  }
		  targetElement = pollDOM ()
		  
		  return targetElement;
		}, 'tr.rowASRLodd');	
  console.log(y);
  var path = "zips/download"
  if (count > 0){
	  path += " ("+count+")"
  }
  path += ".zip"
  
  count += 1;
  var counter = 1
  while (!fs.existsSync(path) && counter < 100) {
    //file exists
	sleep( 100 );
	console.log(counter)
	console.log(!fs.existsSync(path) && counter < 100)
	counter += 1
  }
  var location
  fs.createReadStream('search_result.zip').pipe(unzipper.Extract({ path: 'unzips/german' }));
  
  console.log("Success")


}

async function euSearch(page){
	
  let page_string = 'https://www.clinicaltrialsregister.eu/ctr-search/search?query=&page=1933'
  await page.goto(page_string, { waitUntil: 'networkidle0' }); // wait until page load
  
  while (true) {
	  count += 1
	  
	  await page._client.send('Page.setDownloadBehavior', {behavior: 'allow', downloadPath: dir+"\\eu\\"+count});
	  await page.$eval('#dContent', (el) => el.value = "full");
	  await downloadResultsFromEUPage(page)
	  
	  console.log("AAAAAAAAAAAa")
	  console.log(dir+"\\eu\\"+count)
	  but = await page.evaluate(() => {
		  
		  var out = []
		  // Scrape all contact info and names of the stored people
		  targetElement = document.querySelector('a[accesskey="n"]');
		  
		  // Specifically select Send money on some one with the given Name. As far as I have seen the name matches the contact name 
		  targetElement && targetElement.click();
		  
		  return targetElement;
		});
	  
	  console.log(but)
	  if (but == undefined){
		  return
	  }
	  await Promise.all([
		page.waitForNavigation({ waitUntil: 'networkidle0' }),
		console.log( 
		  "Waiting for Zelle load"
	  ), 
	  ]);
	  
  }
  
}


async function downloadResultsFromEUPage(page)  {
  console.log("BBBB")
  y = await page.evaluate(() => {
		  
		  var out = []
		  // Scrape all contact info and names of the stored people
		  targetElement = document.querySelector('input[id="submit-download"]');
		  
		  // Specifically select Send money on some one with the given Name. As far as I have seen the name matches the contact name 
		  targetElement && targetElement.click();
		  
		  return targetElement;
		});
	
	  // await Promise.all([
		// page.waitForNavigation({ waitUntil: 'networkidle0' }),
		// console.log( 
		  // "Waiting for Search Load"
	  // ), 
	  // ]);  
  console.log(y);
  
  
  console.log("Success")

  
}



main();

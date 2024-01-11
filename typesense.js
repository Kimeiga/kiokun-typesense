/*
 *  Our JavaScript client library works on both the server and the browser.
 *  When using the library on the browser, please be sure to use the
 *  search-only API Key rather than the master API key since the latter
 *  has write access to Typesense and you don't want to expose that.
 */
const util = require('util');
(async () => {

	const Typesense = require('typesense')

	let client = new Typesense.Client({
		'nodes': [{
			'host': 'localhost', // For Typesense Cloud use xxx.a1.typesense.net
			'port': 8108,      // For Typesense Cloud use 443
			'protocol': 'http'   // For Typesense Cloud use https
		}],
		'apiKey': 'GSV3UjDj0By3HYzmgWSiCsprcn7khNRY3EVyVfHcOXOMaV3y',
		'connectionTimeoutSeconds': 2
	})


	// client.collections('cedict').delete()
	// 	.then(response => {
	// 		console.log("Collection deleted:", response);
	// 	})
	// 	.catch(error => {
	// 		console.error("Error deleting collection:", error);
	// 	});


	// let cedictSchema = {
	// 	'name': 'cedict',
	// 	'fields': [
	// 		{ 'name': 't', 'type': 'string', "infix": true },
	// 		{ 'name': 's', 'type': 'string', "infix": true },
	// 		{ 'name': 'p', 'type': 'string', "infix": true },
	// 		{ 'name': 'd', 'type': 'string', "infix": true } // Changed to a single string
	// 	]
	// };
	// client.collections().create(cedictSchema)
	// 	.then(response => {
	// 		console.log("Collection created:", response);
	// 	})
	// 	.catch(error => {
	// 		console.error("Error creating collection:", error);
	// 	});



	// var fs = require('fs/promises');

	// const cedictData = await fs.readFile("output.jsonl");
	// // // client.collections('cedict').documents().import(cedictData);

	// // // Example: Assuming 'documents' is your array of documents
	// // // cedictData.forEach(document => {
	// // // 	document.d = document.d.join("/");
	// // // });

	// // Now import these documents into Typesense
	// client.collections('cedict').documents().import(cedictData)
	// 	.then(response => {
	// 		console.log("Documents imported:", response);
	// 	})
	// 	.catch(error => {
	// 		console.error("Error importing documents:", error);
	// 	});


	let searchParameters = {
		'q': '汉',
		'query_by': '*',
		// 50 per page
		'per_page': 50,
		'infix': 'always'
	};
	client.collections('cedict')
		.documents()
		.search(searchParameters)
		.then(function (searchResults) {
			for (const result of searchResults.hits) {
				console.log(result.document);
			}
			console.log(searchResults.found)
			console.log(searchResults.hits[0].document);
			console.log(searchResults.hits[1].document);
			console.log(searchResults.hits[2].document);

			// console.log(util.inspect(searchResults, { showHidden: false, depth: null, colors: true }));
		});


	// console.log(await client.collections('cedict').retrieve())

	// console.log(client.debug())

})();
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


	await client.collections('dictionary').delete()
		.then(response => {
			console.log("Collection deleted:", response);
		})
		.catch(error => {
			console.error("Error deleting collection:", error);
		});


	// let schema = {
	// 	"name": "dictionary",
	// 	"enable_nested_fields": true,
	// 	"fields": [
	// 		{ "name": "w_s", "type": "string", "infix": true },
	// 		{ "name": "w_t", "type": "string", "infix": true },
	// 		{ "name": "w_p", "type": "string[]", "infix": true },
	// 		{ "name": "w_d", "type": "string[]", "infix": true }
	// 	]
	// }
	let schema = {
		"name": "dictionary",
		"enable_nested_fields": true,
		"fields": [
			{ "name": "w_s", "type": "string", "infix": true, "optional": true },
			{ "name": "w_t", "type": "string", "infix": true, "optional": true },
			{ "name": "w_p", "type": "string[]", "infix": true, "optional": true },
			{ "name": "w_d", "type": "string[]", "infix": true, "optional": true },
			{ "name": "c_t", "type": "string", "infix": true, "optional": true }, // Traditional character
			{ "name": "c_s", "type": "string[]", "infix": true, "optional": true }, // Simplified variants
			{ "name": "c_g", "type": "string[]", "infix": true, "optional": true }, // Glosses
			{ "name": "c_p", "type": "string[]", "infix": true, "optional": true }, // Pinyin
			{ "name": "c_v", "type": "string[]", "infix": true, "optional": true }  // Other variants
		]
	}

	await client.collections().create(schema)
		.then(response => {
			console.log("Collection created:", response);
		})
		.catch(error => {
			console.error("Error creating collection:", error);
		});

	var fs = require('fs/promises');

	const data = await fs.readFile("all_data.jsonl");
	// // client.collections('cedict').documents().import(cedictData);

	// // Example: Assuming 'documents' is your array of documents
	// // cedictData.forEach(document => {
	// // 	document.d = document.d.join("/");
	// // });

	// Now import these documents into Typesense
	await client.collections('dictionary').documents().import(data)
		.then(response => {
			console.log("Documents imported:", response);
		})
		.catch(error => {
			console.error("Error importing documents:", error);
		});


	let searchParameters = {
		'q': '汉',
		'query_by': '*',
		// 50 per page
		'per_page': 50,
		'infix': 'always'
	};
	await client.collections('dictionary')
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
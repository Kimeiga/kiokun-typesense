import fs from 'fs';
import readline from 'readline';
import j2ch from "../j2ch.json" assert { type: 'json' };
import jmdict from "./jmdict-eng-3.5.0.json" assert { type: 'json' };

async function readJsonLines(filePath) {
    const fileStream = fs.createReadStream(filePath);
    const rl = readline.createInterface({
        input: fileStream,
        crlfDelay: Infinity
    });

    const objects = [];

    for await (const line of rl) {
        objects.push(JSON.parse(line));
    }

    return objects;
}

async function processDictionaries() {
    const filePath = "../zh/dictionary_word_2023-12-19.jsonl";
    const cWords = await readJsonLines(filePath);
    const cWordsSet = new Set(cWords.map(word => word.text)); // Assuming 'text' is the key to search for

    for (const entry of jmdict.words) {
        if (entry.kanji) {
            for (const kanji of entry.kanji) {
                if (!kanji.common) {

                    let charArrays = [];
                    let needed = false;

                    for (const char of kanji.text) {
                        if (char in j2ch) {
                            needed = true;
                            charArrays.push([...j2ch[char], char]);
                        } else {
                            charArrays.push([char]); // Add the character itself if not in j2ch
                        }
                    }

                    if (needed) {
                        const allCombinations = cartesianProduct(...charArrays);
                        for (const combination of allCombinations) {
                            const potentialCh = combination.join('');
                            // console.log(potentialCh)
                            if (cWordsSet.has(potentialCh)) {
                                console.log(potentialCh);
                            }
                        }
                    } else if (cWordsSet.has(kanji.text)) {
                        console.log(kanji.text);
                    }
                }
            }
        }
    }
}
function cartesianProduct(...arrays) {
    // Initialize the result array with an initial empty array
    let result = [[]];

    // For each array, map over each element in the result array and concatenate
    for (const array of arrays) {
        result = result.flatMap(resultArray =>
            array.map(item => [...resultArray, item])
        );
    }

    return result;
}

processDictionaries().catch(console.error);

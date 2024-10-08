const parse = require('bash-parser');
const { exec } = require('child_process');

const hasBannedChars = (input) => {
    const bannedCharsRegex = /[&`><*?x]/;
    return bannedCharsRegex.test(input);
};

const validateAST = (astNode) => {
    const requiredPrefix = 'whatTHEsigma';
    const hasPrefix = (str, prefix) => str.startsWith(prefix);

    const checkNode = (node) => {
        console.log("[1] node: ", node);
        console.log("[2] node[type]: ", node['type']);
        if (!node || node['type'] !== 'Script') {
            console.log("[0] failed script check")
            return false;
        }
        for (const command of node['commands']) {
            console.log("[3] command: ", command);
            console.log("[4] command[type]: ", command['type']);
            if (!command || command['type'] !== 'Command') {
                return false;
            }

            let sanitizedText = '';
    
            // console.log("[5] command['prefix'].length: ", command['prefix'].length)
            // console.log("[8] command['prefix']: ", command['prefix'])

            if (command['name'] && command['name']['text']) {
                sanitizedText = command['name']['text'].replace(/[^a-zA-Z]/g, '');
            } else if (command['prefix'] && command['prefix'].length > 0) {
                console.log("[6] command['prefix'][0][text]: ", command['prefix'][0]['text']);
                sanitizedText = command['prefix'][0]['text'].replace(/[^a-zA-Z]/g, '');
            }
            
            console.log("sanitizedText: ", sanitizedText);
            if (sanitizedText !== "" && !hasPrefix(sanitizedText, requiredPrefix)) {
                console.log("[9] failed prefix check")
                return false;
            }
        }
        return true;
    };
    
    return checkNode(astNode);
};

process.stdout.write(`Input: `);
process.stdin.on('data', (data) => {
    const userInput = data.toString().trim();
    const ast = parse(userInput);

    if (!validateAST(ast)) {
        console.log("[7] validate fail")
        process.stdout.write('whatTHEsigma\n');
        process.stdin.pause();  // Close the input stream
        return;
    }
    
    if (hasBannedChars(userInput)) {
        process.stdout.write('ban\n');
        process.stdin.pause();  // Close the input stream
        return;
    }
    
    exec(userInput, { shell: '/bin/bash' }, (error, stdout, stderr) => {
        if (error) {
            process.stdout.write(stderr);
            process.stdin.pause();  // Close the input stream
        } else {
            process.stdout.write(stdout);
            process.stdin.pause();  // Close the input stream
        }
    });
});
